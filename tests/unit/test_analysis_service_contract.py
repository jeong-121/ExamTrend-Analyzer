from pathlib import Path

from examtrend_analyzer.core.schema import FieldMapping
from examtrend_analyzer.services.analysis_service import AnalysisService


def test_analysis_service_has_ui_required_methods():
    service = AnalysisService()

    assert hasattr(service, "preview_file")
    assert hasattr(service, "preview_files")
    assert hasattr(service, "can_auto_apply_mapping")
    assert hasattr(service, "auto_apply_mapping")


def test_preview_files_merges_and_maps(tmp_path):
    f1 = tmp_path / "2025년_1회_모의고사.csv"
    f2 = tmp_path / "2025년_2회_모의고사.csv"

    f1.write_text("question_text\nSQL의 기본 명령어는?\n", encoding="utf-8")
    f2.write_text("question_text\n정규화의 목적은?\n", encoding="utf-8")

    service = AnalysisService()
    df, mapping = service.preview_files([f1, f2])

    assert len(df) == 2
    assert "year" in df.columns
    assert "exam_round" in df.columns
    assert isinstance(mapping, FieldMapping)
    assert service.can_auto_apply_mapping(mapping)
