import pandas as pd

from examtrend_analyzer.services.analysis_service import AnalysisService


def test_analysis_service_uses_topic_fields():
    df = pd.DataFrame({
        "question_text": [
            "조선 세종 왕권 정책에 대한 설명으로 옳은 것은?",
            "전류 전압 저항의 관계에 대한 설명으로 옳은 것은?",
            "문맥 추론 글쓴이 관점에 대한 설명으로 옳은 것은?",
        ]
    })

    result = AnalysisService().run_analysis(df)

    assert result.keyword_counts
    assert result.topic_counts
    assert result.topic_distribution
    assert result.topic_keywords
    assert result.summary.topics
