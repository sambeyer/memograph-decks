import dataclasses

import common
from common import BaseWord
from meta import CardSide, Card

TOPIC = 'verbs'


@dataclasses.dataclass
class Verb(BaseWord):
    english_past: str
    norsk_past: str
    english_past_participle: str
    norsk_past_participle: str
    english_subject: str = 'I'
    english_print_suffix: str = ''

    @property
    def norsk_subject(self):
        if self.english_subject == 'it':
            return 'det'
        return 'jeg'

    def get_cards(self):
        past_card = Card(
            CardSide(f'{self.norsk_subject} {self.norsk_past}'),
            CardSide(
                print_str=f'{self.english_subject} {self.english_past} {self.english_print_suffix}',
                match_str=f'{self.english_subject} {self.english_past}'),
            topic=TOPIC,
        )

        past_participle_card = Card(
            CardSide(f'{self.norsk_subject} {self.norsk_past_participle}'),
            CardSide(
                print_str=f'{self.english_subject} {self.english_past_participle} {self.english_print_suffix}',
                match_str=f'{self.english_subject} {self.english_past_participle}'
            )
        )

        return [
            past_card,
            past_participle_card
        ]

    @classmethod
    def from_dict(cls, inp):
        return cls(**inp)
