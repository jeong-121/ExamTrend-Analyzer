"""Keyword-based chapter classifier.

This classifier is intentionally transparent and rule-based. It is used
when imported exam files do not contain a `chapter` column.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from examtrend_analyzer.preprocessing.tokenizer import KoreanTokenizer


DEFAULT_CHAPTER_KEYWORDS: dict[str, list[str]] = {
    "데이터베이스": [
        "SQL", "정규화", "반정규화", "트랜잭션", "ACID", "무결성", "관계형",
        "관계", "릴레이션", "튜플", "속성", "키", "기본키", "외래키",
        "조인", "인덱스", "뷰", "스키마", "DDL", "DML", "DCL", "ERD",
        "개체", "엔티티", "데이터베이스",
    ],
    "운영체제": [
        "프로세스", "스레드", "스케줄링", "교착상태", "데드락", "메모리",
        "가상메모리", "페이지", "세그먼트", "커널", "시스템콜", "인터럽트",
        "뮤텍스", "세마포어", "동기화", "CPU", "운영체제",
    ],
    "네트워크": [
        "TCP", "UDP", "IP", "HTTP", "HTTPS", "DNS", "라우팅", "라우터",
        "스위치", "패킷", "프로토콜", "OSI", "계층", "서브넷", "게이트웨이",
        "네트워크", "이더넷", "ARP",
    ],
    "자료구조": [
        "배열", "리스트", "스택", "큐", "트리", "그래프", "힙", "해시",
        "테이블", "정렬", "탐색", "이진", "노드", "간선", "자료구조",
    ],
    "알고리즘": [
        "시간복잡도", "복잡도", "탐욕", "그리디", "동적", "DP", "분할정복",
        "백트래킹", "최단경로", "다익스트라", "플로이드", "알고리즘",
    ],
    "소프트웨어공학": [
        "요구사항", "UML", "UseCase", "유스케이스", "클래스다이어그램",
        "시퀀스", "테스트", "폭포수", "애자일", "스크럼", "설계", "모델링",
        "소프트웨어",
    ],
    "인공지능": [
        "인공지능", "AI", "머신러닝", "기계학습", "딥러닝", "신경망",
        "지도학습", "비지도학습", "강화학습", "분류", "회귀", "확산",
        "생성", "모델", "잠재", "노이즈",
    ],
    "국어/독서": [
        "윗글", "독서", "내용", "일치", "적절", "문맥", "글쓴이",
        "밑줄", "보기", "추론", "이해", "문단", "화자",
    ],
    "문학": [
        "시", "소설", "화자", "서술자", "인물", "작품", "정서", "표현",
        "구절", "운율", "상징", "이미지", "갈등", "사건",
    ],
}


@dataclass
class ChapterClassifier:
    """Classify a question into a chapter using weighted keyword matching."""

    chapter_keywords: dict[str, list[str]] = field(
        default_factory=lambda: dict(DEFAULT_CHAPTER_KEYWORDS)
    )
    tokenizer: KoreanTokenizer | None = None
    min_score: int = 1

    def __post_init__(self) -> None:
        if self.tokenizer is None:
            self.tokenizer = KoreanTokenizer()

    def classify(self, text: object) -> str:
        scores = self.score(text)

        if not scores:
            return "미분류"

        best_chapter, best_score = max(scores.items(), key=lambda item: item[1])

        if best_score < self.min_score:
            return "미분류"

        return best_chapter

    def score(self, text: object) -> dict[str, int]:
        raw_text = "" if text is None else str(text)
        tokens = set(self.tokenizer.tokenize(raw_text))
        upper_tokens = {token.upper() for token in tokens}

        scores: dict[str, int] = {}

        for chapter, keywords in self.chapter_keywords.items():
            score = 0

            for keyword in keywords:
                keyword_text = str(keyword)
                if keyword_text in raw_text:
                    score += 2

                if keyword_text in tokens or keyword_text.upper() in upper_tokens:
                    score += 3

            if score > 0:
                scores[chapter] = score

        return scores
