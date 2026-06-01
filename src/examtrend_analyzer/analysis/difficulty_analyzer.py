"""Difficulty analysis module."""

from __future__ import annotations

import pandas as pd

class DifficultyAnalyzer:
    DIFFICULTY_SCORE = {"하": 1, "중": 2, "상": 3, "easy": 1, "medium": 2, "hard": 3, "1": 1, "2": 2, "3": 3}

    def count_by_difficulty(self, data: pd.DataFrame) -> pd.Series:
        if "difficulty" not in data.columns:
            return pd.Series(dtype="int64")
        return data["difficulty"].fillna("미지정").astype(str).value_counts()

    def average_difficulty_by_year(self, data: pd.DataFrame) -> pd.Series:
        if "year" not in data.columns or "difficulty" not in data.columns:
            return pd.Series(dtype="float64")
        copied = data.copy()
        copied["difficulty_score"] = copied["difficulty"].astype(str).map(self.DIFFICULTY_SCORE)
        copied["year"] = pd.to_numeric(copied["year"], errors="coerce")
        return copied.dropna(subset=["year"]).groupby("year")["difficulty_score"].mean()
