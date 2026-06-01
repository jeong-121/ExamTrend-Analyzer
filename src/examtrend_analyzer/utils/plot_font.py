"""Matplotlib Korean font configuration."""

from __future__ import annotations

import platform
from functools import lru_cache

import matplotlib
import matplotlib.font_manager as fm


@lru_cache(maxsize=1)
def configure_korean_font() -> str:
    """Configure a Korean-capable font for matplotlib.

    Returns the font family name that was selected.
    """
    candidates = [
        "Malgun Gothic",
        "AppleGothic",
        "NanumGothic",
        "Noto Sans CJK KR",
        "Noto Sans KR",
        "Noto Sans CJK",
        "DejaVu Sans",
    ]

    available = {font.name for font in fm.fontManager.ttflist}

    selected = None
    for candidate in candidates:
        if candidate in available:
            selected = candidate
            break

    if selected is None:
        system = platform.system()
        if system == "Windows":
            selected = "Malgun Gothic"
        elif system == "Darwin":
            selected = "AppleGothic"
        else:
            selected = "NanumGothic"

    matplotlib.rcParams["font.family"] = selected
    matplotlib.rcParams["axes.unicode_minus"] = False

    return selected
