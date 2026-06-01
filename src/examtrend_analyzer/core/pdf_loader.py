"""PDF loading and question extraction utilities.

This module handles text-based PDFs. Scanned PDFs require OCR and are
intentionally reported as unsupported by this loader.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable

import pandas as pd


QUESTION_START_RE = re.compile(r"(?m)^\s*(\d{1,3})\.\s+")
HEADER_FOOTER_PATTERNS = [
    re.compile(r"^\s*\d+\s*홀수형\s*$"),
    re.compile(r"^\s*홀수형\s*\d+\s*$"),
    re.compile(r"^\s*\d+\s+\d+\s*$"),
    re.compile(r"^\s*\d+\s*/\s*\d+\s*$"),
    re.compile(r"^\s*이 문제지에 관한 저작권은.*$"),
    re.compile(r"^\s*2025학년도 대학수학능력시험 문제지.*$"),
    re.compile(r"^\s*제\s*\d+\s*교시.*$"),
    re.compile(r"^\s*국어\s*영역.*$"),
]


@dataclass
class PdfQuestionLoader:
    """Extract question-like rows from a text-based PDF."""

    min_question_length: int = 8

    def load(self, path: str | Path) -> pd.DataFrame:
        pdf_path = Path(path)
        text = self.extract_text(pdf_path)
        questions = self.extract_questions(text)

        if not questions:
            # Preserve raw text as a single row if question splitting fails.
            questions = [{
                "question_no": None,
                "question_text": text.strip(),
                "source_page": None,
                "source_file": pdf_path.name,
                "source_type": "pdf",
            }]

        return pd.DataFrame(questions)

    def extract_text(self, path: str | Path) -> str:
        try:
            import fitz  # PyMuPDF
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(
                "PDF 처리를 위해 PyMuPDF가 필요합니다. "
                "pip install PyMuPDF 명령으로 설치하세요."
            ) from exc

        pdf_path = Path(path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")

        pages: list[str] = []
        with fitz.open(pdf_path) as doc:
            for page_index, page in enumerate(doc, start=1):
                page_text = page.get_text("text")
                page_text = self._clean_page_text(page_text)
                if page_text.strip():
                    pages.append(f"\n[PAGE {page_index}]\n{page_text}")

        text = "\n".join(pages).strip()
        if not text:
            raise ValueError(
                "PDF에서 텍스트를 추출하지 못했습니다. "
                "스캔 이미지 PDF일 가능성이 높으며 OCR 기능이 필요합니다."
            )
        return text

    def extract_questions(self, text: str) -> list[dict[str, object]]:
        normalized = self._normalize_text(text)
        matches = list(QUESTION_START_RE.finditer(normalized))
        rows: list[dict[str, object]] = []

        for index, match in enumerate(matches):
            question_no = int(match.group(1))
            start = match.start()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(normalized)
            block = normalized[start:end].strip()
            block = self._trim_to_question_block(block)

            if len(block) < self.min_question_length:
                continue

            page = self._find_nearest_page_marker(normalized, start)
            rows.append({
                "question_no": question_no,
                "question_text": block,
                "source_page": page,
                "source_file": "",
                "source_type": "pdf",
            })

        return rows

    def _clean_page_text(self, text: str) -> str:
        lines = []
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if any(pattern.match(line) for pattern in HEADER_FOOTER_PATTERNS):
                continue
            lines.append(line)
        return "\n".join(lines)

    def _normalize_text(self, text: str) -> str:
        text = text.replace("\u00a0", " ")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _trim_to_question_block(self, block: str) -> str:
        # Keep answer choices inside the same question block.
        block = re.sub(r"\n+", "\n", block)
        return block.strip()

    def _find_nearest_page_marker(self, text: str, position: int) -> int | None:
        markers = list(re.finditer(r"\[PAGE\s+(\d+)\]", text[:position]))
        if not markers:
            return None
        return int(markers[-1].group(1))
