"""Analysis result page."""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QPlainTextEdit, QVBoxLayout, QWidget

from examtrend_analyzer.services.analysis_service import AnalysisResult
from examtrend_analyzer.ui.widgets import SummaryCard


class AnalysisPage(QWidget):
    """Shows calculated trend-analysis results as readable text."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.total_card = SummaryCard("분석 문항 수", "0")
        self.keyword_card = SummaryCard("상위 키워드 수", "0")
        self.chapter_card = SummaryCard("단원 수", "0")
        self.result_text = QPlainTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("데이터를 불러온 뒤 [분석 실행]을 누르세요.")

        card_layout = QHBoxLayout()
        card_layout.addWidget(self.total_card)
        card_layout.addWidget(self.keyword_card)
        card_layout.addWidget(self.chapter_card)

        layout = QVBoxLayout(self)
        layout.addLayout(card_layout)
        layout.addWidget(QLabel("분석 결과"))
        layout.addWidget(self.result_text)

    def set_result(self, result: AnalysisResult) -> None:
        """Render analysis result."""
        self.total_card.set_value(str(result.row_count))
        self.keyword_card.set_value(str(len(result.keyword_top)))
        self.chapter_card.set_value(str(len(result.chapter_counts)))
        self.result_text.setPlainText(self._format_result(result))

    def _format_result(self, result: AnalysisResult) -> str:
        lines: list[str] = [
            "[상위 키워드]",
            *[f"{keyword}: {count}" for keyword, count in result.keyword_top],
            "",
            "[연도별 출제 수]",
            result.year_counts.to_string(),
            "",
            "[단원별 출제 수]",
            result.chapter_counts.to_string(),
            "",
            "[단원별 출제 비중]",
            result.chapter_ratio.round(3).to_string(),
            "",
            "[난이도 분포]",
            result.difficulty_counts.to_string(),
            "",
            "[연도별 평균 난이도]",
            result.difficulty_by_year.round(2).to_string(),
            "",
            "[문제 유형 분포]",
            result.question_type_counts.to_string(),
        ]
        return "\n".join(lines)
