import numpy as np

from entities import Hand


class State:
    """The State class represents the encoded hand to hashable to Q-table value
    """

    def __init__(self, hand: Hand, small_blind: bool):
        sorted_hand = sorted(hand.cards, reverse=True)
        if small_blind:
            leading_bit = 52 * 52
        else:
            leading_bit = 0
        self.encoded = leading_bit + sorted_hand[0].encode() * 52 + sorted_hand[1].encode()
        # self.encoded = str(sorted(hand.cards)) + str(small_blind)


if __name__ == "__main__":
    pass
