import pandas as pd

from examtrend_analyzer.services.analysis_service import AnalysisService


def test_same_source_same_question_number_is_filtered():
    df = pd.DataFrame({
        "question_text": [
            "SQL의 기본 명령어에 대한 설명으로 옳은 것은?",
            "SQL의 기본 명령어에 대한 설명으로 옳은 것은?",
            "정규화의 목적에 대한 설명으로 옳은 것은?",
        ],
        "source_file": ["2025_1.pdf", "2025_1.pdf", "2025_2.pdf"],
        "question_no": [30, 30, 31],
    })

    result = AnalysisService().run_analysis(df)

    for row in result.similar_pairs:
        assert not (
            row.get("question_1_source", "").startswith("2025_1.pdf")
            and row.get("question_2_source", "").startswith("2025_1.pdf")
            and "30번" in row.get("question_1_source", "")
            and "30번" in row.get("question_2_source", "")
        )


def test_different_source_same_text_can_remain():
    df = pd.DataFrame({
        "question_text": [
            "SQL의 기본 명령어에 대한 설명으로 옳은 것은?",
            "SQL의 기본 명령어에 대한 설명으로 옳은 것은?",
        ],
        "source_file": ["2025_1.pdf", "2025_2.pdf"],
        "question_no": [30, 30],
    })

    result = AnalysisService().run_analysis(df)

    assert result.similar_pairs
