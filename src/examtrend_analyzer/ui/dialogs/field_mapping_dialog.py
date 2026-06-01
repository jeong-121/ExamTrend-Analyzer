"""Field mapping dialog for user-provided datasets."""

from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout

from examtrend_analyzer.core.schema import COLUMN_LABELS, REQUIRED_COLUMNS, STANDARD_COLUMNS, FieldMapping

class FieldMappingDialog(QDialog):
    """Allow users to map arbitrary input columns to standard columns."""

    def __init__(self, columns: list[str], suggested: FieldMapping, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("필드 매핑")
        self.resize(760, 480)
        self.columns = columns
        self.combos: dict[str, QComboBox] = {}

        self.table = QTableWidget(len(columns), 2)
        self.table.setHorizontalHeaderLabels(["원본 컬럼", "표준 필드"])
        options = [""] + STANDARD_COLUMNS
        for row, column in enumerate(columns):
            self.table.setItem(row, 0, QTableWidgetItem(column))
            combo = QComboBox()
            combo.addItems(options)
            proposed = suggested.mapping.get(column, "")
            if proposed in options:
                combo.setCurrentText(proposed)
            self.combos[column] = combo
            self.table.setCellWidget(row, 1, combo)
        self.table.resizeColumnsToContents()

        self.message = QLabel("필수 필드: " + ", ".join(f"{c}({COLUMN_LABELS.get(c, c)})" for c in REQUIRED_COLUMNS))
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("원본 파일의 컬럼을 프로젝트 표준 필드에 연결하세요."))
        layout.addWidget(self.message)
        layout.addWidget(self.table)
        layout.addWidget(buttons)

    def get_mapping(self) -> dict[str, str]:
        return {column: combo.currentText() for column, combo in self.combos.items()}

    def missing_required(self) -> list[str]:
        mapped = set(self.get_mapping().values())
        return [column for column in REQUIRED_COLUMNS if column not in mapped]
