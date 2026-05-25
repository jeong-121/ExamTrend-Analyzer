"""Difficulty analysis module.

난이도 분포와 연도별 난이도 변화를 분석한다.
"""

import pandas as pd


class DifficultyAnalyzer:
    """난이도 분석기."""

    DIFFICULTY_SCORE = {
        "하": 1,
        "중": 2,
        "상": 3,
    }

    def count_by_difficulty(self, data: pd.DataFrame) -> pd.Series:
        """난이도별 문항 수를 계산한다."""
        # TODO: 난이도 값 검증 및 사용자 정의 난이도 체계 지원
        return data["difficulty"].value_counts()

    def average_difficulty_by_year(self, data: pd.DataFrame) -> pd.Series:
        """연도별 평균 난이도 점수를 계산한다."""
        copied = data.copy()
        copied["difficulty_score"] = copied["difficulty"].map(self.DIFFICULTY_SCORE)
        return copied.groupby("year")["difficulty_score"].mean()
