"""Generic topic analyzer for arbitrary exam datasets.

This module intentionally does not use a fixed subject/chapter dictionary.
It derives broad topic groups from the vocabulary that appears in the
loaded questions, so it can be used for different exams and subjects.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field

from examtrend_analyzer.preprocessing.tokenizer import KoreanTokenizer


@dataclass
class TopicAnalyzer:
    """Create generic topic groups from question text.

    The analyzer works as follows:

    1. tokenize all question texts
    2. select representative global keywords
    3. split keywords into a fixed number of topic groups
    4. assign each question to the topic group with the largest keyword overlap

    Topic names are intentionally generic, for example:
    "주제 1: SQL, 정규화, 트랜잭션"
    """

    topic_count: int = 8
    keywords_per_topic: int = 5
    max_keywords: int = 80
    tokenizer: KoreanTokenizer | None = None
    stopwords: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        if self.tokenizer is None:
            self.tokenizer = KoreanTokenizer()

    def analyze(self, texts: list[str]) -> dict[str, object]:
        normalized_texts = ["" if text is None else str(text) for text in texts]
        token_rows = [self._tokens(text) for text in normalized_texts]

        keyword_counts: Counter[str] = Counter()
        for tokens in token_rows:
            keyword_counts.update(tokens)

        top_keywords = [
            keyword
            for keyword, _ in keyword_counts.most_common(self.max_keywords)
            if keyword.strip()
        ]

        topic_defs = self._build_topics(top_keywords)
        assignments = [
            self._assign_topic(tokens, topic_defs)
            for tokens in token_rows
        ]

        counts = Counter(assignments)
        total = len(assignments)

        distribution = [
            {
                "topic": topic,
                "count": int(count),
                "ratio": round((int(count) / total) * 100, 2) if total else 0.0,
            }
            for topic, count in counts.most_common()
        ]

        topic_keywords = [
            {
                "topic": topic,
                "keywords": keywords,
            }
            for topic, keywords in topic_defs.items()
        ]

        return {
            "assignments": assignments,
            "counts": {topic: int(count) for topic, count in counts.items()},
            "distribution": distribution,
            "topic_keywords": topic_keywords,
        }

    def _tokens(self, text: str) -> list[str]:
        tokens = self.tokenizer.tokenize(text)
        return [
            token
            for token in tokens
            if len(token) >= 2 and token not in self.stopwords
        ]

    def _build_topics(self, keywords: list[str]) -> dict[str, list[str]]:
        if not keywords:
            return {"미분류": []}

        actual_topic_count = min(self.topic_count, max(1, len(keywords)))

        buckets: list[list[str]] = [[] for _ in range(actual_topic_count)]
        for index, keyword in enumerate(keywords):
            buckets[index % actual_topic_count].append(keyword)

        topics: dict[str, list[str]] = {}
        for index, bucket in enumerate(buckets, start=1):
            selected = bucket[: self.keywords_per_topic]
            label_keywords = ", ".join(selected[:3]) if selected else "미분류"
            topic_name = f"주제 {index}: {label_keywords}"
            topics[topic_name] = selected

        return topics

    def _assign_topic(
        self,
        tokens: list[str],
        topic_defs: dict[str, list[str]],
    ) -> str:
        if not topic_defs:
            return "미분류"

        token_set = set(tokens)
        scores: dict[str, int] = {}

        for topic, keywords in topic_defs.items():
            scores[topic] = len(token_set.intersection(keywords))

        best_topic, best_score = max(scores.items(), key=lambda item: item[1])

        if best_score <= 0:
            return "미분류"

        return best_topic
