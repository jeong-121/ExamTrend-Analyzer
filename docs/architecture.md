# Software Architecture Document

## 1. 문서 개요

### 1.1 목적

본 문서는 ExamTrend-Analyzer의 소프트웨어 아키텍처를 정의한다.

본 시스템은 다양한 형식의 기출문제 데이터를 수집하고 분석하여 출제 경향을 파악하기 위한 데스크톱 기반 분석 시스템이다.

---

# 2. 아키텍처 개요

ExamTrend-Analyzer는 Layered Architecture를 기반으로 설계되었다.

각 계층은 독립적으로 동작하며 상위 계층은 하위 계층에만 의존한다.

---

## 2.1 아키텍처 구조

```text
┌─────────────────────────────┐
│      Presentation Layer     │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│        Service Layer        │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│       Analysis Layer        │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│         Core Layer          │
└─────────────────────────────┘
```

---

# 3. 계층별 구조

## 3.1 Presentation Layer

사용자 인터페이스를 담당한다.

### 구성요소

```text
MainWindow
DashboardPage
AnalysisPage
ReportPage
```

---

### MainWindow

애플리케이션 진입점

역할

```text
UI 초기화
이벤트 연결
페이지 전환
상태 표시
```

---

### DashboardPage

역할

```text
파일 로드
분석 실행
상태 확인
```

---

### AnalysisPage

역할

```text
분석 결과 표시
차트 표시
유사 문항 표시
```

---

### ReportPage

역할

```text
보고서 미리보기
보고서 저장
```

---

# 4. Service Layer

비즈니스 로직을 담당한다.

---

## 4.1 AnalysisService

시스템 핵심 서비스

### 책임

```text
파일 전처리
자동 매핑
분석 실행
결과 생성
```

---

### 의존 모듈

```text
FileLoader
KeywordAnalyzer
SimilarityAnalyzer
ChapterClassifier
```

---

## 4.2 ReportService

보고서 생성 담당

### 책임

```text
Markdown 생성
TXT 생성
파일 저장
```

---

# 5. Analysis Layer

실제 분석 알고리즘을 담당한다.

---

## 5.1 KeywordAnalyzer

### 입력

```text
문항 텍스트
```

### 출력

```text
키워드 빈도
```

---

## 5.2 ChapterClassifier

### 입력

```text
문항 텍스트
```

### 출력

```text
단원명
```

---

### 분류 단원

```text
데이터베이스
운영체제
네트워크
자료구조
알고리즘
인공지능
소프트웨어공학
미분류
```

---

## 5.3 SimilarityAnalyzer

### 입력

```text
문항 텍스트
```

### 출력

```text
유사 문항 목록
```

---

### 처리 방식

```text
텍스트 벡터화
Cosine Similarity 계산
Threshold 적용
```

---

# 6. Core Layer

데이터 처리 및 공통 기능 담당

---

## 6.1 FileLoader

지원 형식

```text
PDF
CSV
XLS
XLSX
TXT
```

---

### 역할

```text
파일 읽기
데이터프레임 생성
전처리
```

---

## 6.2 PDF Extractor

### 역할

```text
PDF 텍스트 추출
페이지 추출
문항 추출
```

---

## 6.3 Schema

### 역할

```text
자동 컬럼 매핑
필드 검증
```

---

## 6.4 Models

### 역할

```text
데이터 모델 정의
```

---

### 주요 모델

```text
AnalysisResult
DatasetSummary
ValidationIssue
```

---

# 7. 패키지 구조

```text
src/
└── examtrend_analyzer
    ├── analysis
    │   ├── keyword_analyzer.py
    │   ├── similarity_analyzer.py
    │   └── chapter_classifier.py
    │
    ├── core
    │   ├── file_loader.py
    │   ├── models.py
    │   └── schema.py
    │
    ├── services
    │   ├── analysis_service.py
    │   └── report_service.py
    │
    ├── ui
    │   ├── main_window.py
    │   ├── pages
    │   ├── dialogs
    │   └── widgets
    │
    └── utils
```

---

# 8. 데이터 흐름

## 8.1 파일 분석 흐름

```text
사용자

 ↓

파일 선택

 ↓

FileLoader

 ↓

AnalysisService

 ↓

KeywordAnalyzer

 ↓

ChapterClassifier

 ↓

SimilarityAnalyzer

 ↓

AnalysisResult

 ↓

UI 출력
```

---

## 8.2 보고서 생성 흐름

```text
AnalysisResult

 ↓

ReportService

 ↓

Markdown 생성

 ↓

파일 저장
```

---

# 9. 의존성 규칙

각 계층은 아래 방향으로만 의존할 수 있다.

```text
Presentation
    ↓

Service
    ↓

Analysis
    ↓

Core
```

허용되지 않는 의존성

```text
Core → UI

Analysis → UI

Core → Service
```

---

# 10. 스레드 구조

분석 작업은 UI 스레드와 분리하여 수행한다.

---

## 목적

```text
GUI 프리징 방지
대용량 PDF 처리
백그라운드 분석
```

---

## 구조

```text
Main Thread
    │
    ├─ UI 처리
    │
    └─ Worker Thread
           │
           └─ 분석 수행
```

---

# 11. 예외 처리 구조

## 파일 오류

```text
파일 없음
지원하지 않는 형식
손상된 파일
```

---

## 분석 오류

```text
문항 컬럼 없음
데이터 없음
분석 실패
```

---

## PDF 오류

```text
텍스트 추출 실패
페이지 파싱 실패
```

---

# 12. 향후 확장 구조

향후 아래 모듈을 추가할 수 있도록 설계한다.

```text
YearTrendAnalyzer
DifficultyAnalyzer
QuestionTypeAnalyzer
OCRExtractor
AIClassifier
PredictionEngine
```

---

# 13. 아키텍처 결정 사항

## ADR-001

PyQt 대신 PySide6 사용

이유

```text
상업적 사용 제약 최소화
Qt 공식 지원
```

---

## ADR-002

DB 저장 기능 제거

이유

```text
현재 요구사항에 불필요
복잡도 증가 방지
```

---

## ADR-003

자동 매핑 우선 적용

이유

```text
사용자 편의성 향상
초기 설정 최소화
```

---

## ADR-004

단원 분류는 키워드 사전 기반 사용

이유

```text
구현 단순성
설명 가능성 확보
```
