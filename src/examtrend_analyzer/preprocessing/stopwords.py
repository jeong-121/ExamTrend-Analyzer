"""Stopwords module.

분석에서 제외할 기본 불용어 목록과 필터링 함수를 제공한다.
"""

DEFAULT_STOPWORDS: set[str] = {
    "다음",
    "중",
    "것",
    "대한",
    "설명",
    "옳은",
    "고르시오",
    "문제",
}


def remove_stopwords(tokens: list[str], stopwords: set[str] | None = None) -> list[str]:
    """토큰 목록에서 불용어를 제거한다."""
    # TODO: 사용자 정의 불용어 파일 로딩 기능 추가
    active_stopwords = stopwords or DEFAULT_STOPWORDS
    return [token for token in tokens if token not in active_stopwords]
