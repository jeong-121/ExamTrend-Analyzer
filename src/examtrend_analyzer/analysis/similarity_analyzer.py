"""Similar question detection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from examtrend_analyzer.preprocessing.tokenizer import KoreanTokenizer


@dataclass
class SimilarityAnalyzer:
    tokenizer: KoreanTokenizer | None = None

    def __post_init__(self) -> None:
        if self.tokenizer is None:
            self.tokenizer = KoreanTokenizer()

    def find_similar_pairs(
        self,
        texts: Iterable[object],
        threshold: float = 0.55,
        max_pairs: int = 50,
    ) -> list[dict[str, object]]:
        raw_texts = ["" if text is None else str(text) for text in texts]
        documents = [" ".join(self.tokenizer.tokenize(text)) for text in raw_texts]
        valid_indices = [i for i, doc in enumerate(documents) if doc.strip()]
        if len(valid_indices) < 2:
            return []

        valid_documents = [documents[i] for i in valid_indices]
        vectorizer = TfidfVectorizer(token_pattern=None, tokenizer=str.split, lowercase=False)
        matrix = vectorizer.fit_transform(valid_documents)
        sim = cosine_similarity(matrix)

        pairs: list[dict[str, object]] = []
        for a in range(len(valid_indices)):
            for b in range(a + 1, len(valid_indices)):
                score = float(sim[a, b])
                if score >= threshold:
                    pairs.append({
                        "question_index_1": valid_indices[a],
                        "question_index_2": valid_indices[b],
                        "similarity": round(score, 4),
                        "question_1": raw_texts[valid_indices[a]],
                        "question_2": raw_texts[valid_indices[b]],
                    })

        pairs.sort(key=lambda row: row["similarity"], reverse=True)
        return pairs[:max_pairs]
