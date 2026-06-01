"""Year-based exam trend analysis."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

import pandas as pd

from examtrend_analyzer.preprocessing.tokenizer import KoreanTokenizer


@dataclass
class TrendAnalyzer:
    tokenizer: KoreanTokenizer | None = None

    def __post_init__(self) -> None:
        if self.tokenizer is None:
            self.tokenizer = KoreanTokenizer()

    def analyze_yearly_keywords(
        self,
        dataframe: pd.DataFrame,
        question_column: str = "question_text",
        year_column: str = "year",
        top_n: int = 10,
    ) -> dict[str, dict[str, int]]:
        if question_column not in dataframe.columns or year_column not in dataframe.columns:
            return {}

        result: dict[str, dict[str, int]] = {}

        for year, group in dataframe.groupby(year_column):
            counter: Counter[str] = Counter()
            for text in group[question_column].fillna("").astype(str):
                counter.update(self.tokenizer.tokenize(text))
            result[str(year)] = dict(counter.most_common(top_n))

        return dict(sorted(result.items(), key=lambda item: item[0]))

    def analyze_keyword_year_matrix(
        self,
        dataframe: pd.DataFrame,
        question_column: str = "question_text",
        year_column: str = "year",
    ) -> dict[str, dict[str, int]]:
        if question_column not in dataframe.columns or year_column not in dataframe.columns:
            return {}

        matrix: dict[str, Counter[str]] = defaultdict(Counter)

        for _, row in dataframe.iterrows():
            year = str(row.get(year_column, "")).strip()
            if not year:
                continue
            tokens = self.tokenizer.tokenize(row.get(question_column, ""))
            matrix[year].update(tokens)

        return {
            year: dict(counter)
            for year, counter in sorted(matrix.items(), key=lambda item: item[0])
        }

    def find_rising_keywords(
        self,
        dataframe: pd.DataFrame,
        question_column: str = "question_text",
        year_column: str = "year",
        recent_year_count: int = 3,
        top_n: int = 20,
    ) -> list[dict[str, object]]:
        matrix = self.analyze_keyword_year_matrix(
            dataframe,
            question_column=question_column,
            year_column=year_column,
        )

        if not matrix:
            return []

        years = sorted(matrix.keys())
        if len(years) < 2:
            return []

        recent_years = years[-recent_year_count:]
        previous_years = years[:-recent_year_count] or years[:1]

        keywords: set[str] = set()
        for counter in matrix.values():
            keywords.update(counter.keys())

        rows: list[dict[str, object]] = []

        for keyword in keywords:
            recent_total = sum(matrix[year].get(keyword, 0) for year in recent_years)
            previous_total = sum(matrix[year].get(keyword, 0) for year in previous_years)

            if recent_total <= 0:
                continue

            recent_avg = recent_total / max(len(recent_years), 1)
            previous_avg = previous_total / max(len(previous_years), 1)
            growth = recent_avg - previous_avg

            rows.append({
                "keyword": keyword,
                "recent_total": int(recent_total),
                "previous_total": int(previous_total),
                "growth": round(float(growth), 4),
                "recent_years": recent_years,
            })

        rows.sort(key=lambda row: (row["growth"], row["recent_total"]), reverse=True)
        return rows[:top_n]
