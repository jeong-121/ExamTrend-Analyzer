def test_dashboard_db_buttons_removed():
    from examtrend_analyzer.ui.pages.dashboard_page import DashboardPage

    assert not hasattr(DashboardPage, "save_db_button")
    assert not hasattr(DashboardPage, "reload_result_button")


def test_main_window_db_methods_removed():
    from examtrend_analyzer.ui.main_window import MainWindow

    assert not hasattr(MainWindow, "save_to_database")
    assert not hasattr(MainWindow, "load_saved_result")
