"Application service for file loading, automatic mapping, and simplified analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd

from examtrend_analyzer.analysis.chapter_classifier import ChapterClassifier
from examtrend_analyzer.analysis.keyword_analyzer import KeywordAnalyzer
from examtrend_analyzer.analysis.similarity_analyzer import SimilarityAnalyzer
from examtrend_analyzer.core.file_loader import FileLoader
from examtrend_analyzer.core.models import AnalysisResult, DatasetSummary, ValidationIssue
from examtrend_analyzer.core.schema import FieldMapping, REQUIRED_COLUMNS, suggest_field_mapping
from examtrend_analyzer.utils.filename_metadata import extract_metadata_from_filename


QUESTION_COLUMN_CANDIDATES = [
    "question_text",
    "question",
    "문제",
    "문항",
    "본문",
    "문제본문",
    "내용",
    "text",
]


@dataclass
class AnalysisService:
    """Coordinate file loading, automatic field mapping, and simplified analysis."""

    file_loader: FileLoader = field(default_factory=FileLoader)
    current_dataframe: pd.DataFrame | None = None
    current_file_path: str | None = None
    current_mapping: dict[str, str] = field(default_factory=dict)
    last_result: AnalysisResult | None = None
    last_suggested_mapping: FieldMapping | None = None

    def preview_file(self, path: str | Path) -> tuple[pd.DataFrame, FieldMapping]:
        df = self.file_loader.load(path)
        df = self._attach_filename_metadata(df, path)

        self.current_dataframe = df
        self.current_file_path = str(path)

        suggested = suggest_field_mapping([str(column) for column in df.columns])
        self.last_suggested_mapping = suggested

        return df, suggested

    def preview_files(self, paths: list[str | Path]) -> tuple[pd.DataFrame, FieldMapping]:
        if not paths:
            raise ValueError("선택된 파일이 없습니다.")

        frames: list[pd.DataFrame] = []
        file_names: list[str] = []

        for path in paths:
            df = self.file_loader.load(path)
            df = self._attach_filename_metadata(df, path)
            frames.append(df)
            file_names.append(Path(path).name)

        merged = pd.concat(frames, ignore_index=True, sort=False)

        self.current_dataframe = merged
        self.current_file_path = "; ".join(file_names)

        suggested = suggest_field_mapping([str(column) for column in merged.columns])
        self.last_suggested_mapping = suggested

        return merged, suggested

    def can_auto_apply_mapping(self, suggested: FieldMapping | None = None) -> bool:
        suggested = suggested or self.last_suggested_mapping

        if suggested is None:
            return False

        mapped_values = {value for value in suggested.mapping.values() if value}
        required_columns = REQUIRED_COLUMNS or ["question_text"]

        return all(required in mapped_values for required in required_columns)

    def auto_apply_mapping(self, suggested: FieldMapping | None = None) -> pd.DataFrame:
        suggested = suggested or self.last_suggested_mapping

        if suggested is None:
            raise ValueError("자동 매핑 정보가 없습니다.")

        if not self.can_auto_apply_mapping(suggested):
            mapped_values = {value for value in suggested.mapping.values() if value}
            required_columns = REQUIRED_COLUMNS or ["question_text"]
            missing = [
                required
                for required in required_columns
                if required not in mapped_values
            ]

            raise ValueError(
                "자동 매핑에 실패했습니다. 수동 매핑이 필요합니다: "
                + ", ".join(missing)
            )

        return self.apply_mapping(suggested.mapping)

    def apply_mapping(self, mapping: dict[str, str]) -> pd.DataFrame:
        if self.current_dataframe is None:
            raise ValueError("먼저 파일을 불러와야 합니다.")

        rename_map = {
            original: standard
            for original, standard in mapping.items()
            if original in self.current_dataframe.columns and standard
        }

        self.current_dataframe = self.current_dataframe.rename(columns=rename_map)
        self.current_mapping = mapping

        return self.current_dataframe

    def has_data(self) -> bool:
        return self.current_dataframe is not None and not self.current_dataframe.empty

    def analyze_current(self, question_column: str | None = None) -> AnalysisResult:
        if self.current_dataframe is None or self.current_dataframe.empty:
            raise ValueError("분석할 데이터가 없습니다. 먼저 기출문제 파일을 불러오세요.")

        result = self.run_analysis(
            self.current_dataframe,
            question_column=question_column,
        )

        self.last_result = result
        return result

    def run_analysis(
        self,
        dataframe: pd.DataFrame,
        question_column: str | None = None,
    ) -> AnalysisResult:
        if dataframe is None or dataframe.empty:
            raise ValueError("분석할 데이터가 없습니다. 먼저 기출문제 파일을 불러오세요.")

        df = dataframe.copy()
        question_column = question_column or self.detect_question_column(df)
        texts = df[question_column].fillna("").astype(str).tolist()

        if not any(text.strip() for text in texts):
            raise ValueError("분석 대상 문항 본문이 모두 비어 있습니다.")

        analysis_status: dict[str, str] = {}
        skipped_analyses: list[str] = []

        keyword_analyzer = KeywordAnalyzer()
        similarity_analyzer = SimilarityAnalyzer()

        keyword_counts = keyword_analyzer.analyze(texts, top_n=50)
        keyword_rows = keyword_analyzer.analyze_with_document_frequency(texts, top_n=50)

        similar_pairs = similarity_analyzer.find_similar_pairs(
            texts,
            threshold=0.55,
            max_pairs=100,
        )
        similar_pairs = self._enrich_similar_pairs(
            similar_pairs,
            df,
            question_column,
        )

        analysis_status["키워드 분석"] = "실행됨"
        analysis_status["유사 문항 분석"] = "실행됨"

        chapter_column, chapter_source = self._ensure_chapter_column(df, question_column)

        if chapter_column:
            chapter_counts = self._value_counts(df, chapter_column)
            chapter_distribution = self._chapter_distribution(df, chapter_column)
            if chapter_source == "keyword_auto":
                analysis_status["단원별 출제 비중"] = "실행됨: 키워드 기반 자동 분류"
            else:
                analysis_status["단원별 출제 비중"] = "실행됨"
        else:
            chapter_counts = {}
            chapter_distribution = []
            chapter_source = "none"
            analysis_status["단원별 출제 비중"] = "건너뜀: chapter 컬럼 없음"
            skipped_analyses.append("단원별 출제 비중 분석")

        issues = self._validate_for_ui(df, question_column)

        if chapter_source == "keyword_auto":
            issues.append(
                ValidationIssue(
                    level="info",
                    code="AUTO_CHAPTER",
                    message="chapter 컬럼이 없어 키워드 기반 자동 단원 분류를 적용했습니다.",
                    column="chapter_auto",
                )
            )

        summary = DatasetSummary(
            file_path=Path(self.current_file_path)
            if self.current_file_path and ";" not in self.current_file_path
            else None,
            row_count=int(len(df)),
            column_count=int(len(df.columns)),
            years=[],
            chapters=self._collect_unique_values(df, chapter_column) if chapter_column else [],
            difficulties=[],
        )

        return AnalysisResult(
            summary=summary,
            keyword_counts=keyword_counts,
            yearly_counts={},
            chapter_counts=chapter_counts,
            difficulty_counts={},
            average_difficulty_by_year={},
            issues=issues,
            keyword_rows=keyword_rows,
            bigrams={},
            trigrams={},
            tfidf=[],
            similar_pairs=similar_pairs,
            analysis_status=analysis_status,
            skipped_analyses=skipped_analyses,
            chapter_source=chapter_source,
            chapter_distribution=chapter_distribution,
        )

    def detect_question_column(self, dataframe: pd.DataFrame | None = None) -> str:
        df = dataframe if dataframe is not None else self.current_dataframe

        if df is None or df.empty:
            raise ValueError("분석 가능한 데이터가 없습니다.")

        for column in QUESTION_COLUMN_CANDIDATES:
            if column in df.columns:
                return str(column)

        object_columns = list(df.select_dtypes(include=["object"]).columns)
        if object_columns:
            return str(object_columns[0])

        if len(df.columns) > 0:
            return str(df.columns[0])

        raise ValueError("분석 가능한 컬럼이 없습니다.")

    def _ensure_chapter_column(
        self,
        dataframe: pd.DataFrame,
        question_column: str,
    ) -> tuple[str | None, str]:
        if "chapter" in dataframe.columns and dataframe["chapter"].notna().any():
            return "chapter", "provided"

        if "chapter_auto" in dataframe.columns and dataframe["chapter_auto"].notna().any():
            return "chapter_auto", "provided_auto"

        classifier = ChapterClassifier()
        dataframe["chapter_auto"] = [
            classifier.classify(text)
            for text in dataframe[question_column].fillna("").astype(str)
        ]

        if dataframe["chapter_auto"].notna().any():
            return "chapter_auto", "keyword_auto"

        return None, "none"

    def _attach_filename_metadata(self, dataframe: pd.DataFrame, path: str | Path) -> pd.DataFrame:
        df = dataframe.copy()
        metadata = extract_metadata_from_filename(path)

        df["source_file"] = metadata.source_file

        if "exam_round" not in df.columns:
            df["exam_round"] = metadata.exam_round

        if "month" not in df.columns:
            df["month"] = metadata.month

        if "exam_name" not in df.columns:
            df["exam_name"] = metadata.exam_name

        return df

    def _enrich_similar_pairs(
        self,
        pairs: list[dict[str, object]],
        dataframe: pd.DataFrame,
        question_column: str,
    ) -> list[dict[str, object]]:
        """Attach readable question/source fields and remove meaningless pairs."""
        enriched: list[dict[str, object]] = []

        for pair in pairs:
            idx1 = int(pair.get("question_index_1", -1))
            idx2 = int(pair.get("question_index_2", -1))

            if idx1 == idx2:
                continue

            row1 = self._safe_row(dataframe, idx1)
            row2 = self._safe_row(dataframe, idx2)

            if self._is_same_exam_question(row1, row2):
                continue

            pair = dict(pair)
            pair["question_1_text"] = self._short_text(row1.get(question_column, ""), 220)
            pair["question_2_text"] = self._short_text(row2.get(question_column, ""), 220)
            pair["question_1_source"] = self._source_label(row1)
            pair["question_2_source"] = self._source_label(row2)

            enriched.append(pair)

        return enriched

    def _is_same_exam_question(
        self,
        row1: dict[str, Any],
        row2: dict[str, Any],
    ) -> bool:
        """Filter same exam item comparisons from similar-question results."""
        if not row1 or not row2:
            return False

        source1 = self._normalize_meta_value(row1.get("source_file"))
        source2 = self._normalize_meta_value(row2.get("source_file"))
        qno1 = self._normalize_meta_value(row1.get("question_no"))
        qno2 = self._normalize_meta_value(row2.get("question_no"))

        if source1 and source2 and qno1 and qno2:
            if source1 == source2 and qno1 == qno2:
                return True

        year1 = self._normalize_meta_value(row1.get("year"))
        year2 = self._normalize_meta_value(row2.get("year"))
        round1 = self._normalize_meta_value(row1.get("exam_round"))
        round2 = self._normalize_meta_value(row2.get("exam_round"))

        if year1 and year2 and round1 and round2 and qno1 and qno2:
            if year1 == year2 and round1 == round2 and qno1 == qno2:
                return True

        return False

    def _normalize_meta_value(self, value: object) -> str:
        if value is None:
            return ""

        text = str(value).strip()

        if not text or text.lower() == "nan":
            return ""

        if text.endswith(".0"):
            text = text[:-2]

        return text

    def _safe_row(self, dataframe: pd.DataFrame, index: int) -> dict[str, Any]:
        if index < 0 or index >= len(dataframe):
            return {}

        return dataframe.iloc[index].to_dict()

    def _source_label(self, row: dict[str, Any]) -> str:
        parts: list[str] = []

        for key in ["source_file", "exam_name"]:
            value = row.get(key)
            if value is not None and str(value).strip() and str(value) != "nan":
                parts.append(str(value))

        page = row.get("source_page")
        if page is not None and str(page).strip() and str(page) != "nan":
            parts.append(f"p.{page}")

        question_no = row.get("question_no")
        if question_no is not None and str(question_no).strip() and str(question_no) != "nan":
            parts.append(f"{question_no}번")

        return " / ".join(parts) if parts else "-"

    def _short_text(self, text: object, limit: int = 180) -> str:
        value = "" if text is None else str(text)
        value = " ".join(value.split())

        if len(value) <= limit:
            return value

        return value[:limit].rstrip() + "..."

    def _validate_for_ui(
        self,
        dataframe: pd.DataFrame,
        question_column: str,
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []

        empty_mask = dataframe[question_column].fillna("").astype(str).str.strip().eq("")
        for index in dataframe.index[empty_mask].tolist()[:200]:
            issues.append(
                ValidationIssue(
                    level="warning",
                    code="EMPTY_QUESTION",
                    row_index=int(index) if isinstance(index, int) else None,
                    column=question_column,
                    message="문항 본문이 비어 있습니다.",
                )
            )

        if dataframe.duplicated(subset=[question_column]).any():
            dup_count = int(dataframe.duplicated(subset=[question_column]).sum())
            issues.append(
                ValidationIssue(
                    level="warning",
                    code="DUPLICATE_QUESTION",
                    message=f"중복 문항 후보가 {dup_count}개 있습니다.",
                    column=question_column,
                )
            )

        return issues

    def _collect_unique_values(
        self,
        dataframe: pd.DataFrame,
        column: str | None,
        as_int: bool = False,
    ) -> list:
        if not column or column not in dataframe.columns:
            return []

        values = dataframe[column].dropna().unique().tolist()

        if as_int:
            result = []
            for value in values:
                try:
                    result.append(int(value))
                except Exception:
                    continue
            return sorted(set(result))

        return sorted({str(value) for value in values if str(value).strip()})

    def _value_counts(self, dataframe: pd.DataFrame, column: str) -> dict:
        if column not in dataframe.columns:
            return {}

        counts = dataframe[column].fillna("-").astype(str).value_counts()
        return {key: int(value) for key, value in counts.items()}

    def _chapter_distribution(
        self,
        dataframe: pd.DataFrame,
        chapter_column: str,
    ) -> list[dict[str, object]]:
        if chapter_column not in dataframe.columns or dataframe.empty:
            return []

        counts = dataframe[chapter_column].fillna("미분류").astype(str).value_counts()
        total = int(counts.sum())

        return [
            {
                "chapter": str(chapter),
                "count": int(count),
                "ratio": round((int(count) / total) * 100, 2) if total else 0.0,
            }
            for chapter, count in counts.items()
        ]
