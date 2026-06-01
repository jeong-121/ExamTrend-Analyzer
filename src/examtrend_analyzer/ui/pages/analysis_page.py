"""Analysis result page."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QPlainTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from examtrend_analyzer.core.models import AnalysisResult
from examtrend_analyzer.ui.widgets.chart_canvas import AnalysisChartsWidget


class AnalysisPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.tabs = QTabWidget()

        self.keyword_table = QTableWidget(0, 2)
        self.keyword_table.setHorizontalHeaderLabels(["키워드", "빈도"])

        self.topic_table = QTableWidget(0, 3)
        self.topic_table.setHorizontalHeaderLabels(["자동 주제", "문항 수", "비율(%)"])

        self.topic_keyword_table = QTableWidget(0, 2)
        self.topic_keyword_table.setHorizontalHeaderLabels(["자동 주제", "대표 키워드"])

        self.similar_table = QTableWidget(0, 5)
        self.similar_table.setHorizontalHeaderLabels([
            "유사도",
            "문항 1 출처",
            "문항 1 내용",
            "문항 2 출처",
            "문항 2 내용",
        ])
        self._configure_similar_table()

        self.issue_table = QTableWidget(0, 5)
        self.issue_table.setHorizontalHeaderLabels(["수준", "코드", "행", "컬럼", "메시지"])

        self.summary_text = QPlainTextEdit()
        self.summary_text.setReadOnly(True)

        self.charts_widget = AnalysisChartsWidget()

        self.tabs.addTab(self._wrap(self.summary_text), "요약")
        self.tabs.addTab(self._wrap(self.keyword_table), "키워드")
        self.tabs.addTab(self._wrap(self.topic_table), "자동 주제")
        self.tabs.addTab(self._wrap(self.topic_keyword_table), "주제 키워드")
        self.tabs.addTab(self._wrap(self.similar_table), "유사 문항")
        self.tabs.addTab(self._wrap(self.issue_table), "검증/경고")
        self.tabs.addTab(self.charts_widget, "시각화")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("분석 결과"))
        layout.addWidget(self.tabs)

    def _wrap(self, widget: QWidget) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(widget)
        return container

    def _configure_similar_table(self) -> None:
        self.similar_table.setWordWrap(True)
        self.similar_table.setAlternatingRowColors(True)
        self.similar_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.similar_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.similar_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.similar_table.setMouseTracking(False)
        self.similar_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.similar_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.similar_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.similar_table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.similar_table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        self.similar_table.horizontalScrollBar().setSingleStep(20)
        self.similar_table.horizontalScrollBar().setPageStep(300)
        self.similar_table.verticalScrollBar().setSingleStep(20)

        header = self.similar_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(False)
        header.setMinimumSectionSize(80)

        vertical_header = self.similar_table.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        vertical_header.setDefaultSectionSize(118)
        vertical_header.setMinimumSectionSize(96)

        self._apply_similar_table_column_widths()
        self.similar_table.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.similar_table.setStyleSheet(
            """
            QTableWidget {
                selection-background-color: transparent;
                selection-color: palette(text);
            }
            QTableWidget::item:selected {
                background: transparent;
                color: palette(text);
            }
            QTableWidget::item:hover {
                background: transparent;
            }
            """
        )

    def _apply_similar_table_column_widths(self) -> None:
        self.similar_table.setColumnWidth(0, 80)
        self.similar_table.setColumnWidth(1, 240)
        self.similar_table.setColumnWidth(2, 560)
        self.similar_table.setColumnWidth(3, 240)
        self.similar_table.setColumnWidth(4, 560)

    def update_result(self, result: AnalysisResult) -> None:
        self._update_keyword_table(result)
        self._update_topic_table(result)
        self._update_topic_keyword_table(result)
        self._update_similar_table(result)
        self._update_issue_table(result)
        self._update_summary(result)
        self.charts_widget.update_result(result)

    def _update_keyword_table(self, result: AnalysisResult) -> None:
        rows = sorted(result.keyword_counts.items(), key=lambda item: item[1], reverse=True)[:100]
        self.keyword_table.setRowCount(len(rows))

        for row, (keyword, count) in enumerate(rows):
            self.keyword_table.setItem(row, 0, QTableWidgetItem(str(keyword)))
            self.keyword_table.setItem(row, 1, QTableWidgetItem(str(count)))

        self.keyword_table.resizeColumnsToContents()

    def _update_topic_table(self, result: AnalysisResult) -> None:
        rows = getattr(result, "topic_distribution", [])
        self.topic_table.setRowCount(len(rows))

        for row, item in enumerate(rows):
            self.topic_table.setItem(row, 0, QTableWidgetItem(str(item.get("topic", ""))))
            self.topic_table.setItem(row, 1, QTableWidgetItem(str(item.get("count", 0))))
            self.topic_table.setItem(row, 2, QTableWidgetItem(str(item.get("ratio", 0))))

        self.topic_table.resizeColumnsToContents()

    def _update_topic_keyword_table(self, result: AnalysisResult) -> None:
        rows = getattr(result, "topic_keywords", [])
        self.topic_keyword_table.setRowCount(len(rows))

        for row, item in enumerate(rows):
            keywords = item.get("keywords", [])
            if isinstance(keywords, list):
                keyword_text = ", ".join(map(str, keywords))
            else:
                keyword_text = str(keywords)

            self.topic_keyword_table.setItem(row, 0, QTableWidgetItem(str(item.get("topic", ""))))
            self.topic_keyword_table.setItem(row, 1, QTableWidgetItem(keyword_text))

        self.topic_keyword_table.resizeColumnsToContents()

    def _update_similar_table(self, result: AnalysisResult) -> None:
        rows = result.similar_pairs[:100]
        self.similar_table.setRowCount(len(rows))

        for row, item in enumerate(rows):
            values = [
                str(item.get("similarity", "")),
                str(item.get("question_1_source", "-")),
                str(item.get("question_1_text", "")),
                str(item.get("question_2_source", "-")),
                str(item.get("question_2_text", "")),
            ]

            for column, value in enumerate(values):
                table_item = QTableWidgetItem(value)
                table_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
                table_item.setToolTip(value)
                self.similar_table.setItem(row, column, table_item)

            self.similar_table.setRowHeight(row, 118)

        self._apply_similar_table_column_widths()
        self.similar_table.resizeRowsToContents()

        for row in range(self.similar_table.rowCount()):
            if self.similar_table.rowHeight(row) < 96:
                self.similar_table.setRowHeight(row, 96)
            elif self.similar_table.rowHeight(row) > 180:
                self.similar_table.setRowHeight(row, 180)

    def _update_issue_table(self, result: AnalysisResult) -> None:
        rows = result.issues[:300]
        self.issue_table.setRowCount(len(rows))

        for row, issue in enumerate(rows):
            self.issue_table.setItem(row, 0, QTableWidgetItem(issue.level))
            self.issue_table.setItem(row, 1, QTableWidgetItem(issue.code))
            self.issue_table.setItem(row, 2, QTableWidgetItem("" if issue.row_index is None else str(issue.row_index)))
            self.issue_table.setItem(row, 3, QTableWidgetItem(issue.column or ""))
            self.issue_table.setItem(row, 4, QTableWidgetItem(issue.message))

        self.issue_table.resizeColumnsToContents()

    def _update_summary(self, result: AnalysisResult) -> None:
        issue_counts = {"error": 0, "warning": 0, "info": 0}

        for issue in result.issues:
            issue_counts[issue.level] = issue_counts.get(issue.level, 0) + 1

        analysis_status = getattr(result, "analysis_status", {})
        skipped_analyses = getattr(result, "skipped_analyses", [])
        topic_distribution = getattr(result, "topic_distribution", [])

        lines: list[str] = []

        lines.append("[분석 실행 상태]")
        if analysis_status:
            for key, value in analysis_status.items():
                lines.append(f"{key}: {value}")
        else:
            lines.append("상태 정보 없음")

        lines.append("")
        lines.append("[건너뛴 분석]")
        if skipped_analyses:
            lines.extend(skipped_analyses)
        else:
            lines.append("없음")

        lines.append("")
        lines.append("[검증 요약]")
        lines.append(f"error: {issue_counts.get('error', 0)}")
        lines.append(f"warning: {issue_counts.get('warning', 0)}")
        lines.append(f"info: {issue_counts.get('info', 0)}")

        lines.append("")
        lines.append("[자동 주제별 문항 수]")
        if getattr(result, "topic_counts", {}):
            for key, value in result.topic_counts.items():
                lines.append(f"{key}: {value}")
        else:
            lines.append("자동 주제 분석 결과 없음")

        lines.append("")
        lines.append("[자동 주제별 비중]")
        if topic_distribution:
            for row in topic_distribution[:20]:
                lines.append(f"{row['topic']}: {row['count']}문항 ({row['ratio']}%)")
        else:
            lines.append("결과 없음")

        self.summary_text.setPlainText("\n".join(lines))
