"""Main window module.

PyQt6 기반 메인 윈도우를 정의한다.
현재는 초기 화면 골격만 제공하며, 이후 데이터 로딩, 분석 실행,
그래프 표시 기능을 연결한다.
"""

import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    """ExamTrend Analyzer의 메인 윈도우."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ExamTrend Analyzer")
        self.resize(1000, 700)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """초기 UI 컴포넌트를 구성한다."""
        # TODO: 파일 불러오기 버튼, 분석 실행 버튼, 그래프 영역 추가
        central_widget = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel("ExamTrend Analyzer")
        subtitle_label = QLabel("기출문제 기반 출제 경향 분석 시스템")

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)


def run_app() -> None:
    """PyQt6 애플리케이션을 실행한다."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
