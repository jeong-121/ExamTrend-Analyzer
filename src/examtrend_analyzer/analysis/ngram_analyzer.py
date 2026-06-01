"""N-gram keyword analysis."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from examtrend_analyzer.preprocessing.tokenizer import KoreanTokenizer


@dataclass
class NgramAnalyzer:
    tokenizer: KoreanTokenizer | None = None

    def __post_init__(self) -> None:
        if self.tokenizer is None:
            self.tokenizer = KoreanTokenizer()

    def analyze(self, texts: Iterable[object], n: int = 2, top_n: int = 30) -> dict[str, int]:
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")

        counter: Counter[str] = Counter()
        for text in texts:
            tokens = self.tokenizer.tokenize(text)
            grams = [" ".join(tokens[i:i+n]) for i in range(0, max(len(tokens)-n+1, 0))]
            counter.update(grams)
        return dict(counter.most_common(top_n))
