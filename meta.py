import dataclasses
import inspect
import os
from typing import Iterable, Optional

import mg


@dataclasses.dataclass
class CardSide:
    print_str: str
    match_str: str = None

    def to_node(self):
        return mg.node.Node(self.print_str, match_str=self.match_str)

    @classmethod
    def from_dict(cls, inp):
        if isinstance(inp, dict):
            return cls(**inp)
        return cls(str(inp))


@dataclasses.dataclass
class Card:
    front: CardSide
    back: CardSide
    topic: Optional[str] = None

    def graph_output(self):
        front_node = self.front.to_node()
        back_node = self.back.to_node()
        if self.topic:
            return front_node, back_node, self.topic
        return front_node, back_node

    @classmethod
    def from_dict(cls, inp):
        inp = inp.copy()
        inp['front'] = CardSide.from_dict(inp['front'])
        inp['back'] = CardSide.from_dict(inp['back'])
        return cls(**inp)


def graph(cards: Iterable[Card], set_working_dir=True):
    if set_working_dir:
        frame = inspect.stack()[1]
        set_working_dir(frame=frame)

    for card in cards:
        yield card.graph_output()


def set_working_dir(frame=None):
    if frame is None:
        frame = inspect.stack()[1]
    caller_filepath = frame.filename
    caller_filename = os.path.basename(caller_filepath)
    caller_filename, _ = os.path.splitext(caller_filename)

    this_dir = os.path.dirname(__file__)
    new_dir = os.path.join(this_dir, 'data', f'{caller_filename}.mg')

    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

    os.chdir(new_dir)
