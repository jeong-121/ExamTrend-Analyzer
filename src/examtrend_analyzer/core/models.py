"""Core dataclasses used across services and UI."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ValidationIssue:
    level: str
    code: str
    message: str
    row_index: int | None = None
    column: str | None = None


@dataclass(slots=True)
class DatasetSummary:
    file_path: Path | None = None
    row_count: int = 0
    column_count: int = 0
    years: list[int] = field(default_factory=list)
    chapters: list[str] = field(default_factory=list)
    difficulties: list[str] = field(default_factory=list)


@dataclass(slots=True)
class AnalysisResult:
    summary: DatasetSummary
    keyword_counts: dict[str, int]
    yearly_counts: dict[Any, int]
    chapter_counts: dict[str, int]
    difficulty_counts: dict[str, int]
    average_difficulty_by_year: dict[Any, float]
    issues: list[ValidationIssue] = field(default_factory=list)
    keyword_rows: list[dict[str, object]] = field(default_factory=list)
    bigrams: dict[str, int] = field(default_factory=dict)
    trigrams: dict[str, int] = field(default_factory=dict)
    tfidf: list[dict[str, object]] = field(default_factory=list)
    similar_pairs: list[dict[str, object]] = field(default_factory=list)
    analysis_status: dict[str, str] = field(default_factory=dict)
    skipped_analyses: list[str] = field(default_factory=list)
    chapter_source: str = "none"
    chapter_distribution: list[dict[str, object]] = field(default_factory=list)
