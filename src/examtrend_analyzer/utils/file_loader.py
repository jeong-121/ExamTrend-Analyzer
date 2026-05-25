"""File loader utility module.

CSV, Excel 등 외부 기출문제 데이터 파일을 pandas DataFrame으로 불러온다.
"""

from pathlib import Path

import pandas as pd


class FileLoader:
    """기출문제 데이터 파일 로더."""

    def load_csv(self, file_path: str | Path) -> pd.DataFrame:
        """CSV 파일을 DataFrame으로 로딩한다."""
        # TODO: 인코딩 자동 감지 및 컬럼 검증 기능 추가
        return pd.read_csv(file_path)

    def load_excel(self, file_path: str | Path) -> pd.DataFrame:
        """Excel 파일을 DataFrame으로 로딩한다."""
        # TODO: 시트 선택 옵션 추가
        return pd.read_excel(file_path)

    def validate_columns(self, data: pd.DataFrame, required_columns: list[str]) -> bool:
        """필수 컬럼이 존재하는지 검사한다."""
        return all(column in data.columns for column in required_columns)
