"""Database-facing application service."""

from __future__ import annotations

import pandas as pd

from examtrend_analyzer.database.db_manager import DatabaseManager


class DatabaseService:
    """Provides DataFrame-oriented persistence helpers for the UI."""

    def __init__(self, db_path: str = "examtrend.db") -> None:
        self.manager = DatabaseManager(db_path)
        self.manager.initialize()

    def save_questions(self, data: pd.DataFrame) -> int:
        """Save question rows into SQLite and return saved row count."""
        saved = 0
        for row in data.to_dict(orient="records"):
            self.manager.insert_question(
                year=int(row.get("year")),
                chapter=str(row.get("chapter", "")),
                question_type=str(row.get("question_type", "")),
                difficulty=str(row.get("difficulty", "")),
                question_text=str(row.get("question_text", "")),
                answer=str(row.get("answer", "")),
            )
            saved += 1
        return saved
