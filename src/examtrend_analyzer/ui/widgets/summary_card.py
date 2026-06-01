"""Small summary card widget."""

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class SummaryCard(QFrame):
    """Displays a metric title and value."""

    def __init__(self, title: str, value: str = "-", parent=None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.title_label = QLabel(title)
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("font-size: 24px; font-weight: 700;")

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

    def set_value(self, value: str) -> None:
        """Update the displayed value."""
        self.value_label.setText(value)
