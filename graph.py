import json
import random

from nouns import Noun


def graph():
    with open('words.json') as _fd:
        words_dict = json.load(_fd)

    word_type_dataclasses = {
        'nouns': Noun
    }

    words = [
        word_type_dataclasses[word_type](**word if isinstance(word, dict) else word)
        for word_type, words in words_dict.items()
        for word in words
    ]
    random.shuffle(words)

    yield from (
        card.graph_output()
        for word in words
        for card in word.get_cards()
    )
