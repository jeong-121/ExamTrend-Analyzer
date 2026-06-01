"""File loader utility module."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

import pandas as pd

from examtrend_analyzer.core.schema import apply_field_mapping, normalize_column_name

class FileLoader:
    """Load CSV and Excel datasets into pandas DataFrames."""

    def load(self, file_path: str | Path, mapping: Mapping[str, str] | None = None, normalize: bool = True) -> pd.DataFrame:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")
        if path.stat().st_size == 0:
            raise ValueError("빈 파일은 불러올 수 없습니다.")
        if path.suffix.lower() == ".csv":
            data = self.load_csv(path, normalize=False)
        elif path.suffix.lower() in {".xlsx", ".xls"}:
            data = self.load_excel(path, normalize=False)
        else:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {path.suffix}")
        if mapping:
            return self.apply_mapping(data, mapping)
        if normalize:
            return self._normalize_columns(data)
        return data

    def load_raw(self, file_path: str | Path) -> pd.DataFrame:
        return self.load(file_path, normalize=False)

    def load_csv(self, file_path: str | Path, normalize: bool = True) -> pd.DataFrame:
        last_error: Exception | None = None
        for encoding in ("utf-8-sig", "utf-8", "cp949"):
            try:
                data = pd.read_csv(file_path, encoding=encoding)
                return self._normalize_columns(data) if normalize else data
            except UnicodeDecodeError as exc:
                last_error = exc
        if last_error:
            raise last_error
        data = pd.read_csv(file_path)
        return self._normalize_columns(data) if normalize else data

    def load_excel(self, file_path: str | Path, sheet_name: int | str = 0, normalize: bool = True) -> pd.DataFrame:
        data = pd.read_excel(file_path, sheet_name=sheet_name)
        return self._normalize_columns(data) if normalize else data

    def validate_columns(self, data: pd.DataFrame, required_columns: list[str]) -> bool:
        return all(column in data.columns for column in required_columns)

    def apply_mapping(self, data: pd.DataFrame, mapping: Mapping[str, str]) -> pd.DataFrame:
        copied = data.copy()
        copied.columns = apply_field_mapping([str(c) for c in copied.columns], mapping)
        return copied

    def _normalize_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        copied = data.copy()
        copied.columns = [normalize_column_name(column) for column in copied.columns]
        return copied
