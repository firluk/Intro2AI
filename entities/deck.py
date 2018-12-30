import random

from entities.card import Card


def get_deck():
    _deck = []
    for _suit in pull_suit():
        for v in range(2, 15):
            _new_card = Card(suit=_suit, rank=v)
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


def pull_suit():
    _suits = ["Spade", "Club", "Diamond", "Heart"]
    for i in range(4):
        yield _suits[i]
