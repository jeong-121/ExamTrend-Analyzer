import pandas as pd

from examtrend_analyzer.services.analysis_service import AnalysisService
from examtrend_analyzer.utils.plot_font import configure_korean_font


def test_simplified_analysis_has_no_tfidf_ngram_year_outputs():
    df = pd.DataFrame({
        "question_text": [
            "SQL과 트랜잭션 ACID 특성에 대한 설명으로 옳은 것은?",
            "정규화와 기본키 외래키에 대한 설명으로 옳은 것은?",
        ]
    })

    result = AnalysisService().run_analysis(df)

    assert result.keyword_counts
    assert result.tfidf == []
    assert result.bigrams == {}
    assert result.trigrams == {}
    assert result.yearly_counts == {}
    assert result.chapter_counts


def test_korean_font_configuration_returns_font_name():
    selected = configure_korean_font()
    assert isinstance(selected, str)
    assert selected
