# Analysis Specification

## 1. 문서 목적

본 문서는 ExamTrend Analyzer의 분석 기능을 정의한다.

본 프로젝트는 특정 과목의 고정 단원 사전에 의존하지 않는 범용 기출문제 분석기를 목표로 한다.

## 2. 분석 파이프라인

분석은 `core/pipeline.py`의 `AnalysisPipeline`이 조율한다.

```text
파일 로드 (FileLoader)
    ↓
자동 컬럼 매핑 (suggest_field_mapping / FieldMappingDialog)
    ↓
데이터 검증 (DatasetValidator)
    ↓
문항 텍스트 정제 (TextCleaner)
    ↓
토큰화 (KoreanTokenizer)
    ↓
키워드 분석 (KeywordAnalyzer)
    ↓
N-Gram 분석 (NgramAnalyzer)
    ↓
TF-IDF 분석 (TfidfAnalyzer)
    ↓
유사 문항 분석 (SimilarityAnalyzer)
    ↓
연도별 경향 분석 (TrendAnalyzer)
    ↓
난이도 분석 (DifficultyAnalyzer)
    ↓
AnalysisResult 반환
    ↓
자동 주제 분석 (TopicAnalyzer) — AnalysisService에서 후처리
    ↓
시각화 및 보고서 생성
```

## 3. 전처리

### TextCleaner

문항 텍스트에서 분석에 불필요한 문자를 제거하고 정규화한다.

- 특수문자 제거
- 공백 정규화
- 영문 소문자화

### KoreanTokenizer

Kiwipiepy가 설치된 경우 형태소 분석을 사용한다. 미설치 시 정규식 기반 폴백으로 동작한다.

- 명사, 동사, 형용사 등 의미 있는 품사만 추출
- 불용어(DEFAULT_STOPWORDS) 제거

## 4. 키워드 분석

### 입력

- 문항 텍스트 목록

### 처리

- 문자열 정제 → 토큰화 → 불용어 제거 → 빈도 계산
- 문서 빈도(document frequency) 계산

### 출력

- `keyword_counts`: 키워드별 빈도 (상위 30개)
- `keyword_rows`: 키워드별 빈도 + 문서 빈도 상세 목록

## 5. N-Gram 분석

문항 텍스트에서 연속된 키워드 쌍(바이그램) 및 세 단어 조합(트라이그램)을 추출한다.

### 출력

- `bigrams`: 바이그램별 빈도 (상위 30개)
- `trigrams`: 트라이그램별 빈도 (상위 30개)

## 6. TF-IDF 분석

TF-IDF(Term Frequency-Inverse Document Frequency) 점수로 각 문항에서 중요도가 높은 키워드를 스코어링한다.

### 출력

- `tfidf`: 키워드별 TF-IDF 점수 목록 (상위 30개)

## 7. 자동 주제 분석

자동 주제 분석은 특정 과목의 단원명을 미리 알지 못해도 입력 데이터에서 주제 그룹을 생성하는 기능이다.

### 기존 단원 분류와의 차이

기존 방식은 다음과 같은 고정 사전을 사용한다.

```text
SQL, 정규화, 트랜잭션 → 데이터베이스
TCP, UDP, IP → 네트워크
```

이 방식은 정보처리기사나 컴퓨터공학 과목에는 적합하지만, 한국사, 국어, 영어, 전기기사 등 임의의 시험에는 적합하지 않다.

따라서 본 프로젝트는 고정 단원 분류 대신 자동 주제 그룹 방식을 사용한다.

### 처리 방식 (TopicAnalyzer)

```text
전체 문항에서 대표 키워드 추출
    ↓
대표 키워드를 여러 주제 그룹으로 분배
    ↓
각 문항과 주제 키워드의 겹침 정도 계산
    ↓
가장 관련성이 높은 주제에 문항 배정
    ↓
미분류 문항은 별도 그룹으로 처리
```

### 출력 예시

```text
주제 1: 조선, 왕권, 세종
주제 2: 전류, 전압, 저항
주제 3: 문맥, 글쓴이, 추론
```

자동 주제명은 과목명이나 단원명이 아니라 데이터에서 추출된 대표 키워드로 구성된다.

### 출력 필드

- `topic_source`: 주제 분류 방식 (`"keyword_cluster"`)
- `topic_counts`: 주제별 문항 수
- `topic_distribution`: 주제별 문항 수 및 비율(%) 목록
- `topic_keywords`: 주제별 대표 키워드 목록

## 8. 자동 주제별 비중 분석

각 주제에 배정된 문항 수와 전체 대비 비율을 계산한다.

```text
자동 주제 비율 = 자동 주제 문항 수 / 전체 문항 수 × 100
```

## 9. 유사 문항 분석

유사 문항 분석은 서로 다른 시험 또는 서로 다른 파일 간 반복 출제 가능성이 높은 문항을 찾는다.

### 처리 방식 (SimilarityAnalyzer)

TF-IDF 벡터화 후 코사인 유사도를 계산한다. 유사도 임계값은 0.55이며, 최대 50쌍을 반환한다.

### 제외 규칙

다음 비교는 결과에서 제외한다.

- 동일 데이터 행
- 동일 파일 내부 비교
- 동일 연도 + 동일 회차 내부 비교

### 출력

- `similar_pairs`: 유사 문항 쌍 목록
  - `similarity`: 유사도 점수
  - `question_1_source`: 문항 1 출처 (파일명)
  - `question_1_text`: 문항 1 내용
  - `question_2_source`: 문항 2 출처 (파일명)
  - `question_2_text`: 문항 2 내용

## 10. 연도별 경향 분석

`year` 컬럼이 있는 경우 연도별 문항 수를 집계한다.

- `yearly_counts`: 연도별 문항 수

## 11. 난이도 분석

`difficulty` 컬럼이 있는 경우 난이도 분포 및 연도별 평균 난이도를 산출한다.

난이도 점수 매핑: `하=1, 중=2, 상=3` (영문 `easy/medium/hard`도 지원).

- `difficulty_counts`: 난이도별 문항 수
- `average_difficulty_by_year`: 연도별 평균 난이도

## 12. 보고서 출력

`ReportService`가 `AnalysisResult`를 Markdown 텍스트로 변환한다.

보고서 구성:

1. 분석 개요 (문항 수, 파일명)
2. 분석 실행 상태
3. 키워드 빈도
4. 자동 주제별 비중
5. 자동 주제별 대표 키워드
6. 유사 문항 후보
7. 검증 이슈
