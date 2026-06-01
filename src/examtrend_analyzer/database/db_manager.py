"""SQLite database manager for datasets and analysis results."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

class DatabaseManager:
    """SQLite database management class."""

    def __init__(self, db_path: str | Path = "examtrend.db") -> None:
        self.db_path = Path(db_path)
        if self.db_path.parent != Path("."):
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def initialize(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS datasets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT,
                    file_name TEXT,
                    row_count INTEGER NOT NULL DEFAULT 0,
                    column_count INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dataset_id INTEGER,
                    question_id TEXT,
                    year INTEGER,
                    subject TEXT,
                    chapter TEXT,
                    question_type TEXT,
                    difficulty TEXT,
                    question_text TEXT NOT NULL,
                    answer TEXT,
                    explanation TEXT,
                    source TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(dataset_id) REFERENCES datasets(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS analysis_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dataset_id INTEGER,
                    title TEXT,
                    result_json TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(dataset_id) REFERENCES datasets(id) ON DELETE SET NULL
                );

                CREATE INDEX IF NOT EXISTS idx_questions_dataset ON questions(dataset_id);
                CREATE INDEX IF NOT EXISTS idx_questions_year ON questions(year);
                CREATE INDEX IF NOT EXISTS idx_analysis_runs_dataset ON analysis_runs(dataset_id);
                """
            )
            conn.commit()

    def insert_dataset(self, file_path: str | None, row_count: int, column_count: int) -> int:
        file_name = Path(file_path).name if file_path else ""
        with self.connect() as conn:
            cur = conn.execute(
                "INSERT INTO datasets(file_path, file_name, row_count, column_count) VALUES (?, ?, ?, ?)",
                (file_path, file_name, row_count, column_count),
            )
            conn.commit()
            return int(cur.lastrowid)

    def insert_question(self, dataset_id: int | None, **values: Any) -> int:
        with self.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO questions
                (dataset_id, question_id, year, subject, chapter, question_type, difficulty, question_text, answer, explanation, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    dataset_id,
                    values.get("question_id"),
                    values.get("year"),
                    values.get("subject"),
                    values.get("chapter"),
                    values.get("question_type"),
                    values.get("difficulty"),
                    values.get("question_text") or "",
                    values.get("answer"),
                    values.get("explanation"),
                    values.get("source"),
                ),
            )
            conn.commit()
            return int(cur.lastrowid)

    def insert_analysis_run(self, dataset_id: int | None, title: str, result: dict[str, Any]) -> int:
        with self.connect() as conn:
            cur = conn.execute(
                "INSERT INTO analysis_runs(dataset_id, title, result_json) VALUES (?, ?, ?)",
                (dataset_id, title, json.dumps(result, ensure_ascii=False)),
            )
            conn.commit()
            return int(cur.lastrowid)

    def list_analysis_runs(self, limit: int = 30) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT ar.id, ar.title, ar.created_at, d.file_name, d.row_count
                FROM analysis_runs ar
                LEFT JOIN datasets d ON d.id = ar.dataset_id
                ORDER BY ar.id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def load_analysis_run(self, run_id: int) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM analysis_runs WHERE id = ?", (run_id,)).fetchone()
        if row is None:
            return None
        data = dict(row)
        data["result"] = json.loads(data.pop("result_json"))
        return data
