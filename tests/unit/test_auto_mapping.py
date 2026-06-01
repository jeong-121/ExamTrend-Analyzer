import pandas as pd

from examtrend_analyzer.core.schema import suggest_field_mapping
from examtrend_analyzer.services.analysis_service import AnalysisService


def test_auto_mapping_accepts_pdf_columns():
    mapping = suggest_field_mapping([
        "question_no",
        "question_text",
        "source_page",
        "source_file",
        "source_type",
    ])
    assert mapping.mapping["question_text"] == "question_text"
    assert AnalysisService().can_auto_apply_mapping(mapping)


def test_auto_mapping_accepts_korean_excel_question_column(tmp_path):
    path = tmp_path / "questions.csv"
    path.write_text("문제\nSQL의 기본 명령어는?\n", encoding="utf-8")

    service = AnalysisService()
    df, mapping = service.preview_file(path)

    assert service.can_auto_apply_mapping(mapping)
    mapped_df = service.auto_apply_mapping(mapping)
    assert "question_text" in mapped_df.columns
