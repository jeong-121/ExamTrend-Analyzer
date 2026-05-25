# System Design

## 1. 아키텍처 개요

ExamTrend Analyzer는 계층형 구조로 설계한다.

```text
UI Layer
  ↓
Application / Service Logic
  ↓
Analysis / Preprocessing / Visualization
  ↓
Database / File System
```

## 2. 패키지 역할

| 패키지 | 역할 |
|---|---|
| ui | PyQt6 기반 화면 구성 |
| analysis | 키워드, 경향, 패턴, 난이도 분석 |
| preprocessing | 텍스트 정제, 토큰화, 불용어 처리 |
| visualization | 그래프, 워드클라우드, 히트맵 생성 |
| database | SQLite 연결 및 데이터 모델 |
| utils | 로깅, 파일 로딩 등 공통 기능 |

## 3. 데이터 흐름

```text
사용자 파일 선택
→ FileLoader
→ TextCleaner
→ Tokenizer
→ Analyzer
→ GraphGenerator
→ UI 표시 또는 reports 저장
```

## 4. 확장 전략

- 분석 알고리즘은 Analyzer 클래스로 캡슐화한다.
- 새로운 시각화 방식은 visualization 패키지에 모듈을 추가한다.
- 데이터베이스 테이블 변경은 models.py와 db_manager.py에서 관리한다.
- UI는 분석 로직에 직접 의존하지 않고 결과 데이터만 전달받는다.

## 5. TODO

- [ ] 클래스 다이어그램 추가
- [ ] 시퀀스 다이어그램 추가
- [ ] DB ERD 추가
