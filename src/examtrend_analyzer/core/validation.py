"""Dataset validation rules mapped to requirements."""

from __future__ import annotations

from difflib import SequenceMatcher
import re

import pandas as pd

from examtrend_analyzer.core.models import ValidationIssue
from examtrend_analyzer.core.schema import REQUIRED_COLUMNS

class DatasetValidator:
    """Validate loaded exam-question datasets before analysis."""

    def __init__(self, min_year: int = 1990, max_year: int = 2100, similarity_threshold: float = 0.92) -> None:
        self.min_year = min_year
        self.max_year = max_year
        self.similarity_threshold = similarity_threshold

    def validate(self, data: pd.DataFrame) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        issues.extend(self._validate_not_empty(data))
        issues.extend(self._validate_required_columns(data))
        if any(issue.level == "error" for issue in issues):
            return issues
        issues.extend(self._validate_required_values(data))
        issues.extend(self._validate_year(data))
        issues.extend(self._validate_question_text_length(data))
        issues.extend(self._validate_duplicates(data))
        issues.extend(self._validate_near_duplicates(data))
        issues.extend(self._validate_difficulty(data))
        issues.extend(self._validate_answer(data))
        return issues

    def _validate_not_empty(self, data: pd.DataFrame) -> list[ValidationIssue]:
        if data.empty:
            return [ValidationIssue("error", "EMPTY_DATASET", "데이터셋에 분석할 행이 없습니다.")]
        return []

    def _validate_required_columns(self, data: pd.DataFrame) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for column in REQUIRED_COLUMNS:
            if column not in data.columns:
                issues.append(ValidationIssue("error", "MISSING_COLUMN", f"필수 컬럼이 없습니다: {column}", column=column))
        return issues

    def _validate_required_values(self, data: pd.DataFrame) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for column in ["year", "chapter", "question_type", "difficulty", "question_text", "answer"]:
            if column not in data.columns:
                continue
            empty = data[column].isna() | (data[column].astype(str).str.strip() == "")
            for idx in data.index[empty].tolist():
                level = "error" if column in {"year", "question_text"} else "warning"
                issues.append(ValidationIssue(level, "EMPTY_REQUIRED_VALUE", f"필수 값이 비어 있습니다: {column}", int(idx), column))
        return issues

    def _validate_year(self, data: pd.DataFrame) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        years = pd.to_numeric(data["year"], errors="coerce")
        invalid = years.isna() | (years < self.min_year) | (years > self.max_year)
        for idx in data.index[invalid].tolist():
            issues.append(ValidationIssue("warning", "INVALID_YEAR", f"연도 값이 비정상입니다. 허용 범위: {self.min_year}~{self.max_year}", int(idx), "year"))
        return issues

    def _validate_question_text_length(self, data: pd.DataFrame) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        text = data["question_text"].fillna("").astype(str).str.strip()
        too_short = text.str.len().between(1, 4)
        too_long = text.str.len() > 5000
        for idx in data.index[too_short].tolist():
            issues.append(ValidationIssue("warning", "QUESTION_TEXT_TOO_SHORT", "문제 본문이 지나치게 짧습니다.", int(idx), "question_text"))
        for idx in data.index[too_long].tolist():
            issues.append(ValidationIssue("warning", "QUESTION_TEXT_TOO_LONG", "문제 본문이 지나치게 깁니다.", int(idx), "question_text"))
        return issues

    def _validate_duplicates(self, data: pd.DataFrame) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        normalized = data["question_text"].fillna("").astype(str).map(self._normalize_text_for_compare)
        dupes = normalized.duplicated(keep=False) & (normalized != "")
        for idx in data.index[dupes].tolist():
            issues.append(ValidationIssue("warning", "DUPLICATE_QUESTION", "동일한 문제 본문이 중복되어 있습니다.", int(idx), "question_text"))
        return issues

    def _validate_near_duplicates(self, data: pd.DataFrame) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        texts = data["question_text"].fillna("").astype(str).map(self._normalize_text_for_compare)
        candidates = [(idx, txt) for idx, txt in texts.items() if len(txt) >= 20]
        # O(n^2) 방지: 큰 파일에서는 앞쪽 일부 후보만 빠르게 점검한다.
        max_pairs = 3000
        checked = 0
        for i, (idx_a, text_a) in enumerate(candidates):
            for idx_b, text_b in candidates[i + 1:]:
                if checked >= max_pairs:
                    return issues
                checked += 1
                if abs(len(text_a) - len(text_b)) > max(30, int(max(len(text_a), len(text_b)) * 0.25)):
                    continue
                score = SequenceMatcher(None, text_a, text_b).ratio()
                if score >= self.similarity_threshold:
                    issues.append(ValidationIssue("warning", "SIMILAR_QUESTION", f"유사 문항 후보입니다. 비교 행: {idx_b}, 유사도: {score:.2f}", int(idx_a), "question_text"))
                    break
        return issues

    def _validate_difficulty(self, data: pd.DataFrame) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        allowed = {"상", "중", "하", "최상", "최하", "easy", "medium", "hard", "1", "2", "3", "4", "5"}
        invalid = ~data["difficulty"].fillna("").astype(str).str.strip().str.lower().isin(allowed)
        for idx in data.index[invalid].tolist():
            issues.append(ValidationIssue("warning", "UNKNOWN_DIFFICULTY", "정의되지 않은 난이도 값입니다.", int(idx), "difficulty"))
        return issues

    def _validate_answer(self, data: pd.DataFrame) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        empty = data["answer"].isna() | (data["answer"].astype(str).str.strip() == "")
        for idx in data.index[empty].tolist():
            issues.append(ValidationIssue("warning", "EMPTY_ANSWER", "정답 값이 비어 있습니다.", int(idx), "answer"))
        return issues

    def _normalize_text_for_compare(self, text: str) -> str:
        return re.sub(r"\s+", "", str(text).strip().lower())
