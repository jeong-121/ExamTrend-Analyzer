# Design Document

## 1. 개요

ExamTrend Analyzer는 임의의 기출문제 파일을 분석하기 위한 PySide6 기반 데스크톱 애플리케이션이다.

## 2. 설계 방향

- 특정 과목에 종속되지 않는 범용 분석 구조
- UI, 서비스, 분석, 코어 계층 분리
- 고정 단원 분류 제거, 데이터 기반 자동 주제 분석 도입
- Kiwipiepy 미설치 환경에서도 정상 동작 (정규식 폴백)
- 분석 작업은 별도 스레드로 실행하여 UI 응답성 유지

## 3. 계층 구조

```text
Presentation Layer (ui/)
        ↓
Service Layer (services/)
        ↓
Analysis Layer (analysis/)
        ↓
Core Layer (core/, preprocessing/)
```

## 4. Presentation Layer

| 컴포넌트 | 역할 |
|---|---|
| MainWindow | 탭 전환, 파일 로드, 분석 실행, 보고서 저장 조율 |
| DashboardPage | 파일 상태, 문항 수 표시, 파일 로드·분석 실행 버튼 |
| AnalysisPage | 분석 결과 탭 뷰 (키워드, 자동 주제, 유사 문항, 시각화 등) |
| ReportPage | 보고서 미리보기 및 저장 |
| FieldMappingDialog | 수동 컬럼 매핑 다이얼로그 |
| FunctionWorker | QRunnable 기반 비동기 분석 실행 |

## 5. Service Layer

| 컴포넌트 | 역할 |
|---|---|
| AnalysisService | 파일 로드, 자동 매핑, 분석 실행 조율 |
| ReportService | AnalysisResult → Markdown 변환 및 파일 저장 |

AnalysisService는 분석 로직 내부를 직접 호출하지 않고 `AnalysisPipeline`에 위임한다.

## 6. Analysis Layer

| 컴포넌트 | 역할 |
|---|---|
| KeywordAnalyzer | 키워드 빈도·문서 빈도 계산 |
| NgramAnalyzer | 바이그램·트라이그램 추출 |
| TfidfAnalyzer | TF-IDF 기반 키워드 스코어링 |
| TopicAnalyzer | 데이터 기반 자동 주제 그룹 생성 |
| SimilarityAnalyzer | TF-IDF 코사인 유사도 기반 유사 문항 탐지 |
| TrendAnalyzer | 연도별 문항 수 집계 |
| DifficultyAnalyzer | 난이도 분포·연도별 평균 난이도 산출 |
| PatternAnalyzer | 반복 출제 패턴 탐지 |
| PredictionAnalyzer | 출제 예측 스코어링 |

## 7. Core Layer

| 컴포넌트 | 역할 |
|---|---|
| AnalysisPipeline | 분석기들을 순서대로 실행, AnalysisResult 반환 |
| FileLoader | CSV, Excel, PDF, TXT 통합 로드 |
| PdfQuestionLoader | PDF 텍스트 추출 및 문항 분리 |
| DatasetValidator | 필수 컬럼·데이터 품질 검증 |
| AnalysisResult | 분석 결과 데이터 모델 (dataclass) |
| DatasetSummary | 데이터셋 요약 정보 (dataclass) |
| FieldMapping | 컬럼 매핑 정보 (dataclass) |
| TextCleaner | 문항 텍스트 정제 |
| KoreanTokenizer | 한국어 토크나이저 (Kiwi / 정규식 폴백) |

## 8. 주요 설계 결정

### 고정 단원 분류 제거

특정 과목에 종속되는 `ChapterClassifier` 방식은 범용 기출 분석 목적에 맞지 않아 UI 흐름에서 제거하였다.  
`chapter_classifier.py`와 `chapter_analyzer.py`는 코드베이스에 존재하지만 기본 파이프라인에서는 사용하지 않는다.

### 자동 주제 분석 도입

`TopicAnalyzer`가 입력 데이터의 키워드에서 자동으로 주제 그룹을 생성한다.  
결과는 `AnalysisResult.topic_distribution` 및 `topic_keywords`로 UI와 보고서에 전달된다.

### DB 기능 미활성화

`database/` 패키지(`db_manager.py`, `models.py`)가 존재하지만 현재 버전의 UI에서는 사용하지 않는다.  
향후 이력 저장 기능 도입 시 활성화 예정이다.

### Kiwipiepy 선택적 의존

`KoreanTokenizer`는 Kiwipiepy 설치 여부를 런타임에 확인하고 미설치 시 정규식 기반 폴백으로 동작한다.  
이를 통해 설치 환경에 상관없이 최소한의 분석 품질을 보장한다.
