import pandas as pd

from examtrend_analyzer.core.models import AnalysisResult
from examtrend_analyzer.services.analysis_service import AnalysisService


def test_analysis_service_returns_ui_compatible_result():
    df = pd.DataFrame({
        "year": [2024, 2025],
        "chapter": ["DB", "DB"],
        "question_type": ["객관식", "객관식"],
        "difficulty": [2, 3],
        "question_text": ["SQL의 기본 명령어는?", "정규화의 목적은?"],
        "answer": ["1", "2"],
    })

    result = AnalysisService().run_analysis(df)

    assert isinstance(result, AnalysisResult)
    assert result.summary.row_count == 2
    assert result.keyword_counts
    assert isinstance(result.issues, list)
    assert hasattr(result, "bigrams")
    assert hasattr(result, "tfidf")
