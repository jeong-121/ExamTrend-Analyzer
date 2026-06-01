"""End-to-end analysis pipeline."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from examtrend_analyzer.analysis.difficulty_analyzer import DifficultyAnalyzer
from examtrend_analyzer.analysis.keyword_analyzer import KeywordAnalyzer
from examtrend_analyzer.analysis.ngram_analyzer import NgramAnalyzer
from examtrend_analyzer.analysis.similarity_analyzer import SimilarityAnalyzer
from examtrend_analyzer.analysis.tfidf_analyzer import TfidfAnalyzer
from examtrend_analyzer.analysis.trend_analyzer import TrendAnalyzer
from examtrend_analyzer.core.models import AnalysisResult, DatasetSummary
from examtrend_analyzer.core.validation import DatasetValidator
from examtrend_analyzer.preprocessing.text_cleaner import TextCleaner
from examtrend_analyzer.preprocessing.tokenizer import KoreanTokenizer


class AnalysisPipeline:
    """Coordinates validation, preprocessing, analysis, and result packing."""

    def __init__(self) -> None:
        self.validator = DatasetValidator()
        self.cleaner = TextCleaner()
        self.tokenizer = KoreanTokenizer()
        self.keyword_analyzer = KeywordAnalyzer(self.tokenizer)
        self.ngram_analyzer = NgramAnalyzer(self.tokenizer)
        self.tfidf_analyzer = TfidfAnalyzer(self.tokenizer)
        self.similarity_analyzer = SimilarityAnalyzer(self.tokenizer)
        self.trend_analyzer = TrendAnalyzer()
        self.difficulty_analyzer = DifficultyAnalyzer()

    def run(self, data: pd.DataFrame, file_path: str | Path | None = None) -> AnalysisResult:
        issues = self.validator.validate(data)
        fatal = any(issue.level == "error" for issue in issues)
        summary = self._summarize(data, Path(file_path) if file_path else None)
        if fatal:
            return AnalysisResult(summary, {}, {}, {}, {}, {}, issues)

        if "question_text" not in data.columns:
            raise ValueError("question_text 컬럼이 없습니다. 필드 매핑을 확인하세요.")

        texts = data["question_text"].fillna("").astype(str).tolist()
        cleaned_texts = self.cleaner.clean_many(texts)

        keyword_counts = self.keyword_analyzer.analyze(cleaned_texts, top_n=30)
        keyword_rows = self.keyword_analyzer.analyze_with_document_frequency(cleaned_texts, top_n=30)
        bigrams = self.ngram_analyzer.analyze(cleaned_texts, n=2, top_n=30)
        trigrams = self.ngram_analyzer.analyze(cleaned_texts, n=3, top_n=30)
        tfidf = self.tfidf_analyzer.analyze(cleaned_texts, top_n=30)
        similar_pairs = self.similarity_analyzer.find_similar_pairs(cleaned_texts, threshold=0.55, max_pairs=50)

        return AnalysisResult(
            summary=summary,
            keyword_counts=keyword_counts,
            yearly_counts=self._safe_series_to_dict(self.trend_analyzer.count_by_year(data)),
            chapter_counts=self._safe_series_to_dict(self.trend_analyzer.count_by_chapter(data)),
            difficulty_counts=self._safe_series_to_dict(self.difficulty_analyzer.count_by_difficulty(data)),
            average_difficulty_by_year=self._safe_series_to_dict(
                self.difficulty_analyzer.average_difficulty_by_year(data).dropna()
            ),
            issues=issues,
            keyword_rows=keyword_rows,
            bigrams=bigrams,
            trigrams=trigrams,
            tfidf=tfidf,
            similar_pairs=similar_pairs,
        )

    def _summarize(self, data: pd.DataFrame, file_path: Path | None) -> DatasetSummary:
        years = []
        if "year" in data.columns:
            years = sorted(pd.to_numeric(data["year"], errors="coerce").dropna().astype(int).unique().tolist())
        chapters = sorted(data["chapter"].dropna().astype(str).unique().tolist()) if "chapter" in data.columns else []
        difficulties = sorted(data["difficulty"].dropna().astype(str).unique().tolist()) if "difficulty" in data.columns else []
        return DatasetSummary(
            file_path=file_path,
            row_count=len(data),
            column_count=len(data.columns),
            years=years,
            chapters=chapters,
            difficulties=difficulties,
        )

    def _safe_series_to_dict(self, series: pd.Series) -> dict:
        if series is None or series.empty:
            return {}
        return series.to_dict()
