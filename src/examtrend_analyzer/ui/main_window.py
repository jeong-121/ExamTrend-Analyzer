"""PySide6 main window."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QTabWidget,
)

from examtrend_analyzer.config.settings import APP_NAME, DEFAULT_REPORT_DIR
from examtrend_analyzer.core.models import AnalysisResult
from examtrend_analyzer.services.analysis_service import AnalysisService
from examtrend_analyzer.services.report_service import ReportService
from examtrend_analyzer.ui.dialogs.field_mapping_dialog import FieldMappingDialog
from examtrend_analyzer.ui.pages.analysis_page import AnalysisPage
from examtrend_analyzer.ui.pages.dashboard_page import DashboardPage
from examtrend_analyzer.ui.pages.report_page import ReportPage
from examtrend_analyzer.ui.workers import FunctionWorker


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self.analysis_service = AnalysisService()
        self.report_service = ReportService()
        self.thread_pool = QThreadPool.globalInstance()

        self.setWindowTitle(APP_NAME)
        self.resize(1200, 800)

        self.tabs = QTabWidget()
        self.dashboard_page = DashboardPage()
        self.analysis_page = AnalysisPage()
        self.report_page = ReportPage()

        self.tabs.addTab(self.dashboard_page, "대시보드")
        self.tabs.addTab(self.analysis_page, "분석")
        self.tabs.addTab(self.report_page, "보고서")

        self.setCentralWidget(self.tabs)
        self.setStatusBar(QStatusBar())

        self.dashboard_page.load_button.clicked.connect(self.load_file)
        self.dashboard_page.analyze_button.clicked.connect(self.run_analysis)
        self.report_page.save_button.clicked.connect(self.save_report)

    def load_file(self) -> None:
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "기출문제 파일 선택",
            "",
            (
                "지원 파일 (*.csv *.xlsx *.xls *.pdf *.txt);;"
                "PDF 파일 (*.pdf);;"
                "Excel 파일 (*.xlsx *.xls);;"
                "CSV 파일 (*.csv);;"
                "텍스트 파일 (*.txt);;"
                "전체 파일 (*.*)"
            ),
        )

        if not file_paths:
            return

        try:
            if len(file_paths) == 1:
                raw_data, suggested_mapping = self.analysis_service.preview_file(file_paths[0])
            else:
                raw_data, suggested_mapping = self.analysis_service.preview_files(file_paths)

            if self.analysis_service.can_auto_apply_mapping(suggested_mapping):
                data = self.analysis_service.auto_apply_mapping(suggested_mapping)
                mapping_status = "자동 매핑 적용 완료"
            else:
                dialog = FieldMappingDialog(
                    [str(column) for column in raw_data.columns],
                    suggested_mapping,
                    self,
                )

                if dialog.exec() != FieldMappingDialog.DialogCode.Accepted:
                    self.statusBar().showMessage("파일 로딩이 취소되었습니다.")
                    return

                missing = dialog.missing_required()
                if missing:
                    QMessageBox.warning(
                        self,
                        "필드 매핑 오류",
                        "필수 필드가 매핑되지 않았습니다: " + ", ".join(missing),
                    )
                    return

                data = self.analysis_service.apply_mapping(dialog.get_mapping())
                mapping_status = "수동 매핑 적용 완료"

            file_label = (
                file_paths[0]
                if len(file_paths) == 1
                else f"{len(file_paths)}개 파일 병합"
            )

            self.statusBar().showMessage(f"파일 로딩 완료: {len(data)}개 문항")
            self.dashboard_page.file_label.setText(f"현재 파일: {file_label}")
            self.dashboard_page.mapping_label.setText(f"필드 매핑: {mapping_status}")
            self.dashboard_page.row_card.set_value(len(data))

        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "파일 로딩 실패", str(exc))

    def run_analysis(self) -> None:
        if not self.analysis_service.has_data():
            QMessageBox.warning(
                self,
                "분석 불가",
                "분석할 데이터가 없습니다. 먼저 기출문제 파일을 불러오세요.",
            )
            return

        self.dashboard_page.set_loading_state(True)
        self.statusBar().showMessage("분석 실행 중...")

        worker = FunctionWorker(self.analysis_service.analyze_current)
        worker.signals.finished.connect(self._analysis_finished)
        worker.signals.failed.connect(self._task_failed)
        self.thread_pool.start(worker)

    def _analysis_finished(self, result: AnalysisResult) -> None:
        self.dashboard_page.set_loading_state(False)
        self.dashboard_page.update_result(result)
        self.analysis_page.update_result(result)
        self.report_page.update_result(result)
        self.tabs.setCurrentWidget(self.analysis_page)
        self.statusBar().showMessage("분석 완료")

    def _task_failed(self, message: str) -> None:
        self.dashboard_page.set_loading_state(False)
        self.statusBar().showMessage("작업 실패")
        QMessageBox.critical(self, "작업 실패", message)

    def save_report(self) -> None:
        result = self.analysis_service.last_result

        if result is None:
            QMessageBox.warning(
                self,
                "보고서 저장 불가",
                "먼저 분석을 실행하세요.",
            )
            return

        DEFAULT_REPORT_DIR.mkdir(exist_ok=True)
        default_path = DEFAULT_REPORT_DIR / "analysis_report.md"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "보고서 저장",
            str(default_path),
            "Markdown Files (*.md);;Text Files (*.txt);;All Files (*.*)",
        )

        if not file_path:
            return

        try:
            if hasattr(self.report_service, "save_markdown"):
                saved_path = self.report_service.save_markdown(result, Path(file_path))
            else:
                saved_path = self.report_service.create_markdown(result, Path(file_path))

            QMessageBox.information(
                self,
                "보고서 저장 완료",
                f"저장 위치: {saved_path}",
            )

        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "보고서 저장 실패", str(exc))


def run_app() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
