# Code Style Guide

ExamTrend Analyzer의 코드 스타일 기준입니다.

## 1. Python 버전

Python 3.10 이상을 사용합니다 (`pyproject.toml` 기준: `requires-python = ">=3.10"`).

## 2. 네이밍 규칙

| 대상 | 규칙 | 예시 |
|---|---|---|
| 파일명 | snake_case | keyword_analyzer.py |
| 함수명 | snake_case | analyze_keywords |
| 변수명 | snake_case | question_text |
| 클래스명 | PascalCase | KeywordAnalyzer |
| 상수 | UPPER_SNAKE_CASE | DEFAULT_STOPWORDS |

## 3. 모듈 분리 원칙

- `ui/`: PySide6 화면 및 사용자 이벤트 처리
- `services/`: AnalysisService, ReportService — 파일 로드·매핑·분석 조율
- `analysis/`: 분석 알고리즘 (keyword, ngram, tfidf, similarity, topic, trend, difficulty, pattern, prediction)
- `core/`: 파이프라인, 데이터 모델, 스키마, 검증, 파일 로더
- `preprocessing/`: 텍스트 정제 및 토큰화
- `visualization/`: 그래프 및 시각화 생성
- `database/`: SQLite 연결 및 데이터 모델 (현재 버전 미사용)
- `config/`: 앱 설정
- `utils/`: 공통 유틸리티 (파일명 메타데이터, 폰트, 로거)

## 4. Docstring 규칙

공개 함수와 클래스에는 docstring을 작성합니다.

```python
def analyze_keywords(texts: list[str]) -> dict[str, int]:
    """문항 텍스트 목록에서 키워드 빈도를 분석한다."""
```

## 5. 타입 힌트

모든 공개 함수에 타입 힌트를 작성합니다. `from __future__ import annotations`를 각 모듈 상단에 포함합니다.

```python
from __future__ import annotations

def run(self, data: pd.DataFrame, file_path: str | Path | None = None) -> AnalysisResult:
    ...
```

## 6. TODO 주석

추후 구현이 필요한 부분에는 다음 형식을 사용합니다.

```python
# TODO: CSV 인코딩 자동 감지 기능 추가
```

## 7. 예외 처리

- 파일 입출력, 외부 라이브러리 호출에는 예외 처리를 추가합니다.
- 예외 메시지는 사용자 또는 개발자가 원인을 파악할 수 있도록 한국어로 작성합니다.
- UI 레이어에서는 `QMessageBox`를 통해 사용자에게 오류를 표시합니다.

```python
try:
    df = self.file_loader.load(path)
except Exception as exc:
    QMessageBox.critical(self, "파일 로딩 실패", str(exc))
```

## 8. 테스트 기준

- 분석 로직은 `tests/unit/`에 단위 테스트를 작성합니다.
- 파이프라인 전체 흐름은 `tests/integration/`에 통합 테스트를 작성합니다.
- 테스트 실행: `pytest`

## 9. UI와 분석 로직 분리

- UI 코드(`ui/`)는 분석 로직(`analysis/`)에 직접 의존하지 않습니다.
- UI는 `AnalysisService`를 통해 분석 결과를 받습니다.
- 분석 작업은 `FunctionWorker`를 통해 별도 스레드에서 실행합니다.
