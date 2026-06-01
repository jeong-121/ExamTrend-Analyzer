import pandas as pd

from examtrend_analyzer.analysis.topic_analyzer import TopicAnalyzer
from examtrend_analyzer.services.analysis_service import AnalysisService


def test_topic_analyzer_returns_generic_topics():
    texts = [
        "SQL 정규화 트랜잭션 문제",
        "SQL 인덱스 관계형 데이터베이스",
        "작품 화자 표현 방식",
        "문학 작품 서술자 갈등",
    ]

    result = TopicAnalyzer(topic_count=3).analyze(texts)

    assert result["counts"]
    assert result["distribution"]
    assert result["topic_keywords"]


def test_analysis_service_uses_topic_fields():
    df = pd.DataFrame({
        "question_text": [
            "SQL 정규화 트랜잭션 문제",
            "SQL 인덱스 관계형 데이터베이스",
            "작품 화자 표현 방식",
            "문학 작품 서술자 갈등",
        ]
    })

    result = AnalysisService().run_analysis(df)

    assert result.topic_counts
    assert result.topic_distribution
    assert result.topic_keywords
    assert result.chapter_distribution  # legacy compatibility
