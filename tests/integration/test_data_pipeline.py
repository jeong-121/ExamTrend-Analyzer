"""Integration test for loading, cleaning, tokenizing and analyzing data."""

from examtrend_analyzer.analysis.keyword_analyzer import KeywordAnalyzer
from examtrend_analyzer.preprocessing.stopwords import remove_stopwords
from examtrend_analyzer.preprocessing.text_cleaner import TextCleaner


def test_simple_analysis_pipeline() -> None:
    cleaner = TextCleaner()
    analyzer = KeywordAnalyzer()

    text = cleaner.clean("데이터베이스 정규화에 대한 설명으로 옳은 것은?")
    tokens = text.split()
    tokens = remove_stopwords(tokens)
    result = analyzer.analyze(tokens)

    assert "데이터베이스" in result
