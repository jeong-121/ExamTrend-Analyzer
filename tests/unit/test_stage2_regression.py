from pathlib import Path

import pandas as pd

from examtrend_analyzer.services.analysis_service import AnalysisService


def test_analysis_service_keeps_preview_file_api(tmp_path: Path):
    csv_path = tmp_path / "questions.csv"
    pd.DataFrame({
        "연도": [2024],
        "단원": ["DB"],
        "문제유형": ["서술형"],
        "난이도": ["중"],
        "문제": ["SQL의 기본 명령어를 설명하시오."],
        "정답": ["DDL, DML"],
    }).to_csv(csv_path, index=False, encoding="utf-8-sig")

    service = AnalysisService()
    raw, suggested = service.preview_file(csv_path)
    assert len(raw) == 1
    assert suggested.mapping["문제"] == "question_text"
    service.apply_mapping(suggested.mapping)
    result = service.analyze_current()
    assert result.summary.row_count == 1
    assert "SQL" in result.keyword_counts
    assert isinstance(result.tfidf, list)
