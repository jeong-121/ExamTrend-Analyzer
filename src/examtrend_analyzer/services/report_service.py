"""Report generation service."""

from __future__ import annotations

from pathlib import Path

from examtrend_analyzer.services.analysis_service import AnalysisResult


class ReportService:
    """Creates text reports from analysis results."""

    def build_markdown(self, result: AnalysisResult) -> str:
        """Build a markdown report string."""
        lines: list[str] = [
            "# ExamTrend Analyzer Report",
            "",
            f"- 총 문항 수: {result.row_count}",
            "",
            "## 상위 키워드",
        ]
        if result.keyword_top:
            lines.extend(f"- {keyword}: {count}" for keyword, count in result.keyword_top)
        else:
            lines.append("- 결과 없음")

        lines.extend(["", "## 연도별 출제 수"])
        lines.extend(f"- {index}: {value}" for index, value in result.year_counts.items())

        lines.extend(["", "## 단원별 출제 수"])
        lines.extend(f"- {index}: {value}" for index, value in result.chapter_counts.items())

        lines.extend(["", "## 난이도 분포"])
        lines.extend(f"- {index}: {value}" for index, value in result.difficulty_counts.items())
        return "\n".join(lines) + "\n"

    def save_markdown(self, result: AnalysisResult, output_path: str | Path) -> Path:
        """Save a markdown report."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.build_markdown(result), encoding="utf-8")
        return path
