from __future__ import annotations

from dataclasses import dataclass

import yaml


@dataclass
class CroatianVerb:
    imperfective: CroatianVerbAspect
    perfective: CroatianVerbAspect


@dataclass
class CroatianVerbAspect:
    infinitive: str
    conjugated: str
    english: list[str]


@dataclass
class CroatianTerm:
    croatian: str
    english: list[str]


class CroatianLexicon:

    ASPECT_MAP = {"pf": "perfective", "impf": "imperfective"}

    def __init__(
        self,
        verbs: list[CroatianVerb],
        adjectives: list[CroatianTerm],
        adverbs: list[CroatianTerm],
        sayings: list[CroatianTerm],
    ) -> None:
        super().__init__()
        self.verbs = verbs
        self.adjectives = adjectives
        self.adverbs = adverbs
        self.sayings = sayings

    @classmethod
    def from_dict(cls, data):
        verbs = cls._parse_verbs(data.get("verbs"))
        adjectives = cls._parse_words(data.get("adjectives"))
        adverbs = cls._parse_words(data.get("adverbs"))
        sayings = cls._parse_sayings(data.get("sayings"))
        return cls(verbs=verbs, adjectives=adjectives, adverbs=adverbs, sayings=sayings)

    @classmethod
    def from_yaml(cls, path: str) -> CroatianLexicon:
        with open(path) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return cls.from_dict(data)

    @classmethod
    def _parse_verbs(cls, verb_dict):
        verbs = []
        for verb_data in verb_dict:
            to_write = {}

            for aspect_key, aspect in cls.ASPECT_MAP.items():
                verb_aspect_data = verb_data[aspect_key]
                to_write[aspect] = CroatianVerbAspect(
                    infinitive=verb_aspect_data["inf"],
                    conjugated=verb_aspect_data["conj"],
                    english=verb_data["eng"],
                )

            verbs.append(CroatianVerb(**to_write))

        return verbs

    @classmethod
    def _parse_words(cls, d):
        return [CroatianTerm(croatian=key, english=value) for key, value in d.items()]

    @classmethod
    def _parse_sayings(cls, items):
        return [CroatianTerm(**item) for item in items]
