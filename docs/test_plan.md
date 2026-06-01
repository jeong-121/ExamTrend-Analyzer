# Test Plan

## 1. 테스트 목적

본 테스트 계획은 ExamTrend Analyzer의 분석 기능이 정상적으로 동작하는지 검증한다.

테스트는 `tests/unit/` (단위 테스트)과 `tests/integration/` (통합 테스트)으로 구성된다.

## 2. 주요 테스트 영역

- 파일 로딩 (PDF, Excel, CSV, TXT)
- 자동 컬럼 매핑
- 텍스트 전처리 (TextCleaner, KoreanTokenizer)
- 키워드 분석
- N-Gram 분석
- TF-IDF 분석
- 자동 주제 분석
- 유사 문항 분석
- 보고서 저장
- UI 시각화 임포트
- 데이터 계약 (AnalysisResult 필드)
- 예외 처리

## 3. 단위 테스트 목록 (`tests/unit/`)

| 테스트 파일 | 검증 내용 |
|---|---|
| test_analysis_result_contract.py | AnalysisResult 데이터 모델 필드 계약 |
| test_analysis_service_contract.py | AnalysisService 인터페이스 계약 |
| test_auto_mapping.py | 자동 컬럼 매핑 정확도 |
| test_dashboard_db_buttons_removed.py | DB 버튼 제거 확인 |
| test_file_loading_contract.py | 파일 로딩 인터페이스 계약 |
| test_generic_analysis_service.py | 범용 분석 서비스 동작 |
| test_generic_topic_analysis.py | 자동 주제 분석 동작 |
| test_keyword_analyzer.py | 키워드 빈도 계산 |
| test_multi_file_loading.py | 다중 파일 병합 로딩 |
| test_pdf_loader.py | PDF 로딩 및 문항 추출 |
| test_robust_analysis_contract.py | 결함 데이터 처리 견고성 |
| test_similarity_enrichment.py | 유사 문항 메타데이터 보강 |
| test_similarity_filtering.py | 유사 문항 필터링 (동일 파일/연도/회차 제외) |
| test_similar_table_ui.py | 유사 문항 UI 테이블 렌더링 |
| test_simplified_analysis.py | 간소화 분석 흐름 |
| test_stage2_analysis.py | 2단계 분석 파이프라인 |
| test_stage2_regression.py | 2단계 분석 회귀 테스트 |
| test_text_cleaner.py | 텍스트 정제 |
| test_tokenizer_regression.py | 토크나이저 회귀 테스트 |
| test_topic_analyzer.py | 자동 주제 분석기 |
| test_trend_pattern_engine.py | 연도별 경향 및 패턴 분석 |
| test_ui_visualization_imports.py | 시각화 모듈 임포트 확인 |
| test_validation.py | 데이터 검증 |

## 4. 통합 테스트 목록 (`tests/integration/`)

| 테스트 파일 | 검증 내용 |
|---|---|
| test_pipeline.py | 전체 분석 파이프라인 엔드-투-엔드 |
| test_data_pipeline.py | 데이터 로드부터 분석까지 흐름 |

## 5. 테스트 케이스

| ID | 분류 | 테스트 내용 | 기대 결과 |
|---|---|---|---|
| TC-001 | 파일 | PDF 파일 로드 | 문항 데이터 생성 |
| TC-002 | 파일 | Excel 파일 로드 | 문항 데이터 생성 |
| TC-003 | 파일 | CSV 파일 로드 | 문항 데이터 생성 |
| TC-004 | 파일 | TXT 파일 로드 | 문항 데이터 생성 |
| TC-005 | 파일 | 다중 파일 선택 | 병합 데이터 생성 |
| TC-006 | 매핑 | question_text 자동 탐지 | 자동 매핑 성공 |
| TC-007 | 매핑 | 문제 컬럼 자동 탐지 | 자동 매핑 성공 |
| TC-008 | 분석 | 키워드 분석 실행 | 키워드 빈도 출력 |
| TC-009 | 분석 | N-Gram 분석 실행 | 바이그램·트라이그램 빈도 출력 |
| TC-010 | 분석 | TF-IDF 분석 실행 | 키워드 점수 출력 |
| TC-011 | 분석 | 자동 주제 분석 실행 | 주제 그룹 생성 |
| TC-012 | 분석 | 자동 주제별 비중 계산 | 비율 합산 정상 |
| TC-013 | 분석 | 대표 키워드 생성 | 주제별 키워드 출력 |
| TC-014 | 유사문항 | 동일 파일 내부 비교 | 결과 제외 |
| TC-015 | 유사문항 | 동일 연도/회차 비교 | 결과 제외 |
| TC-016 | 유사문항 | 서로 다른 파일 비교 | 유사 후보 표시 |
| TC-017 | UI | 키워드 탭 표시 | 결과 표시 |
| TC-018 | UI | 자동 주제 탭 표시 | 결과 표시 |
| TC-019 | UI | 유사 문항 탭 표시 | 출처/본문 표시, 읽기 전용 |
| TC-020 | 시각화 | 키워드 차트 표시 | 한글 깨짐 없음 |
| TC-021 | 시각화 | 자동 주제 차트 표시 | 비중 파이 차트 표시 |
| TC-022 | 보고서 | Markdown 저장 | 파일 생성 |
| TC-023 | 전처리 | 빈 텍스트 처리 | 오류 없이 스킵 |
| TC-024 | 전처리 | 불용어 제거 | 지시문 표현 제외 |

## 6. 제외 테스트

다음 기능은 현재 버전의 범위에서 제외되었으므로 테스트 대상이 아니다.

- DB 저장 및 불러오기 UI
- 로그인 및 사용자 계정
- 특정 과목 전용 단원 분류
