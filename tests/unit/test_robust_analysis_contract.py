import pandas as pd

from examtrend_analyzer.services.analysis_service import AnalysisService


def test_keyword_analysis_runs_without_year_or_chapter():
    df = pd.DataFrame({
        "question_text": [
            "SQL의 기본 명령어에 대한 설명으로 옳은 것은?",
            "정규화의 목적에 대한 설명으로 옳은 것은?",
        ]
    })

    result = AnalysisService().run_analysis(df)

    assert result.keyword_counts
    assert result.yearly_counts == {}
    assert "yearly_trend" in getattr(result, "analysis_status", {})
    assert result.chapter_counts


def test_auto_chapter_classification_for_database_questions():
    df = pd.DataFrame({
        "question_text": [
            "SQL과 트랜잭션 ACID 특성에 대한 설명으로 옳은 것은?",
            "정규화와 기본키 외래키에 대한 설명으로 옳은 것은?",
        ]
    })

    result = AnalysisService().run_analysis(df)

    assert "데이터베이스" in result.chapter_counts
    assert getattr(result, "chapter_source", "") == "keyword_auto"
