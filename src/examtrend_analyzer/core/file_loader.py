"""Unified file loader for CSV, Excel, PDF, and TXT inputs."""

from __future__ import annotations

from pathlib import Path
import re

import pandas as pd

from examtrend_analyzer.core.pdf_loader import PdfQuestionLoader


class FileLoader:
    SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".pdf", ".txt"}

    def load(self, path: str | Path) -> pd.DataFrame:
        file_path = Path(path)
        suffix = file_path.suffix.lower()

        if suffix not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {suffix}")

        if suffix == ".csv":
            df = self._load_csv(file_path)
            return self._ensure_source_metadata(df, file_path)

        if suffix in {".xlsx", ".xls"}:
            df = pd.read_excel(file_path)
            return self._ensure_source_metadata(df, file_path)

        if suffix == ".pdf":
            df = PdfQuestionLoader().load(file_path)
            return self._ensure_source_metadata(df, file_path, source_type="pdf")

        if suffix == ".txt":
            text = file_path.read_text(encoding="utf-8")
            df = pd.DataFrame([{
                "question_no": None,
                "question_text": text,
                "source_page": None,
                "source_file": file_path.name,
                "source_type": "txt",
            }])
            return self._ensure_source_metadata(df, file_path, source_type="txt")

        raise ValueError(f"지원하지 않는 파일 형식입니다: {suffix}")

    def _load_csv(self, path: Path) -> pd.DataFrame:
        for encoding in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
            try:
                return pd.read_csv(path, encoding=encoding)
            except UnicodeDecodeError:
                continue

        raise UnicodeDecodeError(
            "unknown",
            b"",
            0,
            1,
            "CSV 인코딩을 판별하지 못했습니다. UTF-8 또는 CP949 파일인지 확인하세요.",
        )

    def _ensure_source_metadata(
        self,
        dataframe: pd.DataFrame,
        path: Path,
        source_type: str | None = None,
    ) -> pd.DataFrame:
        df = dataframe.copy()

        if "source_file" not in df.columns:
            df["source_file"] = path.name

        if source_type and "source_type" not in df.columns:
            df["source_type"] = source_type

        if "year" not in df.columns:
            year = self._extract_year_from_filename(path.name)
            if year is not None:
                df["year"] = year

        return df

    def _extract_year_from_filename(self, filename: str) -> int | None:
        match = re.search(r"(19|20)\d{2}", filename)
        if not match:
            return None

        return int(match.group(0))
