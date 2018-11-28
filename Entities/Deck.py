import random

from Entities.Card import Card
from Entities.Suit import pull_suit


def con_val(v):
    values = {"10": "T", "11": "J", "12": "Q", "13": "K", "1": "A"}
    v += 1
    if 1 < v < 10:
        return str(v)
    else:
        return values[str(v)]


def get_deck():
    _deck = []
    for _suit in pull_suit():
        for v in range(13):
            _new_card = Card()
            _new_card.suit = _suit
            _new_card.val = con_val(v)
            if v == 0:
                _new_card.rank = 13
            else:
                _new_card.rank = v
            _deck.append(_new_card)
    return _deck


def get_deck_shuffled():
    _deck = get_deck()
    random.shuffle(_deck)
    random.shuffle(_deck)
    random.shuffle(_deck)
    random.shuffle(_deck)
    return _deck


class Deck:

    def __init__(self):
        self._deck = get_deck_shuffled()

    def draw_card(self):
        return self._deck.pop()

    def cards_left(self):
        return self._deck.__len__()
