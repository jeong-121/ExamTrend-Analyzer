"""Application settings."""

from pathlib import Path

APP_NAME = "ExamTrend Analyzer"
APP_VERSION = "0.2.0"
DEFAULT_DB_PATH = Path("examtrend.db")
DEFAULT_REPORT_DIR = Path("reports")
SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
