"""Chapter distribution analysis."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class ChapterAnalyzer:
    def analyze_chapter_distribution(
        self,
        dataframe: pd.DataFrame,
        chapter_column: str = "chapter",
    ) -> list[dict[str, object]]:
        if chapter_column not in dataframe.columns or dataframe.empty:
            return []

        counts = dataframe[chapter_column].fillna("미분류").astype(str).value_counts()
        total = int(counts.sum())

        return [
            {
                "chapter": str(chapter),
                "count": int(count),
                "ratio": round((int(count) / total) * 100, 2) if total else 0.0,
            }
            for chapter, count in counts.items()
        ]

    def analyze_chapter_by_year(
        self,
        dataframe: pd.DataFrame,
        chapter_column: str = "chapter",
        year_column: str = "year",
    ) -> dict[str, dict[str, int]]:
        if chapter_column not in dataframe.columns or year_column not in dataframe.columns:
            return {}

        result: dict[str, dict[str, int]] = {}

        for year, group in dataframe.groupby(year_column):
            counts = group[chapter_column].fillna("미분류").astype(str).value_counts()
            result[str(year)] = {
                str(chapter): int(count)
                for chapter, count in counts.items()
            }

        return dict(sorted(result.items(), key=lambda item: item[0]))
