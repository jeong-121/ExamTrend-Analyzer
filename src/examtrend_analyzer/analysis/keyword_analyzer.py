"""Keyword frequency analysis."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from examtrend_analyzer.preprocessing.tokenizer import KoreanTokenizer


@dataclass
class KeywordAnalyzer:
    tokenizer: KoreanTokenizer | None = None

    def __post_init__(self) -> None:
        if self.tokenizer is None:
            self.tokenizer = KoreanTokenizer()

    def top_n(self, tokens: Iterable[object], n: int = 10) -> list[tuple[str, int]]:
        counter: Counter[str] = Counter(str(token) for token in tokens if str(token).strip())
        return counter.most_common(n)

    def analyze(self, texts: Iterable[object], top_n: int = 30) -> dict[str, int]:
        counter: Counter[str] = Counter()
        for text in texts:
            counter.update(self.tokenizer.tokenize(text))
        return dict(counter.most_common(top_n))

    def analyze_with_document_frequency(self, texts: Iterable[object], top_n: int = 30) -> list[dict[str, object]]:
        frequency: Counter[str] = Counter()
        document_frequency: Counter[str] = Counter()
        for text in texts:
            tokens = self.tokenizer.tokenize(text)
            frequency.update(tokens)
            document_frequency.update(set(tokens))

        rows = []
        for keyword, count in frequency.most_common(top_n):
            rows.append({
                "keyword": keyword,
                "frequency": count,
                "document_frequency": document_frequency[keyword],
            })
        return rows
