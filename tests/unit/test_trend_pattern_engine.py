import pandas as pd

from examtrend_analyzer.services.analysis_service import AnalysisService


def test_trend_pattern_engine_outputs_expected_sections():
    df = pd.DataFrame({
        "year": [2021, 2022, 2023, 2024, 2024],
        "chapter": ["DB", "DB", "OS", "DB", "OS"],
        "question_text": [
            "SQL 정규화 트랜잭션",
            "SQL 정규화 인덱스",
            "프로세스 스케줄링",
            "SQL 트랜잭션 정규화",
            "프로세스 스케줄링 알고리즘",
        ],
    })

    result = AnalysisService().run_analysis(df)

    assert result.yearly_counts
    assert result.chapter_distribution
    assert result.yearly_keyword_trends
    assert result.repeated_patterns
    assert result.prediction_candidates
    assert result.difficulty_counts == {}
    assert result.average_difficulty_by_year == {}
