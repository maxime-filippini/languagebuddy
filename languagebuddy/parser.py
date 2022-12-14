from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

RE_TAG = re.compile(r"#([^\s]+)")
RE_VOCAB = re.compile("([^=]+)=([^=]+)")
RE_COMMENTS = re.compile(r"\(([^\)]+)\)")


class LineTag(Enum):
    fix = "fix"
    v = "v"
    pf = "pf"
    impf = "impf"
    n = "n"
    m = "m"
    f = "f"
    nt = "nt"
    adj = "adj"
    adv = "adv"
    sent = "sent"
    trans = "trans"
    rule = "rule"
    say = "say"
    tbc = "tbc"


@dataclass
class LessonData:
    items: list[LessonItem]


@dataclass
class LessonItem:
    text: str
    tags: list[LineTag]


@dataclass
class VocabItem:
    source: str
    target: str


class LessonParser:
    def __init__(self) -> None:
        pass

    def _get_tags_from_line(self, line: str):
        return [getattr(LineTag, t_s) for t_s in re.findall(RE_TAG, line)]

    def parse_single_line(self, line: str) -> LessonItem:
        """Parse a single line of a lesson note.

        Args:
            line (str): Line from a note

        Returns:
            LessonItem: Lesson item
        """
        tags = self._get_tags_from_line(line)
        full_line = re.sub(RE_TAG, "", line).strip()

        return LessonItem(text=full_line, tags=tags)

    def parse(self, path: str) -> LessonData:
        with open(path) as f:
            lines = f.readlines()

        lines = [s for line in lines if (s := line.strip())]

        data = []
        for line in lines:
            data.append(self.parse_single_line(line))

        return LessonData(items=data)
