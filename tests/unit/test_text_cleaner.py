"""Unit tests for TextCleaner."""

from examtrend_analyzer.preprocessing.text_cleaner import TextCleaner


def test_clean_removes_special_characters() -> None:
    cleaner = TextCleaner()
    result = cleaner.clean(" SQL의   기본 명령어는? ")

    assert result == "SQL의 기본 명령어는"


def test_clean_many() -> None:
    cleaner = TextCleaner()
    result = cleaner.clean_many([" A!! ", " B?? "])

    assert result == ["A", "B"]
