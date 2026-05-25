"""Database models module.

SQLite에 저장할 데이터 구조를 dataclass로 정의한다.
"""

from dataclasses import dataclass


@dataclass
class Question:
    """기출문제 문항 모델."""

    year: int
    chapter: str
    question_type: str
    difficulty: str
    question_text: str
    answer: str | None = None


@dataclass
class KeywordStat:
    """키워드 통계 모델."""

    keyword: str
    count: int
