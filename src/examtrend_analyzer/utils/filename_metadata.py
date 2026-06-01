"""Extract exam metadata from filenames."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


YEAR_RE = re.compile(r"(19\d{2}|20\d{2})")
ROUND_RE = re.compile(r"(?<!\d)(\d{1,2})\s*(?:회|차|round|Round|ROUND)")
MONTH_RE = re.compile(r"(?<!\d)(1[0-2]|0?[1-9])\s*월")


@dataclass(frozen=True)
class FileMetadata:
    year: int | None = None
    exam_round: int | None = None
    month: int | None = None
    exam_name: str | None = None
    source_file: str = ""


def extract_metadata_from_filename(path: str | Path) -> FileMetadata:
    file_path = Path(path)
    stem = file_path.stem

    year = _extract_int(YEAR_RE, stem)
    exam_round = _extract_int(ROUND_RE, stem)
    month = _extract_int(MONTH_RE, stem)

    exam_name = stem
    if year is not None:
        exam_name = re.sub(str(year), "", exam_name)
    if exam_round is not None:
        exam_name = re.sub(rf"{exam_round}\s*(?:회|차|round|Round|ROUND)", "", exam_name)
    if month is not None:
        exam_name = re.sub(rf"0?{month}\s*월", "", exam_name)

    exam_name = re.sub(r"[_\-\(\)\[\]\s]+", " ", exam_name).strip()
    exam_name = exam_name or None

    return FileMetadata(
        year=year,
        exam_round=exam_round,
        month=month,
        exam_name=exam_name,
        source_file=file_path.name,
    )


def _extract_int(pattern: re.Pattern[str], text: str) -> int | None:
    match = pattern.search(text)
    if not match:
        return None
    try:
        return int(match.group(1))
    except Exception:
        return None
