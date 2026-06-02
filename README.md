# ExamTrend Analyzer

**기출문제 기반 출제 경향 분석 시스템**

ExamTrend Analyzer는 기출문제 데이터를 분석하여 키워드 빈도, 자동 주제 그룹, 유사 문항 패턴을 파악하는 Python 기반 데스크톱 애플리케이션입니다.  
PDF, Excel, CSV, TXT 파일을 불러와 자동으로 분석하고 Markdown 보고서를 생성합니다.

---

## 1. 프로젝트 개요

시험 대비 과정에서 과거 기출문제를 분석하여 자주 출제되는 개념, 출제 비중, 반복 출제 패턴을 파악하는 것은 효율적인 학습 전략 수립에 핵심적입니다.  
ExamTrend Analyzer는 이러한 분석 과정을 자동화하여 사용자가 기출문제 데이터를 기반으로 학습 전략을 수립할 수 있도록 지원합니다.

입력된 문항 데이터에서 자주 등장하는 키워드를 기반으로 자동 주제 그룹을 생성합니다.  
따라서 다양한 시험에 범용적으로 적용할 수 있습니다.

---

## 2. 주요 기능

### 2.1 파일 불러오기

- **지원 형식**: PDF, CSV, XLSX, XLS, TXT
- **다중 파일 병합**: 여러 파일을 동시에 선택하여 통합 분석
- **자동 컬럼 매핑**: 파일의 열 이름을 자동으로 표준 필드에 매핑
- **수동 매핑**: 자동 매핑 실패 시 사용자가 직접 필드 지정
- **파일명 메타데이터 추출**: 파일명에서 연도, 회차, 시험명 자동 인식

### 2.2 텍스트 전처리

- 특수문자 제거 및 공백 정규화
- 한국어 형태소 분석 (Kiwipiepy 사용 가능, 미설치 시 정규식 폴백)
- 조사·어미·지시문 표현 불용어 제거
- 영문 토큰 대문자 정규화

### 2.3 분석 기능

- **키워드 분석**: 빈도, 문서 빈도 계산 및 상위 키워드 추출
- **N-Gram 분석**: 바이그램·트라이그램 기반 공출현 패턴 탐지
- **TF-IDF 분석**: 문서 중요도 기반 핵심 키워드 스코어링
- **자동 주제 분석**: 입력 데이터의 키워드를 기반으로 주제 그룹 자동 생성
- **자동 주제별 출제 비중**: 주제별 문항 수 및 비율(%) 계산
- **유사 문항 탐지**: TF-IDF 코사인 유사도 기반 유사 문항 쌍 탐지

### 2.4 시각화

- 상위 키워드 빈도 수평 막대 그래프
- 자동 주제별 출제 비중 파이 차트
- PySide6 화면 내 인라인 렌더링 (matplotlib 기반)
- 한글 폰트 자동 탐지 및 적용

### 2.5 보고서 생성

- Markdown(.md) 및 TXT(.txt) 형식으로 저장
- 분석 상태, 키워드 결과, 자동 주제별 비중, 유사 문항, 검증 이슈 포함

---

## 3. 기술 스택

| 구분 | 기술 |
|---|---|
<<<<<<< HEAD
| Language | Python 3.10 이상 |
| GUI | PySide6 >= 6.6.0 |
| Data Analysis | pandas >= 2.0.0 |
| NLP | kiwipiepy >= 0.18.0 (선택), scikit-learn >= 1.3.0 |
| Visualization | matplotlib >= 3.7.0 |
| PDF 처리 | PyMuPDF (fitz) |
| Spreadsheet | openpyxl >= 3.1.0 |
| Testing | pytest >= 8.0.0 |
=======
| 프로젝트명 | ExamTrend Analyzer |
| 플랫폼 | Python 기반 데스크탑 애플리케이션 |
| GUI 프레임워크 | PySide6 |
| 개발 언어 | Python 3.11 이상 |
| 핵심 기술 | 텍스트 마이닝, 자연어 처리, 데이터 시각화 |
| 제약 조건 | LLM API 사용 금지 · 완전 오프라인 구동 |

### 핵심 가치

- **객관적 분석** — 감이 아닌 데이터로 출제 경향 파악
- **반복 패턴 탐지** — 코사인 유사도 기반 유사 문항 자동 탐지
- **다양한 입력** — PDF, CSV, Excel, TXT 다중 파일 병합 분석
- **완전 독립 구동** — LLM API 없이 순수 통계·NLP만으로 동작
>>>>>>> 6c516b727c31bf690a62e07ca6c4482197ecebb2

---

## 4. 설치 방법

### 4.1 저장소 클론

```bash
git clone https://github.com/your-username/ExamTrend-Analyzer.git
cd ExamTrend-Analyzer
```

### 4.2 가상환경 생성 및 활성화

```bash
python -m venv .venv
```

Windows (Git Bash):

```bash
source .venv/Scripts/activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```
```bash
python -m pip install --upgrade pip
```

### 4.3 의존성 설치

```bash
pip install -r requirements.txt
```

### 4.4 한국어 형태소 분석기 설치 (선택)

Kiwipiepy를 설치하면 더 정확한 키워드 추출이 가능합니다. 미설치 시 정규식 기반 토크나이저로 자동 대체됩니다.

```bash
pip install kiwipiepy
```

---

## 5. 실행 방법

```bash
python run.py
```

또는

```bash
python -m examtrend_analyzer.main
```

---

## 6. 테스트 실행

```bash
pytest
```

---

## 7. 사용 방법

### Step 1. 파일 불러오기

Dashboard 화면에서 **기출문제 파일 불러오기** 버튼을 클릭합니다.  
PDF, CSV, Excel, TXT 파일을 단독 또는 다중 선택할 수 있습니다.

```
예시
2023_1회.pdf
2024_1회.pdf
2025_1회.pdf
→ 3개 파일 병합, 총 문항 수: 180
```

### Step 2. 컬럼 매핑 확인

시스템이 파일의 열 이름을 자동으로 표준 필드에 매핑합니다.  
매핑에 실패한 경우 수동 매핑 다이얼로그가 나타납니다.

### Step 3. 분석 실행

Dashboard에서 **분석 실행** 버튼을 클릭합니다.  
분석 완료 후 Analysis 탭으로 자동 이동합니다.

### Step 4. 결과 확인

Analysis 탭에서 아래 항목을 탭으로 확인합니다.

| 탭 | 내용 |
|---|---|
| 요약 | 분석 상태 및 개요 |
| 키워드 | 상위 키워드 빈도 |
| 자동 주제 | 자동 주제별 문항 수 및 출제 비중 |
| 주제 키워드 | 자동 주제별 대표 키워드 |
| 유사 문항 | 유사도 0.55 이상 문항 쌍 목록 |
| 검증/경고 | 데이터 품질 이슈 목록 |
| 시각화 | 키워드 차트, 자동 주제 파이 차트 |

### Step 5. 보고서 저장

Report 탭에서 **Markdown 보고서 저장** 버튼을 클릭하여 분석 결과를 저장합니다.

---

## 8. 입력 파일 형식

### CSV / Excel

아래 열 이름을 권장합니다. 다른 이름도 자동 매핑을 시도합니다.

| 필드 | 설명 | 필수 여부 |
|---|---|---|
| question_text | 문항 본문 | **필수** |
| year | 출제 연도 | 선택 |
| chapter | 단원 | 선택 |
| difficulty | 난이도 (상/중/하) | 선택 |
| answer | 정답 | 선택 |
| question_type | 문제 유형 | 선택 |
| subject | 과목 | 선택 |
| exam_name | 시험명 | 선택 |
| exam_round | 회차 | 선택 |
| question_id | 문항 ID | 선택 |

예시 (`sample_data/sample_questions.csv`)

| year | chapter | difficulty | question_text | answer |
|---|---|---|---|---|
| 2024 | 데이터베이스 | 중 | SQL의 기본 명령어에 대한 설명으로 옳은 것은? | ② |

### PDF

텍스트 기반 PDF에서 문항 번호(예: `1.`, `2.`) 패턴으로 문항을 자동 분리합니다.  
스캔 이미지 PDF는 지원하지 않습니다.

---

## 9. 자동 주제 분석

chapter 컬럼 여부와 상관없이, 시스템은 입력 문항의 키워드에서 자동으로 주제 그룹을 생성합니다.  
주제명은 고정된 단원명이 아니라 데이터에서 추출된 대표 키워드로 구성됩니다.

예시:

```text
주제 1: SQL, 정규화, 트랜잭션
주제 2: 통신, 프로토콜, 네트워크
주제 3: 프로세스, 스레드, 스케줄링
```

---

## 10. 디렉토리 구조

```text
ExamTrend-Analyzer/
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_STYLE.md
├── ISSUE_TEMPLATE.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── run.py
├── examtrend.db
├── data/
├── reports/
├── docs/
│   ├── requirements.md
│   ├── design.md
│   ├── architecture.md
│   ├── analysis_spec.md
│   ├── test_plan.md
│   ├── manual.md
│   ├── user_manual.md
│   ├── deployment.md
│   ├── meeting_log.md
│   └── project_log.md
└── src/
    └── examtrend_analyzer/
        ├── __init__.py
        ├── main.py
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
        │   │   ├── dashboard_page.py
        │   │   ├── analysis_page.py
        │   │   └── report_page.py
        │   ├── dialogs/
        │   │   └── field_mapping_dialog.py
        │   └── widgets/
        │       ├── chart_canvas.py
        │       └── summary_card.py
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

---

## 11. 오류 해결

| 오류 | 원인 | 해결 방법 |
|---|---|---|
| 파일 로드 실패 | 지원하지 않는 형식 또는 손상된 파일 | 파일 확인 후 재시도 |
| 분석 실행 불가 | 파일 미선택 | 파일 로드 후 재실행 |
| PDF 분석 실패 | 스캔 이미지 PDF (텍스트 추출 불가) | 텍스트 기반 PDF 사용 |
| 한글 깨짐 | 시스템 폰트 미설치 | 한글 폰트(나눔고딕 등) 설치 |
| 자동 매핑 실패 | 컬럼명 미인식 | 수동 매핑 다이얼로그에서 직접 지정 |
| PyMuPDF 없음 | PDF 처리 라이브러리 미설치 | `pip install PyMuPDF` 실행 |

---

## 12. 개발 원칙

- UI, 서비스, 분석, 전처리, 코어 계층 분리
- UI는 분석 로직에 직접 의존하지 않음
- 분석 작업은 별도 스레드(`QThreadPool`)로 실행하여 UI 응답성 유지
- 원본 데이터는 변경하지 않고 복사본에서 처리
- Kiwipiepy 미설치 환경에서도 정규식 폴백으로 정상 동작
- 특정 과목 사전에 의존하지 않는 범용 분석 구조

---

## 13. 라이선스

본 프로젝트는 MIT License를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참고하십시오.
