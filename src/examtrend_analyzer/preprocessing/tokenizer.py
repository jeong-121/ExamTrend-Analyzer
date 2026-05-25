"""Tokenizer module.

kiwipiepy를 사용하여 한국어 문항 텍스트를 토큰화한다.
"""

from kiwipiepy import Kiwi


class KoreanTokenizer:
    """한국어 형태소 기반 토큰화 클래스."""

    def __init__(self) -> None:
        self.kiwi = Kiwi()

    def tokenize(self, text: str) -> list[str]:
        """입력 문장을 토큰 목록으로 변환한다."""
        # TODO: 명사, 동사, 형용사 등 분석 대상 품사 필터링 옵션 추가
        result = self.kiwi.tokenize(text)
        return [token.form for token in result]

    def tokenize_many(self, texts: list[str]) -> list[list[str]]:
        """여러 문장을 일괄 토큰화한다."""
        return [self.tokenize(text) for text in texts]
