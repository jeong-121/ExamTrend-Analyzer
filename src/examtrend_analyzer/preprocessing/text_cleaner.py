"""Text cleaning module.

기출문제 텍스트에서 분석에 불필요한 문자를 제거하고 정규화한다.
"""

import re


class TextCleaner:
    """문항 텍스트 정제 클래스."""

    def clean(self, text: str) -> str:
        """문항 텍스트를 정제한다.

        Args:
            text: 원본 문항 텍스트.

        Returns:
            정제된 문항 텍스트.
        """
        # TODO: 과목별 특수 기호 보존 규칙 추가
        text = text.strip()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^0-9A-Za-z가-힣\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def clean_many(self, texts: list[str]) -> list[str]:
        """여러 문장을 일괄 정제한다."""
        return [self.clean(text) for text in texts]
