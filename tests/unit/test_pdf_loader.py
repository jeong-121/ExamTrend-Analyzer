from pathlib import Path

import pandas as pd

from examtrend_analyzer.core.pdf_loader import PdfQuestionLoader


def test_pdf_loader_extract_questions_from_text():
    text = """
    [PAGE 1]
    [1~3] 다음 글을 읽고 물음에 답하시오.
    1. 윗글의 내용과 일치하지 않는 것은?
    ① 보기 하나
    ② 보기 둘
    2. ㉠에 해당하는 내용으로 가장 적절한 것은?
    ① 보기 하나
    """
    rows = PdfQuestionLoader().extract_questions(text)
    assert len(rows) == 2
    assert rows[0]["question_no"] == 1
    assert "일치하지 않는 것은" in rows[0]["question_text"]
