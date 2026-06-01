# ExamTrend Analyzer

**기출문제 기반 출제 경향 분석 시스템**

ExamTrend Analyzer는 기출문제 데이터를 분석하여 시험 출제 경향, 키워드 빈도, 단원별 비중, 난이도 변화 등을 시각화하는 Python 기반 Desktop Application입니다.  
소프트웨어공학 텀 프로젝트를 기준으로 설계되었으며, 기능 확장과 유지보수를 고려한 표준 Python 프로젝트 구조를 따릅니다.

---

## 1. 프로젝트 개요

시험 대비 과정에서는 과거 기출문제를 분석하여 자주 출제되는 개념, 단원별 비중, 난이도 변화, 반복 출제 패턴을 파악하는 것이 중요합니다.  
ExamTrend Analyzer는 이러한 분석 과정을 자동화하여 사용자가 기출문제 데이터를 기반으로 학습 전략을 수립할 수 있도록 지원합니다.

본 프로젝트는 다음과 같은 데이터를 분석 대상으로 합니다.

- 기출문제 문항 텍스트
- 출제 연도
- 단원 또는 주제
- 문제 유형
- 난이도
- 정답 및 해설
- 키워드 정보

---

## 2. 주요 기능

### 2.1 기출문제 데이터 관리

- CSV, Excel, JSON 등 다양한 형식의 기출문제 데이터 불러오기
- SQLite 기반 로컬 데이터 저장
- 문제, 단원, 키워드, 난이도 정보 관리

### 2.2 텍스트 전처리

- 불필요한 특수문자 제거
- 공백 정규화
- 한국어 형태소 분석
- 불용어 제거
- 키워드 추출을 위한 토큰화

### 2.3 분석 기능

- 키워드 빈도 분석
- 연도별 출제 경향 분석
- 단원별 출제 비중 분석
- 반복 출제 패턴 분석
- 난이도 변화 분석

### 2.4 시각화 기능

- 키워드 빈도 그래프
- 단원별 비중 차트
- 연도별 출제 추이 그래프
- 난이도 변화 그래프
- 히트맵 기반 패턴 시각화
- 워드클라우드 생성

### 2.5 Desktop UI

- PySide6 기반 데스크톱 애플리케이션
- 데이터 불러오기 화면
- 분석 결과 대시보드
- 그래프 및 보고서 출력 화면

### 2.6 구조 개편 기준

- `ui`: PySide6 화면과 위젯만 담당
- `services`: UI와 분석/DB/보고서 로직 사이의 응용 서비스 계층
- `analysis`: 순수 분석 알고리즘
- `preprocessing`: 텍스트 정제와 토큰화
- `visualization`: 그래프 생성
- `database`: SQLite 연결과 데이터 모델

---

## 3. 기술 스택

| 구분 | 기술 |
|---|---|
| Language | Python |
| GUI | PySide6 |
| Data Analysis | pandas |
| Visualization | matplotlib |
| Database | SQLite |
| Korean NLP | kiwipiepy |
| Testing | pytest |

---

## 4. 설치 방법

### 4.1 저장소 클론

```bash
git clone https://github.com/your-username/ExamTrend-Analyzer.git
cd ExamTrend-Analyzer
```

### 4.2 가상환경 생성

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 4.3 의존성 설치

```bash
pip install -r requirements.txt
```

---

## 5. 실행 방법

현재 구조는 PySide6 기반 데스크톱 앱 진입점과 기본 화면을 제공합니다.

```bash
python -m examtrend_analyzer.main
```

개발 중에는 다음 명령을 사용할 수 있습니다.

```bash
python src/examtrend_analyzer/main.py
```

---

## 6. 테스트 실행

```bash
pytest
```

테스트 코드는 `tests/` 디렉토리에 작성합니다.

---

## 7. 디렉토리 구조

```text
ExamTrend-Analyzer/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── CODE_STYLE.md
├── ISSUE_TEMPLATE.md
├── docs/
│   ├── requirements.md
│   ├── design.md
│   ├── test_plan.md
│   └── meeting_log.md
├── sample_data/
│   └── sample_questions.csv
├── reports/
│   └── .gitkeep
├── src/
│   └── examtrend_analyzer/
│       ├── __init__.py
│       ├── main.py
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── main_window.py
│       │   ├── pages/
│       │   │   ├── __init__.py
│       │   │   ├── dashboard_page.py
│       │   │   ├── analysis_page.py
│       │   │   └── report_page.py
│       │   └── widgets/
│       │       ├── __init__.py
│       │       └── summary_card.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── analysis_service.py
│       │   ├── database_service.py
│       │   └── report_service.py
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── keyword_analyzer.py
│       │   ├── trend_analyzer.py
│       │   ├── pattern_analyzer.py
│       │   └── difficulty_analyzer.py
│       ├── preprocessing/
│       │   ├── __init__.py
│       │   ├── tokenizer.py
│       │   ├── text_cleaner.py
│       │   └── stopwords.py
│       ├── visualization/
│       │   ├── __init__.py
│       │   ├── graph_generator.py
│       │   ├── wordcloud_generator.py
│       │   └── heatmap_generator.py
│       ├── database/
│       │   ├── __init__.py
│       │   ├── db_manager.py
│       │   └── models.py
│       └── utils/
│           ├── __init__.py
│           ├── logger.py
│           └── file_loader.py
└── tests/
    ├── unit/
    │   ├── test_keyword_analyzer.py
    │   └── test_text_cleaner.py
    └── integration/
        └── test_data_pipeline.py
```

---

## 8. 데이터 형식 예시

`sample_data/sample_questions.csv`

| year | chapter | question_type | difficulty | question_text | answer |
|---|---|---|---|---|---|
| 2022 | 데이터베이스 | 객관식 | 중 | SQL의 기본 명령어에 대한 설명으로 옳은 것은? | SELECT |

---

## 9. 개발 원칙

- 기능별 모듈 분리
- UI, 분석, 전처리, 데이터베이스, 시각화 계층 분리
- 테스트 가능한 함수 중심 설계
- SQLite 접근 로직은 database 모듈로 격리
- 시각화 로직은 visualization 모듈로 격리
- 한국어 처리 로직은 preprocessing 모듈로 격리
- 분석 로직은 analysis 모듈로 격리

---

## 10. 향후 개발 계획

- [ ] PySide6 기반 메인 화면 구현
- [ ] CSV 데이터 import 기능 구현
- [ ] SQLite 스키마 확정
- [ ] 키워드 빈도 분석 구현
- [ ] 연도별 출제 경향 분석 구현
- [ ] 단원별 비중 분석 구현
- [ ] 난이도 변화 분석 구현
- [ ] 그래프 이미지 저장 기능 구현
- [ ] 분석 보고서 자동 생성 기능 구현
- [ ] 단위 테스트 및 통합 테스트 보강

---

## 11. 라이선스

본 프로젝트는 MIT License를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참고하십시오.
