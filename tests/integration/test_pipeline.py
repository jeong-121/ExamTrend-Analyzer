import pandas as pd
from examtrend_analyzer.core.pipeline import AnalysisPipeline

def test_pipeline_runs_with_valid_data():
    data = pd.DataFrame({
        "year": [2024, 2025],
        "chapter": ["DB", "AI"],
        "question_type": ["객관식", "서술형"],
        "difficulty": ["중", "상"],
        "question_text": ["데이터베이스 키 설명", "인공지능 학습 설명"],
        "answer": ["키", "학습"],
    })
    result = AnalysisPipeline().run(data)
    assert result.summary.row_count == 2
    assert result.keyword_counts
