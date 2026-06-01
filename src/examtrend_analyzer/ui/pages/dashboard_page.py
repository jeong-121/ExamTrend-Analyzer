"""Dashboard page."""

from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from examtrend_analyzer.core.models import AnalysisResult
from examtrend_analyzer.ui.widgets.summary_card import SummaryCard


class DashboardPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.load_button = QPushButton("기출문제 파일 불러오기")
        self.analyze_button = QPushButton("분석 실행")

        self.file_label = QLabel("현재 파일: 없음")
        self.mapping_label = QLabel("필드 매핑: 미적용")

        self.row_card = SummaryCard("문항 수")
        self.year_card = SummaryCard("연도 범위")
        self.chapter_card = SummaryCard("단원 수")
        self.issue_card = SummaryCard("검증 이슈")

        grid = QGridLayout()
        grid.addWidget(self.row_card, 0, 0)
        grid.addWidget(self.year_card, 0, 1)
        grid.addWidget(self.chapter_card, 1, 0)
        grid.addWidget(self.issue_card, 1, 1)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("대시보드"))
        layout.addWidget(self.file_label)
        layout.addWidget(self.mapping_label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.analyze_button)
        layout.addLayout(grid)
        layout.addStretch()

    def set_loading_state(self, running: bool) -> None:
        self.load_button.setEnabled(not running)
        self.analyze_button.setEnabled(not running)

    def update_result(self, result: AnalysisResult) -> None:
        if result.summary.file_path:
            self.file_label.setText(f"현재 파일: {result.summary.file_path}")

        self.row_card.set_value(result.summary.row_count)
        self.year_card.set_value(
            f"{min(result.summary.years)}~{max(result.summary.years)}"
            if result.summary.years
            else "-"
        )
        self.chapter_card.set_value(len(result.summary.chapters))
        self.issue_card.set_value(len(result.issues))
