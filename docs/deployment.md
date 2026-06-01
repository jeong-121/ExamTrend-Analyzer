# Deployment Guide

## 1. 설치

```bash
git clone https://github.com/<repository>/ExamTrend-Analyzer.git
cd ExamTrend-Analyzer
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
pip install -r requirements.txt
```

## 2. 실행

```bash
python run.py
```

## 3. 주요 의존성

| 패키지 | 버전 | 용도 |
|---|---|---|
| PySide6 | >= 6.6.0 | GUI 프레임워크 |
| pandas | >= 2.0.0 | 데이터 처리 |
| numpy | >= 1.24.0 | 수치 연산 |
| matplotlib | >= 3.7.0 | 시각화 |
| openpyxl | >= 3.1.0 | Excel 처리 |
| scikit-learn | >= 1.3.0 | TF-IDF, 코사인 유사도 |
| kiwipiepy | >= 0.18.0 | 한국어 형태소 분석 (선택) |
| PyMuPDF | 최신 | PDF 텍스트 추출 |
| pytest | >= 8.0.0 | 테스트 (개발용) |

## 4. Python 버전

Python 3.10 이상이 필요합니다.

## 5. 테스트 실행

```bash
pytest
```

## 6. 배포용 exe 생성 (Windows)

PyInstaller를 사용하여 단일 실행 파일을 생성할 수 있습니다.

```bash
pip install pyinstaller
pyinstaller --onefile --windowed run.py
```

생성된 파일은 `dist/run.exe`에 위치합니다.

> 주의: PySide6와 matplotlib의 리소스 파일(폰트, 플러그인 등)을 함께 패키징해야 할 수 있습니다.  
> `--add-data` 옵션으로 필요한 파일을 지정하세요.

## 7. 제외 기능

현재 버전은 다음 기능을 UI에서 제공하지 않습니다.

- DB 저장 및 불러오기
- 로그인 및 사용자 계정
- 특정 과목 전용 단원 분류
