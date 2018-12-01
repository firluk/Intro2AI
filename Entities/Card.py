from Entities.Suit import get_icon


class Card:
    """The Card class

    Has a suit, a val, and a rank.

    Example:
        Queen of diamonds will have the following characteristics:
        suit - "♦"
        val - "Q"
        rank - 12
    """

    def __init__(self, suit = None, rank = None):
        self.suit = suit
        """Suit of the card"""
        self.rank = rank
        """Numerical value of the card"""
        if rank:
            self.val = rank_to_value(rank)
        else:
            self.val = None
        """Literal value of the card"""

    def to_string(self):
        return str(self.val) + get_icon(str(self.suit))


def rank_to_value(v):
    values = {"10": "T", "11": "J", "12": "Q", "13": "K", "14": "A"}
    if 1 < v < 10:
        return str(v)
    else:
        return values[str(v)]
