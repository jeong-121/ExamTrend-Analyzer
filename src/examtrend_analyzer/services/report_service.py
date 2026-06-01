"""Report generation service."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class ReportService:
    """분석 결과를 Markdown 보고서로 생성하고 저장하는 서비스."""

    def build_markdown(self, result: Any) -> str:
        if isinstance(result, dict):
            return self._build_from_dict(result)

        return self._build_from_object(result)

    def save_markdown(self, result: Any, path: str | Path) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.build_markdown(result), encoding="utf-8")
        return output_path

    def create_markdown(self, result: Any, path: str | Path) -> Path:
        return self.save_markdown(result, path)

    def _build_from_object(self, result: Any) -> str:
        summary = getattr(result, "summary", None)

        row_count = getattr(summary, "row_count", 0)
        file_path = getattr(summary, "file_path", None)
        topics = getattr(summary, "topics", [])

        lines: list[str] = []

        lines.append("# 분석 보고서")
        lines.append("")

        lines.append("## 1. 분석 개요")
        lines.append("")
        lines.append(f"- 문항 수: {row_count}")
        lines.append(f"- 원본 파일: {file_path if file_path else '-'}")
        lines.append(f"- 자동 주제 수: {len(topics)}")
        lines.append("")

        analysis_status = getattr(result, "analysis_status", {})
        topic_distribution = getattr(result, "topic_distribution", [])
        topic_keywords = getattr(result, "topic_keywords", [])

        lines.append("## 2. 분석 실행 상태")
        if analysis_status:
            for key, value in analysis_status.items():
                lines.append(f"- {key}: {value}")
        else:
            lines.append("- 상태 정보 없음")
        lines.append("")

        self._append_mapping(lines, "3. 키워드 빈도", getattr(result, "keyword_counts", {}))

        lines.append("## 4. 자동 주제별 비중")
        if topic_distribution:
            for row in topic_distribution[:30]:
                lines.append(
                    f"- {row['topic']}: {row['count']}문항 ({row['ratio']}%)"
                )
        else:
            lines.append("- 결과 없음")
        lines.append("")

        lines.append("## 5. 자동 주제별 대표 키워드")
        if topic_keywords:
            for row in topic_keywords[:30]:
                keywords = row.get("keywords", [])
                if isinstance(keywords, list):
                    keyword_text = ", ".join(map(str, keywords))
                else:
                    keyword_text = str(keywords)
                lines.append(f"- {row.get('topic', '-')}: {keyword_text}")
        else:
            lines.append("- 결과 없음")
        lines.append("")

        lines.append("## 6. 유사 문항 후보")
        similar_pairs = getattr(result, "similar_pairs", [])
        if similar_pairs:
            for row in similar_pairs[:50]:
                lines.append(
                    f"- similarity={row.get('similarity')}\n"
                    f"  - 문항1: {row.get('question_1_source', '-')} / {row.get('question_1_text', '')}\n"
                    f"  - 문항2: {row.get('question_2_source', '-')} / {row.get('question_2_text', '')}"
                )
        else:
            lines.append("- 기준 이상 유사 문항 후보가 없습니다.")
        lines.append("")

        lines.append("## 7. 검증 이슈")
        issues = getattr(result, "issues", [])
        if issues:
            for issue in issues[:100]:
                level = getattr(issue, "level", "-")
                code = getattr(issue, "code", "-")
                message = getattr(issue, "message", "-")
                row_index = getattr(issue, "row_index", None)
                column = getattr(issue, "column", None)

                location = []
                if row_index is not None:
                    location.append(f"row={row_index}")
                if column:
                    location.append(f"column={column}")

                location_text = f" ({', '.join(location)})" if location else ""
                lines.append(f"- [{level}] {code}: {message}{location_text}")
        else:
            lines.append("- 검증 이슈 없음")
        lines.append("")

        return "\n".join(lines)

    def _build_from_dict(self, result: dict[str, Any]) -> str:
        lines: list[str] = []

        lines.append("# 분석 보고서")
        lines.append("")
        lines.append(f"- 문항 수: {result.get('question_count', 0)}")
        lines.append("")

        self._append_mapping(lines, "상위 키워드", result.get("keywords", {}))

        return "\n".join(lines)

    def _append_mapping(
        self,
        lines: list[str],
        title: str,
        data: dict[Any, Any],
    ) -> None:
        lines.append(f"## {title}")

        if data:
            for key, value in data.items():
                lines.append(f"- {key}: {value}")
        else:
            lines.append("- 결과 없음")

        lines.append("")
