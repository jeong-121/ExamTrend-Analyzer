from pathlib import Path

from examtrend_analyzer.services.analysis_service import AnalysisService
from examtrend_analyzer.utils.filename_metadata import extract_metadata_from_filename


def test_extract_metadata_from_filename():
    metadata = extract_metadata_from_filename("2025년_3회_모의고사.pdf")
    assert metadata.year == 2025
    assert metadata.exam_round == 3
    assert metadata.source_file == "2025년_3회_모의고사.pdf"


def test_preview_files_merges_multiple_csv_files(tmp_path):
    file1 = tmp_path / "2024년_1회_모의고사.csv"
    file2 = tmp_path / "2025년_2회_모의고사.csv"

    file1.write_text("question_text\nSQL의 기본 명령어는?\n", encoding="utf-8")
    file2.write_text("question_text\n정규화의 목적은?\n", encoding="utf-8")

    service = AnalysisService()
    df, mapping = service.preview_files([file1, file2])

    assert len(df) == 2
    assert "year" in df.columns
    assert "exam_round" in df.columns
    assert sorted(df["year"].dropna().astype(int).tolist()) == [2024, 2025]
    assert service.can_auto_apply_mapping(mapping)
