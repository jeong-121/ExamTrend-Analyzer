from examtrend_analyzer.analysis.topic_analyzer import TopicAnalyzer


def test_topic_analyzer_returns_generic_topics():
    texts = [
        "조선 세종 왕권 정책에 대한 설명으로 옳은 것은?",
        "전류 전압 저항의 관계에 대한 설명으로 옳은 것은?",
        "문맥 추론 글쓴이 관점에 대한 설명으로 옳은 것은?",
    ]

    result = TopicAnalyzer(topic_count=3).analyze(texts)

    assert result["counts"]
    assert result["distribution"]
    assert result["topic_keywords"]
    assert all("주제" in row["topic"] or row["topic"] == "미분류" for row in result["topic_keywords"])
