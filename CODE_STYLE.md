# Code Style Guide

ExamTrend Analyzer의 코드 스타일 기준입니다.

## 1. Python 버전

Python 3.10 이상을 권장합니다.

## 2. 네이밍 규칙

| 대상 | 규칙 | 예시 |
|---|---|---|
| 파일명 | snake_case | keyword_analyzer.py |
| 함수명 | snake_case | analyze_keywords |
| 변수명 | snake_case | question_text |
| 클래스명 | PascalCase | KeywordAnalyzer |
| 상수 | UPPER_SNAKE_CASE | DEFAULT_STOPWORDS |

## 3. 모듈 분리 원칙

- `ui`: PySide6 화면 및 사용자 이벤트 처리
- `analysis`: 분석 알고리즘
- `preprocessing`: 텍스트 정제 및 토큰화
- `visualization`: 그래프 및 시각화 생성
- `database`: SQLite 연결 및 데이터 모델
- `utils`: 공통 유틸리티

## 4. Docstring 규칙

공개 함수와 클래스에는 docstring을 작성합니다.

```python
def analyze_keywords(texts: list[str]) -> dict[str, int]:
    """문항 텍스트 목록에서 키워드 빈도를 분석한다."""
```

## 5. TODO 주석

추후 구현이 필요한 부분에는 다음 형식을 사용합니다.

```python
# TODO: CSV 인코딩 자동 감지 기능 추가
```

## 6. 예외 처리

- 파일 입출력, 데이터베이스 접근, 외부 라이브러리 호출에는 예외 처리를 추가합니다.
- 예외 메시지는 사용자 또는 개발자가 원인을 파악할 수 있도록 작성합니다.

## 7. 테스트 기준

- 분석 로직은 단위 테스트를 작성합니다.
- 데이터 로딩부터 분석까지 이어지는 흐름은 통합 테스트를 작성합니다.
