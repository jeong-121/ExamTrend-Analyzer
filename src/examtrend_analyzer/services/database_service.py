"""Database service wrapper."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

import pandas as pd

from examtrend_analyzer.config.settings import DEFAULT_DB_PATH
from examtrend_analyzer.core.models import AnalysisResult, DatasetSummary, ValidationIssue
from examtrend_analyzer.database.db_manager import DatabaseManager


class DatabaseService:
    """High-level persistence API used by UI and services."""

    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH) -> None:
        self.manager = DatabaseManager(db_path)
        self.manager.initialize()

    def save_questions(self, data: pd.DataFrame, file_path: str | Path | None = None) -> int:
        dataset_id = self.manager.insert_dataset(
            str(file_path) if file_path else None,
            row_count=len(data),
            column_count=len(data.columns),
        )
        for _, row in data.iterrows():
            self.manager.insert_question(
                dataset_id,
                question_id=self._clean(row.get("question_id")),
                year=self._to_int(row.get("year")),
                subject=self._clean(row.get("subject")),
                chapter=self._clean(row.get("chapter")),
                question_type=self._clean(row.get("question_type")),
                difficulty=self._clean(row.get("difficulty")),
                question_text=self._clean(row.get("question_text")),
                answer=self._clean(row.get("answer")),
                explanation=self._clean(row.get("explanation")),
                source=self._clean(row.get("source")),
            )
        return dataset_id

    def save_analysis_result(self, result: AnalysisResult, dataset_id: int | None = None, title: str = "기출문제 분석 결과") -> int:
        return self.manager.insert_analysis_run(dataset_id, title, self.result_to_dict(result))

    def list_analysis_runs(self, limit: int = 30) -> list[dict[str, Any]]:
        return self.manager.list_analysis_runs(limit)

    def load_analysis_run(self, run_id: int) -> AnalysisResult | None:
        stored = self.manager.load_analysis_run(run_id)
        if stored is None:
            return None
        return self.result_from_dict(stored["result"])

    def result_to_dict(self, result: AnalysisResult) -> dict[str, Any]:
        return {
            "summary": {
                "file_path": str(result.summary.file_path) if result.summary.file_path else None,
                "row_count": result.summary.row_count,
                "column_count": result.summary.column_count,
                "years": result.summary.years,
                "chapters": result.summary.chapters,
                "difficulties": result.summary.difficulties,
            },
            "keyword_counts": result.keyword_counts,
            "yearly_counts": {str(k): v for k, v in result.yearly_counts.items()},
            "chapter_counts": result.chapter_counts,
            "difficulty_counts": result.difficulty_counts,
            "average_difficulty_by_year": {str(k): v for k, v in result.average_difficulty_by_year.items()},
            "issues": [asdict(issue) for issue in result.issues],
            "keyword_rows": result.keyword_rows,
            "bigrams": result.bigrams,
            "trigrams": result.trigrams,
            "tfidf": result.tfidf,
            "similar_pairs": result.similar_pairs,
        }

    def result_from_dict(self, payload: dict[str, Any]) -> AnalysisResult:
        summary_payload = payload.get("summary", {})
        summary = DatasetSummary(
            file_path=Path(summary_payload["file_path"]) if summary_payload.get("file_path") else None,
            row_count=int(summary_payload.get("row_count", 0)),
            column_count=int(summary_payload.get("column_count", 0)),
            years=list(summary_payload.get("years", [])),
            chapters=list(summary_payload.get("chapters", [])),
            difficulties=list(summary_payload.get("difficulties", [])),
        )
        issues = [ValidationIssue(**issue) for issue in payload.get("issues", [])]
        return AnalysisResult(
            summary=summary,
            keyword_counts={str(k): int(v) for k, v in payload.get("keyword_counts", {}).items()},
            yearly_counts=payload.get("yearly_counts", {}),
            chapter_counts=payload.get("chapter_counts", {}),
            difficulty_counts=payload.get("difficulty_counts", {}),
            average_difficulty_by_year=payload.get("average_difficulty_by_year", {}),
            issues=issues,
            keyword_rows=list(payload.get("keyword_rows", [])),
            bigrams={str(k): int(v) for k, v in payload.get("bigrams", {}).items()},
            trigrams={str(k): int(v) for k, v in payload.get("trigrams", {}).items()},
            tfidf=list(payload.get("tfidf", [])),
            similar_pairs=list(payload.get("similar_pairs", [])),
        )

    def _clean(self, value: Any) -> str:
        if pd.isna(value):
            return ""
        return str(value).strip()

    def _to_int(self, value: Any) -> int | None:
        try:
            if pd.isna(value):
                return None
            return int(float(value))
        except (TypeError, ValueError):
            return None
