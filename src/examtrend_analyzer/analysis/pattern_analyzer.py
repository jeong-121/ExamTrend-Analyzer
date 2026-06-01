"""Repeated pattern analysis for exam topics."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

import pandas as pd

from examtrend_analyzer.preprocessing.tokenizer import KoreanTokenizer


@dataclass
class PatternAnalyzer:
    tokenizer: KoreanTokenizer | None = None

    def __post_init__(self) -> None:
        if self.tokenizer is None:
            self.tokenizer = KoreanTokenizer()

    def analyze_repeated_keywords(
        self,
        dataframe: pd.DataFrame,
        question_column: str = "question_text",
        year_column: str = "year",
        min_years: int = 2,
        top_n: int = 30,
    ) -> list[dict[str, object]]:
        if question_column not in dataframe.columns:
            return []

        keyword_years: dict[str, set[str]] = defaultdict(set)
        keyword_total: Counter[str] = Counter()

        for _, row in dataframe.iterrows():
            year = (
                str(row.get(year_column, "미상")).strip()
                if year_column in dataframe.columns
                else "미상"
            )
            tokens = self.tokenizer.tokenize(row.get(question_column, ""))
            keyword_total.update(tokens)

            for token in set(tokens):
                keyword_years[token].add(year)

        rows: list[dict[str, object]] = []

        for keyword, years in keyword_years.items():
            if len(years) < min_years:
                continue

            sorted_years = sorted(years)

            rows.append({
                "keyword": keyword,
                "total_count": int(keyword_total[keyword]),
                "year_count": int(len(years)),
                "years": sorted_years,
                "consecutive_streak": self._longest_consecutive_streak(sorted_years),
            })

        rows.sort(
            key=lambda row: (
                row["year_count"],
                row["consecutive_streak"],
                row["total_count"],
            ),
            reverse=True,
        )

        return rows[:top_n]

    def _longest_consecutive_streak(self, years: list[str]) -> int:
        numeric_years: list[int] = []

        for year in years:
            try:
                numeric_years.append(int(float(year)))
            except Exception:
                continue

        if not numeric_years:
            return 0

        numeric_years = sorted(set(numeric_years))
        best = 1
        current = 1

        for previous, now in zip(numeric_years, numeric_years[1:]):
            if now == previous + 1:
                current += 1
            else:
                best = max(best, current)
                current = 1

        return max(best, current)
