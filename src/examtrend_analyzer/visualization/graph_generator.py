"""Graph generation module.

matplotlib을 사용하여 분석 결과 그래프를 생성한다.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


class GraphGenerator:
    """기본 그래프 생성 클래스."""

    def create_bar_chart(self, data: pd.Series, title: str, output_path: str | Path | None = None) -> None:
        """막대그래프를 생성한다."""
        # TODO: 한글 폰트 설정 자동화
        data.plot(kind="bar")
        plt.title(title)
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path)

        plt.close()

    def create_line_chart(self, data: pd.Series, title: str, output_path: str | Path | None = None) -> None:
        """선 그래프를 생성한다."""
        # TODO: x축, y축 라벨 옵션 추가
        data.plot(kind="line", marker="o")
        plt.title(title)
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path)

        plt.close()
