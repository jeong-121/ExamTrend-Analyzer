"""Heatmap generation module.

단원-연도, 키워드-연도 등 2차원 빈도 데이터를 히트맵으로 시각화한다.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


class HeatmapGenerator:
    """히트맵 생성 클래스."""

    def create_heatmap(self, matrix: pd.DataFrame, title: str, output_path: str | Path | None = None) -> None:
        """DataFrame 형태의 행렬 데이터를 히트맵으로 생성한다."""
        # TODO: seaborn 사용 여부 검토 또는 matplotlib 기반 개선
        plt.imshow(matrix, aspect="auto")
        plt.title(title)
        plt.colorbar()
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path)

        plt.close()
