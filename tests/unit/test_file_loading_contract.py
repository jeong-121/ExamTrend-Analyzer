import pandas as pd
import pytest

from examtrend_analyzer.core.schema import FieldMapping
from examtrend_analyzer.services.analysis_service import AnalysisService


def test_preview_file_contract_returns_dataframe_and_mapping(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("question_text\nSQL의 기본 명령어는?\n", encoding="utf-8")

    df, suggested = AnalysisService().preview_file(csv_path)

    assert isinstance(df, pd.DataFrame)
    assert isinstance(suggested, FieldMapping)
    assert suggested.mapping["question_text"] == "question_text"


def test_analyze_current_without_data_raises_clear_error():
    service = AnalysisService()

    with pytest.raises(ValueError, match="먼저 기출문제 파일"):
        service.analyze_current()
