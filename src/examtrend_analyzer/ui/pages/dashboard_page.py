"""Dashboard page for loaded data and summary metrics."""

from __future__ import annotations

import pandas as pd
from PySide6.QtWidgets import QGridLayout, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from examtrend_analyzer.ui.widgets import SummaryCard


class DashboardPage(QWidget):
    """Shows dataset preview and high-level status."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.file_card = SummaryCard("불러온 파일", "없음")
        self.row_card = SummaryCard("문항 수", "0")
        self.column_card = SummaryCard("컬럼 수", "0")
        self.preview_table = QTableWidget()
        self.preview_table.setAlternatingRowColors(True)

        card_layout = QGridLayout()
        card_layout.addWidget(self.file_card, 0, 0)
        card_layout.addWidget(self.row_card, 0, 1)
        card_layout.addWidget(self.column_card, 0, 2)

        layout = QVBoxLayout(self)
        layout.addLayout(card_layout)
        layout.addWidget(QLabel("데이터 미리보기"))
        layout.addWidget(self.preview_table)

    def set_dataset(self, file_name: str, data: pd.DataFrame) -> None:
        """Display loaded dataset metadata and preview rows."""
        self.file_card.set_value(file_name)
        self.row_card.set_value(str(len(data)))
        self.column_card.set_value(str(len(data.columns)))
        self._fill_table(data.head(30))

    def _fill_table(self, data: pd.DataFrame) -> None:
        self.preview_table.clear()
        self.preview_table.setRowCount(len(data))
        self.preview_table.setColumnCount(len(data.columns))
        self.preview_table.setHorizontalHeaderLabels([str(column) for column in data.columns])

        for row_index, (_, row) in enumerate(data.iterrows()):
            for column_index, value in enumerate(row):
                self.preview_table.setItem(row_index, column_index, QTableWidgetItem(str(value)))

        self.preview_table.resizeColumnsToContents()
