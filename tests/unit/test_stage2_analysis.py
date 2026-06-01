import pandas as pd

from examtrend_analyzer.services.analysis_service import AnalysisService
from examtrend_analyzer.preprocessing.tokenizer import KoreanTokenizer


def test_tokenizer_removes_particles_and_one_char_tokens():
    tokenizer = KoreanTokenizer(use_kiwi=False)
    tokens = tokenizer.tokenize("SQL의 기본 명령어에 대한 설명")
    assert "SQL" in tokens
    assert "의" not in tokens
    assert "에" not in tokens
    assert "대한" not in tokens


def test_stage2_analysis_outputs_tfidf_and_ngrams():
    df = pd.DataFrame({
        "question_text": [
            "SQL 기본 명령어를 설명하시오.",
            "SQL 조인과 인덱스를 설명하시오.",
            "정규화와 함수 종속성을 설명하시오.",
        ]
    })
    result = AnalysisService().run_analysis(df)
    assert result["question_count"] == 3
    assert result["keywords"]
    assert "tfidf" in result
    assert "bigrams" in result
    assert isinstance(result["similar_pairs"], list)
