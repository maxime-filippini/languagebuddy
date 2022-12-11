from __future__ import annotations

from abc import ABC
from abc import abstractclassmethod


class Language(ABC):
    @abstractclassmethod
    def characters(cls):
        ...

    @classmethod
    def from_lexicon_db(cls, db_connection) -> Language:
        ...


class Croatian(Language):
    characters = "abcčćddžđefghijklljmnnjoprsštuvzž"


class English(Language):
    characters = "abcdefghijklmnopqrstuvwxyz"
