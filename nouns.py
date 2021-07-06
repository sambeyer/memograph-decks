import abc
import dataclasses

import common
from common import BaseWord, Gender, UnknownGender
from meta import Card, CardSide

TOPIC = 'nouns'

@dataclasses.dataclass
class Noun(BaseWord):
    gender: Gender
    english: str
    english_plural: str
    indefinite_singular: str
    definite_singular: str = None
    indefinite_plural: str = None
    definite_plural: str = None

    def __post_init__(self):
        if not Gender.is_valid(self.gender):
            raise UnknownGender(f'Unknown gender {self.gender}')

        self.gender = Gender(self.gender)

        strategy = self._get_noun_strategy()
        if self.definite_singular is None:
            self.definite_singular = strategy.get_definite_singular(self)
        if self.indefinite_plural is None:
            self.indefinite_plural = strategy.get_indefinite_plural(self)
        if self.definite_plural is None:
            self.definite_plural = strategy.get_definite_plural(self)

    @property
    def n_syllables(self):
        return common.count_vowels(self.indefinite_singular)

    def get_cards(self):
        english_a = 'an' if self.english[0] in common.VOWELS else 'a'
        norsk_a = 'en' if self.gender == Gender.MASCULINE else 'et'

        is_card = Card(
            CardSide(f'{norsk_a} {self.indefinite_singular}'),
            CardSide(f'{english_a} {self.english}'),
        )
        ds_card = Card(
            CardSide(self.definite_singular),
            CardSide(f'the {self.english}'),
        )
        ip_card = Card(
            CardSide(f'mange {self.indefinite_plural}'),
            CardSide(f'many {self.english_plural}'),
        )
        dp_card = Card(
            CardSide(f'alle {self.definite_plural}'),
            CardSide(f'all the {self.english_plural}'),
        )

        return [
            is_card,
            ds_card,
            ip_card,
            dp_card,
        ]

    def _get_noun_strategy(self):
        return RegularNounStrategy

    @classmethod
    def from_dict(cls, inp):
        return cls(**inp)


class BaseNounStrategy(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_definite_singular(cls, noun: Noun) -> str:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def get_indefinite_plural(cls, noun: Noun) -> str:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def get_definite_plural(cls, noun: Noun) -> str:
        raise NotImplementedError()


class RegularNounStrategy(BaseNounStrategy):
    @classmethod
    def get_definite_singular(cls, noun: Noun) -> str:
        base = cls._get_base(noun)
        if noun.gender == Gender.MASCULINE:
            ending = 'en'
        elif noun.gender == Gender.NEUTER:
            ending = 'et'
        else:
            raise Gender.UnknownGender(f'Unknown gender {noun.gender}')
        return f'{base}{ending}'

    @classmethod
    def get_indefinite_plural(cls, noun: Noun) -> str:
        if noun.gender == Gender.NEUTER and noun.n_syllables == 1:
            return noun.indefinite_singular
        return f'{cls._get_base(noun)}er'

    @classmethod
    def get_definite_plural(cls, noun: Noun) -> str:
        indefinite_plural = (
            noun.indefinite_plural
            if noun.indefinite_plural is not None
            else cls.get_indefinite_plural(noun)
        )

        if noun.gender == Gender.NEUTER and noun.n_syllables == 1:
            base = indefinite_plural
        elif indefinite_plural.endswith('e'):
            base = indefinite_plural[:-1]
        elif indefinite_plural.endswith('er'):
            base = indefinite_plural[:-2]
        else:
            base = cls._get_base(noun)

        return f'{base}ene'

    @staticmethod
    def _get_base(noun: Noun):
        noun = noun.indefinite_singular
        if noun.endswith('e') and common.count_vowels(noun) != 1:
            return noun[:-1]
        return noun
