"""Matplotlib chart canvas widgets for PySide6."""

from __future__ import annotations

from typing import Any

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from examtrend_analyzer.core.models import AnalysisResult
from examtrend_analyzer.utils.plot_font import configure_korean_font


class ChartCanvas(QWidget):
    """Reusable chart container."""

    def __init__(self, title: str, parent=None) -> None:
        super().__init__(parent)

        configure_korean_font()

        self.title_label = QLabel(title)
        self.figure = Figure(figsize=(7, 4), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.canvas)

    def clear(self, message: str = "표시할 데이터가 없습니다.") -> None:
        configure_korean_font()
        self.figure.clear()
        axis = self.figure.add_subplot(111)
        axis.text(
            0.5,
            0.5,
            message,
            ha="center",
            va="center",
            transform=axis.transAxes,
        )
        axis.set_axis_off()
        self.canvas.draw_idle()

    def bar_chart(
        self,
        data: dict[Any, int],
        title: str,
        x_label: str,
        y_label: str,
        top_n: int | None = None,
        horizontal: bool = False,
    ) -> None:
        configure_korean_font()
        self.figure.clear()

        if not data:
            self.clear("표시할 데이터가 없습니다.")
            return

        items = list(data.items())

        if top_n is not None:
            items = sorted(
                items,
                key=lambda item: item[1],
                reverse=True,
            )[:top_n]
        else:
            items = sorted(items, key=lambda item: str(item[0]))

        labels = [str(key) for key, _ in items]
        values = [int(value) for _, value in items]

        axis = self.figure.add_subplot(111)

        if horizontal:
            labels = list(reversed(labels))
            values = list(reversed(values))
            axis.barh(labels, values)
            axis.set_xlabel(y_label)
            axis.set_ylabel(x_label)
        else:
            axis.bar(labels, values)
            axis.set_xlabel(x_label)
            axis.set_ylabel(y_label)
            axis.tick_params(axis="x", rotation=45)

        axis.set_title(title)
        axis.grid(True, axis="y" if not horizontal else "x", alpha=0.25)

        self.canvas.draw_idle()

    def pie_chart(
        self,
        rows: list[dict[str, object]],
        title: str,
        label_key: str = "chapter",
        value_key: str = "count",
        top_n: int = 8,
    ) -> None:
        configure_korean_font()
        self.figure.clear()

        if not rows:
            self.clear("chapter 컬럼 또는 자동 분류 결과가 없어 표시할 수 없습니다.")
            return

        selected = rows[:top_n]
        labels = [str(row[label_key]) for row in selected]
        values = [int(row[value_key]) for row in selected]

        axis = self.figure.add_subplot(111)
        axis.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
        )
        axis.set_title(title)
        axis.axis("equal")

        self.canvas.draw_idle()


class AnalysisChartsWidget(QWidget):
    """Composite visualization panel for simplified AnalysisResult."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.keyword_chart = ChartCanvas("상위 키워드 빈도")
        self.chapter_chart = ChartCanvas("단원별 출제 비중")

        layout = QVBoxLayout(self)
        layout.addWidget(self.keyword_chart)
        layout.addWidget(self.chapter_chart)

    def update_result(self, result: AnalysisResult) -> None:
        self.keyword_chart.bar_chart(
            result.keyword_counts,
            title="상위 키워드 빈도",
            x_label="키워드",
            y_label="빈도",
            top_n=15,
            horizontal=True,
        )

        self.chapter_chart.pie_chart(
            getattr(result, "chapter_distribution", []),
            title="단원별 출제 비중",
        )
