"""High-level analysis workflow for exam question data."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from examtrend_analyzer.analysis.difficulty_analyzer import DifficultyAnalyzer
from examtrend_analyzer.analysis.keyword_analyzer import KeywordAnalyzer
from examtrend_analyzer.analysis.pattern_analyzer import PatternAnalyzer
from examtrend_analyzer.analysis.trend_analyzer import TrendAnalyzer
from examtrend_analyzer.preprocessing.stopwords import remove_stopwords
from examtrend_analyzer.preprocessing.text_cleaner import TextCleaner
from examtrend_analyzer.preprocessing.tokenizer import KoreanTokenizer


REQUIRED_COLUMNS = ["year", "chapter", "question_type", "difficulty", "question_text", "answer"]


@dataclass(slots=True)
class AnalysisResult:
    """Container for all calculated analysis outputs."""

    row_count: int
    keyword_top: list[tuple[str, int]] = field(default_factory=list)
    year_counts: pd.Series = field(default_factory=pd.Series)
    chapter_counts: pd.Series = field(default_factory=pd.Series)
    chapter_ratio: pd.Series = field(default_factory=pd.Series)
    difficulty_counts: pd.Series = field(default_factory=pd.Series)
    difficulty_by_year: pd.Series = field(default_factory=pd.Series)
    question_type_counts: pd.Series = field(default_factory=pd.Series)


class AnalysisService:
    """Coordinates preprocessing and analyzer classes for the UI layer."""

    def __init__(self) -> None:
        self.cleaner = TextCleaner()
        self.tokenizer = KoreanTokenizer()
        self.keyword_analyzer = KeywordAnalyzer()
        self.trend_analyzer = TrendAnalyzer()
        self.difficulty_analyzer = DifficultyAnalyzer()
        self.pattern_analyzer = PatternAnalyzer()

    def validate(self, data: pd.DataFrame) -> list[str]:
        """Return missing required columns."""
        return [column for column in REQUIRED_COLUMNS if column not in data.columns]

    def analyze(self, data: pd.DataFrame, top_n: int = 20) -> AnalysisResult:
        """Run the full analysis pipeline."""
        missing = self.validate(data)
        if missing:
            raise ValueError(f"필수 컬럼이 없습니다: {', '.join(missing)}")

        normalized = data.copy()
        normalized["question_text"] = normalized["question_text"].fillna("").astype(str)
        cleaned_texts = self.cleaner.clean_many(normalized["question_text"].tolist())
        tokenized_questions = self.tokenizer.tokenize_many(cleaned_texts)
        tokens = [token for question_tokens in tokenized_questions for token in question_tokens]
        tokens = remove_stopwords(tokens)

        return AnalysisResult(
            row_count=len(normalized),
            keyword_top=self.keyword_analyzer.top_n(tokens, top_n),
            year_counts=self.trend_analyzer.count_by_year(normalized),
            chapter_counts=self.trend_analyzer.count_by_chapter(normalized),
            chapter_ratio=self.trend_analyzer.chapter_ratio(normalized),
            difficulty_counts=self.difficulty_analyzer.count_by_difficulty(normalized),
            difficulty_by_year=self.difficulty_analyzer.average_difficulty_by_year(normalized),
            question_type_counts=self.pattern_analyzer.find_repeated_question_types(normalized),
        )
