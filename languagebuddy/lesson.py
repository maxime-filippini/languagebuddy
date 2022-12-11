from __future__ import annotations

from language import Language


class Lesson:
    def __init__(self, ref_language: Language, foreign_language: Language) -> None:
        self.ref_language = ref_language
        self.foreign_language = foreign_language

    @classmethod
    def from_markdown(self, path: str) -> Lesson:
        ...
