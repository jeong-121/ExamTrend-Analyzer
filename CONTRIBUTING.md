# Contributing Guide

ExamTrend Analyzer 프로젝트에 기여할 때는 아래 기준을 따릅니다.

## 1. 브랜치 전략

```text
main        : 안정 버전
develop     : 개발 통합 브랜치
feature/*   : 기능 개발
fix/*       : 버그 수정
docs/*      : 문서 수정
test/*      : 테스트 추가
```

예시:

```bash
git checkout -b feature/ngram-analysis
git checkout -b fix/pdf-loader-encoding
git checkout -b docs/update-readme
```

## 2. 커밋 메시지 규칙

```text
type: summary
```

사용 가능한 type:

- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 스타일 수정 (기능 변경 없음)
- `refactor`: 리팩토링
- `test`: 테스트 코드 추가/수정
- `chore`: 설정 또는 기타 작업

예시:

```text
feat: add ngram frequency analyzer
fix: handle empty csv file on load
docs: update architecture diagram
test: add unit test for similarity filtering
```

## 3. Pull Request 규칙

PR에는 다음 내용을 포함합니다.

- 변경 목적
- 주요 변경 사항
- 테스트 여부 (`pytest` 실행 결과)
- 관련 이슈 번호

## 4. 코드 작성 기준

- 함수와 클래스에는 명확한 역할을 부여합니다.
- UI 코드와 분석 로직을 분리합니다 (`CODE_STYLE.md` 참고).
- 분석 결과는 `AnalysisResult` 데이터 모델을 통해 전달합니다.
- 특정 과목에 종속되는 고정 단원 사전을 분석 로직에 추가하지 않습니다.
- Kiwipiepy 미설치 환경에서도 동작해야 합니다 (정규식 폴백 유지).

## 5. 의존성 추가 규칙

새 외부 라이브러리를 추가하는 경우 `requirements.txt`와 `pyproject.toml`을 함께 갱신합니다.

## 6. 테스트

PR 전 다음 명령을 실행합니다.

```bash
pytest
```

단위 테스트는 `tests/unit/`, 통합 테스트는 `tests/integration/`에 작성합니다.
