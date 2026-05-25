"""Pattern analysis module.

반복 출제되는 문제 유형, 키워드 조합, 단원 간 패턴을 분석한다.
"""

import pandas as pd


class PatternAnalyzer:
    """반복 출제 패턴 분석기."""

    def find_repeated_question_types(self, data: pd.DataFrame) -> pd.Series:
        """문제 유형별 반복 출제 빈도를 계산한다."""
        # TODO: question_type 컬럼 표준화 기능 추가
        return data["question_type"].value_counts()

    def find_keyword_patterns(self, tokenized_questions: list[list[str]]) -> dict[tuple[str, ...], int]:
        """문항별 토큰 목록에서 키워드 조합 패턴을 찾는다."""
        # TODO: n-gram 기반 패턴 분석으로 확장
        patterns: dict[tuple[str, ...], int] = {}
        for tokens in tokenized_questions:
            key = tuple(sorted(set(tokens)))
            patterns[key] = patterns.get(key, 0) + 1
        return patterns
