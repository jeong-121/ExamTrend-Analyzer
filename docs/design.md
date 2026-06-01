# Design Document

## 1. 문서 개요

### 1.1 목적

본 문서는 ExamTrend-Analyzer의 소프트웨어 설계를 정의한다.

시스템은 기출문제 데이터를 분석하여 출제 경향을 파악하고 반복 출제 패턴을 탐지하기 위한 데스크톱 애플리케이션이다.

---

# 2. 설계 원칙

본 시스템은 다음 원칙을 따른다.

## 2.1 계층 분리

UI 계층과 분석 계층을 분리한다.

---

## 2.2 모듈화

각 기능은 독립적인 모듈로 구성한다.

---

## 2.3 확장성

새로운 분석기를 쉽게 추가할 수 있도록 설계한다.

---

## 2.4 유지보수성

비즈니스 로직과 화면 로직을 분리한다.

---

# 3. 전체 구조

```text
Presentation Layer
        │
        ▼
Service Layer
        │
        ▼
Analysis Layer
        │
        ▼
Core Layer
```

---

# 4. Presentation Layer

## 4.1 MainWindow

애플리케이션의 최상위 창

### 역할

* 메뉴 관리
* 탭 관리
* 페이지 전환
* 이벤트 처리

---

## 4.2 DashboardPage

초기 화면

### 역할

* 파일 불러오기
* 분석 실행
* 상태 표시

### 제공 기능

```text
기출문제 파일 불러오기
분석 실행
문항 수 표시
분석 상태 표시
```

---

## 4.3 AnalysisPage

분석 결과 표시 화면

### 역할

* 키워드 결과 표시
* 단원 분석 결과 표시
* 유사 문항 표시
* 시각화 표시

---

## 4.4 ReportPage

보고서 생성 화면

### 역할

* 보고서 미리보기
* 보고서 저장

---

# 5. Service Layer

## 5.1 AnalysisService

시스템 핵심 서비스

### 역할

```text
파일 분석
데이터 정제
분석 실행
결과 생성
```

---

### 주요 메서드

```python
preview_file()
preview_files()

auto_apply_mapping()

analyze_current()

run_analysis()
```

---

## 5.2 ReportService

보고서 생성 서비스

### 역할

```text
Markdown 생성
TXT 생성
파일 저장
```

---

# 6. Analysis Layer

## 6.1 KeywordAnalyzer

키워드 분석기

### 입력

```text
문항 텍스트
```

### 출력

```text
키워드 빈도
```

---

## 6.2 SimilarityAnalyzer

유사 문항 분석기

### 입력

```text
문항 텍스트
```

### 처리

```text
벡터화
코사인 유사도 계산
```

### 출력

```text
유사 문항 목록
```

---

## 6.3 ChapterClassifier

단원 자동 분류기

### 입력

```text
문항 텍스트
```

### 출력

```text
단원명
```

예시

```text
SQL
정규화

→ 데이터베이스
```

---

# 7. Core Layer

## 7.1 FileLoader

파일 로딩 담당

### 지원 형식

```text
PDF
CSV
XLS
XLSX
TXT
```

---

## 7.2 PDF Extractor

PDF 전용 처리 모듈

### 역할

```text
텍스트 추출
페이지 추출
문항 추출
```

---

## 7.3 Models

데이터 모델 정의

---

### AnalysisResult

분석 결과 저장

```text
키워드 결과
단원 결과
유사 문항 결과
검증 결과
```

---

### DatasetSummary

데이터 요약 정보

```text
문항 수
파일 정보
단원 수
```

---

### ValidationIssue

검증 결과

```text
Error
Warning
Info
```

---

# 8. UI 구성

## Dashboard

```text
+--------------------------------+

기출문제 파일 불러오기

분석 실행

현재 파일

문항 수

+--------------------------------+
```

---

## Analysis

```text
+--------------------------------+

요약

키워드

단원별 분석

유사 문항

시각화

+--------------------------------+
```

---

## Report

```text
+--------------------------------+

보고서 미리보기

보고서 저장

+--------------------------------+
```

---

# 9. 데이터 흐름

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

AnalysisPage

 ↓

ReportPage
```

---

# 10. 예외 처리

## 파일 없음

```text
분석할 데이터가 없습니다.
```

---

## 잘못된 형식

```text
지원하지 않는 파일 형식입니다.
```

---

## PDF 추출 실패

```text
PDF 분석 실패
```

---

## 컬럼 탐지 실패

```text
수동 매핑이 필요합니다.
```

---

# 11. 향후 확장 계획

## 분석 기능

* 연도별 출제 경향
* 문제 유형 분류
* 난이도 분석
* 출제 예측

---

## 데이터 처리

* OCR 지원
* 이미지 기반 PDF 지원

---

## 배포

* 웹 버전
* 클라우드 버전

---

## AI 기능

* LLM 기반 단원 분류
* 자동 요약
* 자동 문제 생성
* 출제 가능성 예측

```
```
