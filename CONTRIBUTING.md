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
git checkout -b feature/keyword-analysis
```

## 2. 커밋 메시지 규칙

```text
type: summary
```

사용 가능한 type:

- feat: 새로운 기능
- fix: 버그 수정
- docs: 문서 수정
- style: 코드 스타일 수정
- refactor: 리팩토링
- test: 테스트 코드 추가/수정
- chore: 설정 또는 기타 작업

예시:

```text
feat: add keyword frequency analyzer
fix: handle empty csv file
docs: update installation guide
```

## 3. Pull Request 규칙

PR에는 다음 내용을 포함합니다.

- 변경 목적
- 주요 변경 사항
- 테스트 여부
- 관련 이슈 번호

## 4. 코드 작성 기준

- 함수와 클래스에는 명확한 역할을 부여합니다.
- UI 코드와 분석 로직을 분리합니다.
- 데이터베이스 접근 로직을 직접 UI에서 호출하지 않습니다.
- 테스트 가능한 단위로 함수를 작성합니다.

## 5. 테스트

PR 전 다음 명령을 실행합니다.

```bash
pytest
```
