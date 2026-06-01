# System Design

## 1. 아키텍처 개요

ExamTrend Analyzer는 PySide6 UI와 분석 로직을 분리한 계층형 구조로 설계한다.

```text
UI Layer (PySide6)
  ↓
Application / Service Layer
  ↓
Analysis / Preprocessing / Visualization
  ↓
Database / File System
```

## 2. 패키지 역할

| 패키지 | 역할 |
|---|---|
| ui | PySide6 기반 화면, 페이지, 재사용 위젯 구성 |
| services | UI 요청을 분석, 보고서, DB 기능으로 연결하는 응용 서비스 계층 |
| analysis | 키워드, 경향, 패턴, 난이도 분석 |
| preprocessing | 텍스트 정제, 토큰화, 불용어 처리 |
| visualization | 그래프, 워드클라우드, 히트맵 생성 |
| database | SQLite 연결 및 데이터 모델 |
| utils | 로깅, 파일 로딩 등 공통 기능 |

## 3. UI 구조

```text
ui/
├── main_window.py
├── pages/
│   ├── dashboard_page.py
│   ├── analysis_page.py
│   └── report_page.py
└── widgets/
    └── summary_card.py
```

- `MainWindow`: 툴바, 페이지 전환, 파일 로딩/분석/보고서 저장 이벤트 처리
- `DashboardPage`: 데이터 미리보기와 파일/행/컬럼 요약
- `AnalysisPage`: 분석 결과 요약과 텍스트 결과 표시
- `ReportPage`: Markdown 보고서 미리보기
- `SummaryCard`: 여러 화면에서 재사용하는 요약 카드

## 4. Service 구조

```text
services/
├── analysis_service.py
├── database_service.py
└── report_service.py
```

- `AnalysisService`: 전처리 → 토큰화 → 키워드/경향/난이도/패턴 분석을 하나의 흐름으로 묶음
- `ReportService`: 분석 결과를 Markdown 보고서로 변환하고 저장
- `DatabaseService`: DataFrame 데이터를 SQLite 저장 로직으로 연결

## 5. 데이터 흐름

```text
사용자 파일 선택
→ MainWindow
→ FileLoader
→ DashboardPage 미리보기
→ AnalysisService
→ TextCleaner
→ KoreanTokenizer
→ Analyzer 클래스들
→ AnalysisPage / ReportPage 표시
→ ReportService를 통한 reports 저장
```

## 6. 확장 전략

- UI는 PySide6 위젯과 이벤트 처리만 담당한다.
- 분석 알고리즘은 `analysis` 패키지의 Analyzer 클래스로 캡슐화한다.
- UI와 분석 알고리즘 사이에는 `services` 계층을 둔다.
- 새로운 화면은 `ui/pages`에 추가한다.
- 재사용 UI 요소는 `ui/widgets`에 추가한다.
- 새로운 시각화 방식은 `visualization` 패키지에 모듈을 추가한다.
- 데이터베이스 테이블 변경은 `models.py`와 `db_manager.py`에서 관리한다.

## 7. TODO

- [ ] matplotlib 그래프를 PySide6 화면에 임베딩
- [ ] 클래스 다이어그램 추가
- [ ] 시퀀스 다이어그램 추가
- [ ] DB ERD 추가
