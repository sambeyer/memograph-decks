import dataclasses

from common import BaseWord
from meta import Card, CardSide

@dataclasses.dataclass
class Expression(BaseWord):
    english: str
    norsk: str

    def get_cards(self):
        return[Card(CardSide(self.norsk), CardSide(self.english))]

    @classmethod
    def from_dict(cls, inp):
        return cls(**inp)
