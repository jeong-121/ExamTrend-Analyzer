"""PySide6 main window for ExamTrend Analyzer."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QToolBar,
)

from examtrend_analyzer.services import AnalysisResult, AnalysisService, ReportService
from examtrend_analyzer.ui.pages import AnalysisPage, DashboardPage, ReportPage
from examtrend_analyzer.utils.file_loader import FileLoader


class MainWindow(QMainWindow):
    """Main PySide6 window for the analysis workflow."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ExamTrend Analyzer")
        self.resize(1100, 760)

        self.file_loader = FileLoader()
        self.analysis_service = AnalysisService()
        self.report_service = ReportService()
        self.current_data: pd.DataFrame | None = None
        self.current_result: AnalysisResult | None = None

        self.stack = QStackedWidget()
        self.dashboard_page = DashboardPage()
        self.analysis_page = AnalysisPage()
        self.report_page = ReportPage()
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.analysis_page)
        self.stack.addWidget(self.report_page)
        self.setCentralWidget(self.stack)

        self._setup_toolbar()
        self.statusBar().showMessage("CSV 또는 Excel 파일을 불러오세요.")

    def _setup_toolbar(self) -> None:
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        load_action = toolbar.addAction("파일 불러오기")
        load_action.triggered.connect(self.load_file)

        analyze_action = toolbar.addAction("분석 실행")
        analyze_action.triggered.connect(self.run_analysis)

        toolbar.addSeparator()

        dashboard_action = toolbar.addAction("대시보드")
        dashboard_action.triggered.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))

        analysis_action = toolbar.addAction("분석 결과")
        analysis_action.triggered.connect(lambda: self.stack.setCurrentWidget(self.analysis_page))

        report_action = toolbar.addAction("보고서")
        report_action.triggered.connect(lambda: self.stack.setCurrentWidget(self.report_page))

        toolbar.addSeparator()

        save_report_action = toolbar.addAction("보고서 저장")
        save_report_action.triggered.connect(self.save_report)

    def load_file(self) -> None:
        """Load CSV or Excel data into the dashboard."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "기출문제 데이터 불러오기",
            "",
            "Data Files (*.csv *.xlsx *.xls);;CSV Files (*.csv);;Excel Files (*.xlsx *.xls)",
        )
        if not file_path:
            return

        path = Path(file_path)
        try:
            if path.suffix.lower() == ".csv":
                data = self.file_loader.load_csv(path)
            elif path.suffix.lower() in {".xlsx", ".xls"}:
                data = self.file_loader.load_excel(path)
            else:
                raise ValueError("지원하지 않는 파일 형식입니다.")
        except Exception as exc:  # noqa: BLE001 - UI boundary should show any load error.
            QMessageBox.critical(self, "파일 로딩 실패", str(exc))
            return

        self.current_data = data
        self.current_result = None
        self.dashboard_page.set_dataset(path.name, data)
        self.stack.setCurrentWidget(self.dashboard_page)
        self.statusBar().showMessage(f"파일 로딩 완료: {path.name}")

    def run_analysis(self) -> None:
        """Run analysis for the loaded dataset."""
        if self.current_data is None:
            QMessageBox.information(self, "분석 불가", "먼저 CSV 또는 Excel 파일을 불러오세요.")
            return

        try:
            result = self.analysis_service.analyze(self.current_data)
        except Exception as exc:  # noqa: BLE001 - UI boundary should show any analysis error.
            QMessageBox.critical(self, "분석 실패", str(exc))
            return

        self.current_result = result
        self.analysis_page.set_result(result)
        report = self.report_service.build_markdown(result)
        self.report_page.set_report(report)
        self.stack.setCurrentWidget(self.analysis_page)
        self.statusBar().showMessage("분석 완료")

    def save_report(self) -> None:
        """Save the current report as markdown."""
        if self.current_result is None:
            QMessageBox.information(self, "저장 불가", "먼저 분석을 실행하세요.")
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "보고서 저장",
            "reports/examtrend_report.md",
            "Markdown Files (*.md);;Text Files (*.txt)",
        )
        if not output_path:
            return

        try:
            saved_path = self.report_service.save_markdown(self.current_result, output_path)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "보고서 저장 실패", str(exc))
            return

        self.statusBar().showMessage(f"보고서 저장 완료: {saved_path}")
        QMessageBox.information(self, "저장 완료", f"보고서를 저장했습니다.\n{saved_path}")


def run_app() -> None:
    """Run the PySide6 application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
