import random

from Entities.Card import Card
from Entities.Suit import pull_suit


def con_val(v):
    values = {"9": "T", "10": "J", "11": "Q", "12": "K", "0": "A"}
    v2 = int(v)
    if v2 > 0 & v2 < 9:
        return v
    else:
        return values[v]


def get_deck():
    _deck = []
    for s in range(4):
        _suit = pull_suit()
        for v in range(13):
            _new_card = Card()
            _new_card.suit = _suit
            _new_card.val = con_val(v)
            _deck.append(_new_card)
    return _deck


def get_deck_shuffled():
    _deck = []
    for s in range(4):
        _suit = pull_suit()
        for v in range(13):
            _new_card = Card()
            _new_card.suit = _suit
            _new_card.val = con_val(v)
            _deck.append(_new_card)
    random.shuffle(_deck)
    return _deck


def draw_card():
    _deck = []
    for s in range(4):
        _suit = pull_suit()
        for v in range(13):
            _new_card = Card()
            _new_card.suit = _suit
            _new_card.val = con_val(v)
            _deck.append(_new_card)
    random.shuffle(_deck)
    for i in range(52):
        yield _deck.pop()
