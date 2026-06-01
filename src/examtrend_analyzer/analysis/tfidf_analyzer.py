"""TF-IDF based keyword scoring."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from examtrend_analyzer.preprocessing.tokenizer import KoreanTokenizer


@dataclass
class TfidfAnalyzer:
    tokenizer: KoreanTokenizer | None = None

    def __post_init__(self) -> None:
        if self.tokenizer is None:
            self.tokenizer = KoreanTokenizer()

    def analyze(self, texts: Iterable[object], top_n: int = 30) -> list[dict[str, object]]:
        documents = [" ".join(self.tokenizer.tokenize(text)) for text in texts]
        documents = [doc for doc in documents if doc.strip()]
        if not documents:
            return []

        vectorizer = TfidfVectorizer(token_pattern=None, tokenizer=str.split, lowercase=False)
        matrix = vectorizer.fit_transform(documents)
        scores = matrix.mean(axis=0).A1
        terms = vectorizer.get_feature_names_out()

        rows = [
            {"keyword": term, "tfidf": float(score)}
            for term, score in zip(terms, scores)
        ]
        rows.sort(key=lambda row: row["tfidf"], reverse=True)
        return rows[:top_n]
