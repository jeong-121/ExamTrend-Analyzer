"""Trend analysis module.

연도별, 단원별 출제 빈도와 비중을 분석한다.
"""

import pandas as pd


class TrendAnalyzer:
    """출제 경향 분석기."""

    def count_by_year(self, data: pd.DataFrame) -> pd.Series:
        """연도별 문항 수를 계산한다."""
        # TODO: year 컬럼 검증 로직 추가
        return data["year"].value_counts().sort_index()

    def count_by_chapter(self, data: pd.DataFrame) -> pd.Series:
        """단원별 문항 수를 계산한다."""
        # TODO: chapter 컬럼이 없는 경우 예외 처리 추가
        return data["chapter"].value_counts()

    def chapter_ratio(self, data: pd.DataFrame) -> pd.Series:
        """단원별 출제 비중을 계산한다."""
        counts = self.count_by_chapter(data)
        return counts / counts.sum()
