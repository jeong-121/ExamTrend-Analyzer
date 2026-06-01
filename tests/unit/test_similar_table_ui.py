def test_analysis_page_has_similar_table_configuration_method():
    from examtrend_analyzer.ui.pages.analysis_page import AnalysisPage

    assert hasattr(AnalysisPage, "_configure_similar_table")
    assert hasattr(AnalysisPage, "_apply_similar_table_column_widths")
    assert hasattr(AnalysisPage, "_update_similar_table")
