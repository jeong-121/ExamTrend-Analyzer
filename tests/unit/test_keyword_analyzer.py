"""Unit tests for KeywordAnalyzer."""

from examtrend_analyzer.analysis.keyword_analyzer import KeywordAnalyzer


def test_analyze_keyword_frequency() -> None:
    analyzer = KeywordAnalyzer()
    result = analyzer.analyze(["SQL", "정규화", "SQL"])

    assert result["SQL"] == 2
    assert result["정규화"] == 1


def test_top_n_keywords() -> None:
    analyzer = KeywordAnalyzer()
    result = analyzer.top_n(["A", "B", "A", "C"], n=1)

    assert result == [("A", 2)]
