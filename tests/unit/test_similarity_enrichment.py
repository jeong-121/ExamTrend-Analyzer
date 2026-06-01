import pandas as pd

from examtrend_analyzer.services.analysis_service import AnalysisService


def test_similar_pairs_include_question_text_and_source():
    df = pd.DataFrame({
        "question_text": [
            "SQL의 기본 명령어에 대한 설명으로 옳은 것은?",
            "SQL의 기본 명령어에 대한 설명으로 옳은 것은?",
        ],
        "source_file": ["2025_1.pdf", "2025_2.pdf"],
        "question_no": [1, 2],
    })

    result = AnalysisService().run_analysis(df)

    assert result.similar_pairs
    first = result.similar_pairs[0]
    assert "question_1_text" in first
    assert "question_2_text" in first
    assert "question_1_source" in first
    assert "question_2_source" in first
