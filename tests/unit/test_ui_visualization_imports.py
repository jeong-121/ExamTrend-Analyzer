def test_visualization_widgets_importable():
    from examtrend_analyzer.ui.widgets.chart_canvas import AnalysisChartsWidget, ChartCanvas

    assert ChartCanvas is not None
    assert AnalysisChartsWidget is not None


def test_analysis_page_importable():
    from examtrend_analyzer.ui.pages.analysis_page import AnalysisPage

    assert AnalysisPage is not None
