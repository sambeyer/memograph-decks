import abc
import enum

VOWELS = set('aeiouyæøå')

class UnknownGender(Exception):
    """Raised when an unknown gender is encountered"""

class Gender(enum.Enum):
    MASCULINE = 'm'
    NEUTER = 'n'

    @classmethod
    def is_valid(cls, gender: str) -> bool:
        try:
            _ = cls(gender)
        except ValueError:
            return False
        return True


class BaseWord(abc.ABC):
    @abc.abstractmethod
    def get_cards(self):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def from_dict(cls):
        raise NotImplementedError()


def count_vowels(word: str) -> int:
    return len([c for c in word if c in VOWELS])
