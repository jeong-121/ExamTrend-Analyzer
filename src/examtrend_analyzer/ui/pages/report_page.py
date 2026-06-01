"""Report page."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QPushButton, QPlainTextEdit, QVBoxLayout, QWidget

from examtrend_analyzer.core.models import AnalysisResult


class ReportPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.save_button = QPushButton("Markdown 보고서 저장")
        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("보고서"))
        layout.addWidget(self.save_button)
        layout.addWidget(self.preview)

    def update_result(self, result: AnalysisResult) -> None:
        lines = [
            "# 분석 보고서 미리보기",
            "",
            f"문항 수: {result.summary.row_count}",
            f"검증 이슈: {len(result.issues)}",
            "",
            "## 상위 키워드",
        ]

        for keyword, count in sorted(
            result.keyword_counts.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:15]:
            lines.append(f"- {keyword}: {count}")

        lines.extend(["", "## 단원별 출제 비중"])

        if result.chapter_distribution:
            for row in result.chapter_distribution[:10]:
                lines.append(f"- {row['chapter']}: {row['count']}문항 ({row['ratio']}%)")
        else:
            lines.append("- chapter 컬럼 또는 자동 분류 결과가 없어 분석하지 못했습니다.")

        lines.extend(["", "## 유사 문항 후보"])

        if result.similar_pairs:
            for row in result.similar_pairs[:10]:
                lines.append(
                    f"- similarity={row.get('similarity')}\\n"
                    f"  - 문항1: {row.get('question_1_source', '-')} / {row.get('question_1_text', '')}\\n"
                    f"  - 문항2: {row.get('question_2_source', '-')} / {row.get('question_2_text', '')}"
                )
        else:
            lines.append("- 기준 이상 유사 문항 후보가 없습니다.")

        self.preview.setPlainText("\n".join(lines))
