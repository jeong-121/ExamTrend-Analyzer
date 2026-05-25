"""Application entry point.

PyQt6 기반 Desktop Application을 실행하는 진입점이다.
"""

from examtrend_analyzer.ui.main_window import run_app


def main() -> None:
    """애플리케이션을 실행한다."""
    # TODO: 애플리케이션 설정 로딩 기능 추가
    run_app()


if __name__ == "__main__":
    main()
