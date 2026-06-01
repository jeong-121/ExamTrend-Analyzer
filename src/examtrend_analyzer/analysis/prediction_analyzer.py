"""Transparent heuristic scoring for likely future exam topics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PredictionAnalyzer:
    def rank_candidate_topics(
        self,
        repeated_keywords: list[dict[str, object]],
        rising_keywords: list[dict[str, object]],
        tfidf_rows: list[dict[str, object]],
        top_n: int = 20,
    ) -> list[dict[str, object]]:
        scores: dict[str, dict[str, object]] = {}

        def ensure(keyword: str) -> dict[str, object]:
            if keyword not in scores:
                scores[keyword] = {
                    "keyword": keyword,
                    "score": 0.0,
                    "reasons": [],
                }
            return scores[keyword]

        for row in repeated_keywords:
            keyword = str(row["keyword"])
            target = ensure(keyword)

            year_count = int(row.get("year_count", 0))
            streak = int(row.get("consecutive_streak", 0))
            total_count = int(row.get("total_count", 0))

            points = year_count * 2.0 + streak * 1.5 + min(total_count, 20) * 0.2

            target["score"] = float(target["score"]) + points
            target["reasons"].append(
                f"{year_count}개 연도 출제, 최장 {streak}년 연속"
            )

        for row in rising_keywords:
            keyword = str(row["keyword"])
            target = ensure(keyword)

            growth = float(row.get("growth", 0.0))
            recent_total = int(row.get("recent_total", 0))

            points = max(growth, 0.0) * 2.5 + recent_total * 0.3

            target["score"] = float(target["score"]) + points
            target["reasons"].append(
                f"최근 증가(growth={growth}, recent={recent_total})"
            )

        for row in tfidf_rows:
            keyword = str(row["keyword"])
            target = ensure(keyword)

            tfidf = float(row.get("tfidf", 0.0))
            points = tfidf * 5.0

            target["score"] = float(target["score"]) + points
            target["reasons"].append(f"TF-IDF {tfidf:.4f}")

        ranked = list(scores.values())
        ranked.sort(key=lambda row: float(row["score"]), reverse=True)

        for index, row in enumerate(ranked[:top_n], start=1):
            row["rank"] = index
            row["score"] = round(float(row["score"]), 4)

        return ranked[:top_n]
