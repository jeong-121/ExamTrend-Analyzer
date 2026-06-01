"""Korean-aware tokenization utilities.

Kiwi is used when available. When Kiwi is unavailable, a conservative regex
fallback removes common Korean particles/endings so 조사 and 지시문 표현 do
not dominate keyword rankings.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable

try:
    from examtrend_analyzer.preprocessing.stopwords import DEFAULT_STOPWORDS
except Exception:  # pragma: no cover
    DEFAULT_STOPWORDS = set()

EXTRA_STOP_WORDS: set[str] = {
    "은", "는", "이", "가", "을", "를", "의", "에", "에서", "으로", "로",
    "와", "과", "도", "만", "부터", "까지", "에게", "한테", "께", "보다",
    "및", "또는", "그리고", "하지만", "그러나", "따라서",
    "대한", "대해", "대하여", "관련", "설명", "설명으로", "다음", "보기",
    "문제", "문항", "중", "것", "것은", "것을", "것이", "있는", "없는",
    "옳은", "옳지", "않은", "고르시오", "선택하시오", "무엇", "무엇인가",
    "하", "ㄴ", "는지", "으로서", "으로써",
}

DEFAULT_STOP_WORDS: set[str] = set(DEFAULT_STOPWORDS) | EXTRA_STOP_WORDS

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_+.#-]*|[가-힣]{2,}|[0-9]+[A-Za-z]+")
EN_PARTICLE_RE = re.compile(
    r"([A-Za-z0-9_+.#-]+)(은|는|이|가|을|를|의|에|에서|으로|로|와|과|도|만)\b"
)
KO_SUFFIXES: tuple[str, ...] = (
    "으로써", "으로서", "에서", "에게", "한테", "까지", "부터", "보다",
    "으로", "라는", "이며", "이고", "하고", "에서의",
    "은", "는", "이", "가", "을", "를", "의", "에", "로", "와", "과", "도", "만",
)
KO_ENDINGS: tuple[str, ...] = (
    "하시오", "하세요", "한다", "하다", "하는", "하면", "하며",
    "인가", "인지", "으로", "으로서", "으로써",
)


@dataclass
class KoreanTokenizer:
    """Tokenize Korean exam questions into analyzable keywords."""

    stop_words: set[str] = field(default_factory=lambda: set(DEFAULT_STOP_WORDS))
    min_length: int = 2
    use_kiwi: bool = True

    def __post_init__(self) -> None:
        self._kiwi = None
        if self.use_kiwi:
            try:
                from kiwipiepy import Kiwi  # type: ignore

                self._kiwi = Kiwi()
            except Exception:
                self._kiwi = None

    def tokenize(self, text: object) -> list[str]:
        if text is None:
            return []

        normalized = self._normalize(str(text))
        if not normalized:
            return []

        if self._kiwi is not None:
            tokens = self._tokenize_with_kiwi(normalized)
        else:
            tokens = self._tokenize_with_regex(normalized)

        return self._filter_tokens(tokens)

    def tokenize_many(self, texts: Iterable[object]) -> list[list[str]]:
        return [self.tokenize(text) for text in texts]

    def _normalize(self, text: str) -> str:
        text = text.replace("\u00a0", " ")
        text = EN_PARTICLE_RE.sub(r"\1 ", text)
        text = re.sub(r"[^0-9A-Za-z가-힣_+.#\-\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _tokenize_with_kiwi(self, text: str) -> list[str]:
        result: list[str] = []
        try:
            for token in self._kiwi.tokenize(text):
                form = token.form
                tag = token.tag
                if tag.startswith("N") or tag in {"SL"}:
                    result.append(form)
        except Exception:
            return self._tokenize_with_regex(text)
        return result

    def _tokenize_with_regex(self, text: str) -> list[str]:
        return TOKEN_RE.findall(text)

    def _filter_tokens(self, tokens: Iterable[str]) -> list[str]:
        filtered: list[str] = []

        for raw in tokens:
            token = self._normalize_token(raw)

            if not token:
                continue
            if len(token) < self.min_length:
                continue
            if token in self.stop_words or token.lower() in self.stop_words:
                continue
            if token.isdigit():
                continue
            if re.fullmatch(r"[ㄱ-ㅎㅏ-ㅣ]+", token):
                continue

            filtered.append(token)

        return filtered

    def _normalize_token(self, raw: object) -> str:
        token = str(raw).strip()
        if not token:
            return ""

        if re.search(r"[A-Za-z]", token) and not re.search(r"[가-힣]", token):
            return token.upper()

        token = self._strip_korean_suffix(token)

        if token in self.stop_words:
            return ""

        return token

    def _strip_korean_suffix(self, token: str) -> str:
        if not re.fullmatch(r"[가-힣]+", token):
            return token

        original = token

        for suffix in KO_ENDINGS:
            if token.endswith(suffix) and len(token) > len(suffix) + 1:
                token = token[: -len(suffix)]
                break

        for suffix in KO_SUFFIXES:
            if token.endswith(suffix) and len(token) > len(suffix) + 1:
                token = token[: -len(suffix)]
                break

        return "" if token in self.stop_words else token or original
