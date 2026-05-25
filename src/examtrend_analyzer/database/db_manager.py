"""Database manager module.

SQLite 연결, 테이블 생성, 기본 CRUD 작업을 담당한다.
"""

import sqlite3
from pathlib import Path


class DatabaseManager:
    """SQLite 데이터베이스 관리 클래스."""

    def __init__(self, db_path: str | Path = "examtrend.db") -> None:
        self.db_path = Path(db_path)

    def connect(self) -> sqlite3.Connection:
        """SQLite 데이터베이스 연결을 생성한다."""
        # TODO: row_factory 설정 및 트랜잭션 관리 기능 추가
        return sqlite3.connect(self.db_path)

    def initialize(self) -> None:
        """기본 테이블을 생성한다."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    chapter TEXT NOT NULL,
                    question_type TEXT,
                    difficulty TEXT,
                    question_text TEXT NOT NULL,
                    answer TEXT
                )
                """
            )
            conn.commit()

    def insert_question(
        self,
        year: int,
        chapter: str,
        question_type: str,
        difficulty: str,
        question_text: str,
        answer: str,
    ) -> None:
        """문항 데이터를 데이터베이스에 저장한다."""
        # TODO: 중복 문항 방지 정책 추가
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO questions
                (year, chapter, question_type, difficulty, question_text, answer)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (year, chapter, question_type, difficulty, question_text, answer),
            )
            conn.commit()
