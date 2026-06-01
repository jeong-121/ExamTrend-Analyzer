# Software Architecture Document

## 1. 아키텍처 개요

ExamTrend Analyzer는 계층형 아키텍처를 따른다.

```text
Presentation Layer (PySide6 UI)
            ↓
    Service Layer
  (AnalysisService / ReportService)
            ↓
    Analysis Layer
  (KeywordAnalyzer / NgramAnalyzer / TfidfAnalyzer /
   TopicAnalyzer / SimilarityAnalyzer /
   TrendAnalyzer / DifficultyAnalyzer /
   PatternAnalyzer / PredictionAnalyzer)
            ↓
    Core Layer
  (AnalysisPipeline / FileLoader / Models / Schema / Validation)
            ↓
    AnalysisResult
            ↓
    ReportService
```

## 2. 패키지 구조

```text
src/examtrend_analyzer/
├── config/
│   └── settings.py
├── core/
│   ├── file_loader.py
│   ├── pdf_loader.py
│   ├── pipeline.py
│   ├── models.py
│   ├── schema.py
│   └── validation.py
├── preprocessing/
│   ├── text_cleaner.py
│   ├── tokenizer.py
│   └── stopwords.py
├── analysis/
│   ├── keyword_analyzer.py
│   ├── ngram_analyzer.py
│   ├── tfidf_analyzer.py
│   ├── similarity_analyzer.py
│   ├── topic_analyzer.py
│   ├── trend_analyzer.py
│   ├── difficulty_analyzer.py
│   ├── pattern_analyzer.py
│   ├── prediction_analyzer.py
│   ├── chapter_analyzer.py
│   └── chapter_classifier.py
├── services/
│   ├── analysis_service.py
│   ├── database_service.py
│   └── report_service.py
├── ui/
│   ├── main_window.py
│   ├── workers.py
│   ├── pages/
│   ├── widgets/
│   └── dialogs/
├── visualization/
│   ├── graph_generator.py
│   ├── heatmap_generator.py
│   └── wordcloud_generator.py
├── database/
│   ├── db_manager.py
│   └── models.py
└── utils/
    ├── filename_metadata.py
    ├── file_loader.py
    ├── plot_font.py
    └── logger.py
```

## 3. 주요 컴포넌트

### AnalysisService

파일 로드, 자동 컬럼 매핑, 분석 실행을 조율하는 중심 서비스이다.  
`preview_file` / `preview_files`로 파일을 미리 로드하고, `analyze_current`로 분석을 실행한다.  
마지막 분석 결과는 `last_result`에 보관한다.

### AnalysisPipeline

`core/pipeline.py`에 정의된 파이프라인 클래스이다.  
Validator → TextCleaner → KoreanTokenizer → 각 분석기 순서로 실행하고 `AnalysisResult`를 반환한다.

### TopicAnalyzer

특정 과목의 단원 사전 없이 입력 문항의 키워드를 기반으로 자동 주제 그룹을 생성한다.  
결과는 `topic_counts`, `topic_distribution`, `topic_keywords` 필드에 담긴다.

### AnalysisResult

분석 결과를 UI와 보고서에 전달하는 불변 데이터 모델(`dataclass`)이다.  
`summary`, `keyword_counts`, `yearly_counts`, `chapter_counts`, `difficulty_counts`,  
`bigrams`, `trigrams`, `tfidf`, `similar_pairs`, `topic_distribution`, `topic_keywords` 등을 포함한다.

### FileLoader

CSV, Excel, PDF, TXT 파일을 통합 로드하고 `source_file`, `year` 등의 메타데이터를 자동 추가한다.  
PDF는 `PdfQuestionLoader`에 위임한다.

### ReportService

`AnalysisResult`를 Markdown 보고서 텍스트로 변환하고 파일로 저장한다.

## 4. 데이터 흐름

```text
사용자 파일 선택 (QFileDialog)
        ↓
FileLoader.load()
        ↓
AnalysisService.preview_file() → suggest_field_mapping()
        ↓
자동 매핑 성공 → auto_apply_mapping()
자동 매핑 실패 → FieldMappingDialog (수동 매핑)
        ↓
AnalysisService.analyze_current() [별도 스레드]
        ↓
AnalysisPipeline.run()
  - DatasetValidator
  - TextCleaner
  - KoreanTokenizer
  - KeywordAnalyzer / NgramAnalyzer / TfidfAnalyzer
  - SimilarityAnalyzer
  - TrendAnalyzer / DifficultyAnalyzer
        ↓
AnalysisResult
        ↓
DashboardPage / AnalysisPage / ReportPage 갱신
```

## 5. 스레딩 모델

분석 작업은 `FunctionWorker` (QRunnable 기반)를 통해 `QThreadPool`에서 실행된다.  
완료 시 `signals.finished` 시그널을 통해 메인 스레드의 UI를 갱신한다.  
UI는 분석 중 로딩 상태로 전환되며, 완료 또는 실패 시 복원된다.

## 6. 주요 설계 결정

### 고정 단원 분류 제거

특정 과목에 종속되는 `ChapterClassifier` 방식은 범용 기출 분석 목적에 맞지 않아 제거하였다.

### 자동 주제 분석 도입

`TopicAnalyzer`가 입력 데이터에서 자주 등장하는 키워드를 기반으로 주제 그룹을 생성한다.

### Kiwipiepy 선택적 의존

`KoreanTokenizer`는 Kiwipiepy 설치 여부를 런타임에 확인하고, 미설치 시 정규식 기반 폴백으로 동작한다.

### DB 기능 미활성화

`database/` 패키지가 존재하지만 현재 버전의 UI에서는 DB 저장 및 불러오기를 제공하지 않는다.
