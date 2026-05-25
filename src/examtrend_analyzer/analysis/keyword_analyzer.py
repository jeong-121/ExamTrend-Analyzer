"""Keyword analysis module.

문항 텍스트 또는 토큰 목록을 기반으로 키워드 빈도를 계산한다.
"""

from collections import Counter


class KeywordAnalyzer:
    """키워드 빈도 분석기."""

    def analyze(self, tokens: list[str]) -> dict[str, int]:
        """토큰 목록에서 키워드 빈도를 계산한다.

        Args:
            tokens: 전처리와 토큰화를 거친 문자열 목록.

        Returns:
            키워드를 key, 빈도를 value로 갖는 딕셔너리.
        """
        # TODO: 품사 필터링, 최소 길이 필터링, 상위 N개 추출 옵션 추가
        return dict(Counter(tokens))

    def top_n(self, tokens: list[str], n: int = 20) -> list[tuple[str, int]]:
        """상위 N개 키워드를 반환한다."""
        counter = Counter(tokens)
        return counter.most_common(n)
