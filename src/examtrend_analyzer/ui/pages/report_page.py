"""Report page."""

from PySide6.QtWidgets import QLabel, QPlainTextEdit, QVBoxLayout, QWidget


class ReportPage(QWidget):
    """Shows generated markdown report content."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.report_text = QPlainTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setPlaceholderText("분석 실행 후 보고서가 표시됩니다.")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("보고서 미리보기"))
        layout.addWidget(self.report_text)

    def set_report(self, content: str) -> None:
        """Display report markdown."""
        self.report_text.setPlainText(content)
