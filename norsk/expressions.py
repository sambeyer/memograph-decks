import dataclasses
from typing import Optional

from common import BaseWord
from meta import Card, CardSide

@dataclasses.dataclass
class Expression(BaseWord):
    english: str
    norsk: str
    topic: Optional[str] = None

    def get_cards(self):
        front = CardSide(self.norsk)
        back = CardSide(self.english)
        card = Card(front, back, topic=self.topic) if self.topic else Card(front, back)
        return[card]

    @classmethod
    def from_dict(cls, inp):
        return cls(**inp)
