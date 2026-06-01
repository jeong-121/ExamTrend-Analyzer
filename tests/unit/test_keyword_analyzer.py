"""Unit tests for KeywordAnalyzer."""

from examtrend_analyzer.analysis.keyword_analyzer import KeywordAnalyzer


def test_analyze_keyword_frequency() -> None:
    analyzer = KeywordAnalyzer()
    result = analyzer.analyze(["SQL", "정규화", "SQL"])

    assert result["SQL"] == 2
    assert result["정규화"] == 1


def test_top_n_keywords() -> None:
    analyzer = KeywordAnalyzer()
    result = analyzer.top_n(["SQL", "정규화", "SQL", "트랜잭션"], n=1)

    assert result == [("SQL", 2)]


def test_stopwords_and_single_character_tokens_are_removed() -> None:
    analyzer = KeywordAnalyzer()
    result = analyzer.analyze(["은", "의", "에", "ㄴ", "SQL", "정규화"])

    assert "은" not in result
    assert "의" not in result
    assert "에" not in result
    assert "ㄴ" not in result
    assert result == {"SQL": 1, "정규화": 1}
