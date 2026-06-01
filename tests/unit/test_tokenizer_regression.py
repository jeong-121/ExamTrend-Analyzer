from examtrend_analyzer.preprocessing.tokenizer import KoreanTokenizer


def test_regex_tokenizer_removes_common_particles_and_exam_words():
    tokenizer = KoreanTokenizer(use_kiwi=False)
    tokens = tokenizer.tokenize("SQL의 기본 명령어에 대한 설명으로 옳은 것은?")
    assert "SQL" in tokens
    assert "명령어" in tokens
    assert "의" not in tokens
    assert "에" not in tokens
    assert "대한" not in tokens
    assert "설명으로" not in tokens
    assert "것은" not in tokens
