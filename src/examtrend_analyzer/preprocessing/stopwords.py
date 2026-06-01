"""Stopwords module.

분석에서 제외할 기본 불용어 목록과 필터링 함수를 제공한다.
조사, 어미, 문제 지시문 표현이 상위 키워드에 노출되지 않도록 기본 사전을 넓게 둔다.
"""

from __future__ import annotations

DEFAULT_STOPWORDS: set[str] = {
    # 조사/접속/지시어
    "은", "는", "이", "가", "을", "를", "의", "에", "에서", "에게", "께", "로", "으로",
    "와", "과", "도", "만", "부터", "까지", "보다", "처럼", "및", "또는", "그리고", "그러나",
    # 문제 지시문에서 자주 나오는 일반어
    "다음", "중", "것", "것은", "것을", "것이", "있는", "없는", "옳은", "옳지", "않은",
    "고르시오", "선택하시오", "설명", "설명하시오", "서술하시오", "작성하시오", "구하시오",
    "무엇", "무엇인", "무엇인가", "어느", "해당", "해당하", "해당하는", "대한", "대해", "대하여", "관련", "문제",
    "보기", "아래", "위", "각", "가장", "올바른", "틀린", "알맞은", "바르게", "나타낸",
    # 분석에서 의미가 약한 일반 명사/동사
    "기본", "주요", "단계", "분석", "방법", "종류", "특징", "개념", "내용", "기능", "역할",
    "사용", "이용", "처리", "수행", "가능", "필요", "경우", "대상", "결과", "산출물",
}


def normalize_token(token: str) -> str:
    """키워드 비교를 위한 단일 토큰 정규화."""
    return str(token).strip()


def remove_stopwords(tokens: list[str], stopwords: set[str] | None = None, min_length: int = 2) -> list[str]:
    """토큰 목록에서 불용어, 빈 토큰, 1글자 한글 토큰, 순수 숫자 토큰을 제거한다."""
    active_stopwords = stopwords or DEFAULT_STOPWORDS
    filtered: list[str] = []

    for raw in tokens:
        token = normalize_token(raw)
        if not token:
            continue
        if token in active_stopwords:
            continue
        if token.isdigit():
            continue
        if len(token) < min_length:
            continue
        filtered.append(token)

    return filtered
