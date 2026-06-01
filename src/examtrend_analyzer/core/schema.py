"""Data schema, aliases, and field mapping utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

REQUIRED_COLUMNS = ["question_text"]
OPTIONAL_COLUMNS = ["year", "chapter", "question_type", "difficulty", "answer", "explanation", "source", "subject", "exam_name", "question_id"]
STANDARD_COLUMNS = REQUIRED_COLUMNS + OPTIONAL_COLUMNS

COLUMN_LABELS: dict[str, str] = {
    "year": "연도",
    "chapter": "단원",
    "question_type": "문제 유형",
    "difficulty": "난이도",
    "question_text": "문제 본문",
    "answer": "정답",
    "explanation": "해설",
    "source": "출처",
    "subject": "과목",
    "exam_name": "시험명",
    "exam_round": "회차",
    "month": "월",
    "question_id": "문항 ID",
}

COLUMN_ALIASES: dict[str, str] = {
    "year": "year", "년도": "year", "연도": "year", "출제연도": "year", "시행연도": "year",
    "chapter": "chapter", "chapter_auto": "chapter", "단원": "chapter", "챕터": "chapter", "영역": "chapter", "대단원": "chapter", "소단원": "chapter",
    "question_type": "question_type", "유형": "question_type", "문제유형": "question_type", "문항유형": "question_type", "객관식/주관식": "question_type",
    "difficulty": "difficulty", "난이도": "difficulty", "level": "difficulty", "등급": "difficulty",
    "question_text": "question_text", "문제": "question_text", "문항": "question_text", "문제본문": "question_text", "문항본문": "question_text", "질문": "question_text", "내용": "question_text",
    "answer": "answer", "정답": "answer", "답": "answer", "답안": "answer",
    "explanation": "explanation", "해설": "explanation", "설명": "explanation",
    "source": "source", "출처": "source", "기출": "source", "자료출처": "source",
    "subject": "subject", "과목": "subject", "교과목": "subject",
    "exam_name": "exam_name", "시험명": "exam_name", "시험": "exam_name", "시험종류": "exam_name", "회차": "exam_round", "차수": "exam_round", "exam_round": "exam_round", "월": "month", "month": "month",
    "question_id": "question_id", "문항ID": "question_id", "문제ID": "question_id", "id": "question_id", "번호": "question_id",
}

@dataclass(slots=True)
class FieldMapping:
    """Mapping between original dataset columns and normalized project columns."""

    mapping: dict[str, str] = field(default_factory=dict)  # original -> standard

    def original_for(self, standard_column: str) -> str | None:
        for original, standard in self.mapping.items():
            if standard == standard_column:
                return original
        return None

    def missing_required(self) -> list[str]:
        mapped = set(self.mapping.values())
        return [column for column in REQUIRED_COLUMNS if column not in mapped]

    def as_rename_dict(self) -> dict[str, str]:
        return {original: standard for original, standard in self.mapping.items() if standard}


def normalize_column_name(name: str) -> str:
    cleaned = str(name).strip()
    compact = cleaned.replace(" ", "").replace("_", "").lower()
    if cleaned in COLUMN_ALIASES:
        return COLUMN_ALIASES[cleaned]
    if compact in COLUMN_ALIASES:
        return COLUMN_ALIASES[compact]
    return cleaned


def suggest_field_mapping(columns: list[str]) -> FieldMapping:
    mapping: dict[str, str] = {}
    used: set[str] = set()
    for column in columns:
        standard = normalize_column_name(column)
        if standard in STANDARD_COLUMNS and standard not in used:
            mapping[column] = standard
            used.add(standard)
        else:
            mapping[column] = ""
    return FieldMapping(mapping)


def apply_field_mapping(columns: list[str], mapping: Mapping[str, str]) -> list[str]:
    result: list[str] = []
    seen: dict[str, int] = {}
    for column in columns:
        target = mapping.get(column) or normalize_column_name(column)
        if target in STANDARD_COLUMNS:
            count = seen.get(target, 0)
            seen[target] = count + 1
            result.append(target if count == 0 else f"{target}_{count + 1}")
        else:
            result.append(str(column).strip())
    return result


AUTO_MAPPING_EXTRA_ALIASES = {
    "question_no": "question_id",
    "문항번호": "question_id",
    "번호": "question_id",
    "source_page": "source",
    "source_file": "source",
    "source_type": "source",
    "출제년도": "year",
    "시행년도": "year",
    "학년도": "year",
    "영역": "chapter",
    "과목명": "subject",
    "선택과목": "subject",
    "문제내용": "question_text",
    "문제 텍스트": "question_text",
    "문항 텍스트": "question_text",
    "지문": "question_text",
}

COLUMN_ALIASES.update(AUTO_MAPPING_EXTRA_ALIASES)
