from Entities.Suit import get_icon
from functools import total_ordering


@total_ordering
class Card:
    """The Card class

    Has a suit, a val, and a rank.

    Example:
        Queen of diamonds will have the following characteristics:
        suit - "♦"
        val - "Q"
        rank - 12
    """

    def __init__(self, suit=None, rank=None):
        self.suit = suit
        """Suit of the card"""
        self.rank = rank
        """Numerical value of the card"""
        if rank:
            self.val = rank_to_value(rank)
        else:
            self.val = None
        """Literal value of the card"""

    # the order implemented and equality for sorting and hashing
    def __eq__(self, other):
        return not self.suit == other and self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank or (self.rank == other.rank and self.suit < other.suit)

    # for readability in debugging
    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.__str__()

    # for hashing to sets and dictionaries
    def __hash__(self):
        return hash(self.to_string())

    def to_string(self):
        return str(self.val) + get_icon(str(self.suit))


def rank_to_value(v):
    values = {"10": "T", "11": "J", "12": "Q", "13": "K", "14": "A"}
    if 1 < v < 10:
        return str(v)
    else:
        return values[str(v)]


# testing the sorting
if __name__ == "__main__":
    aceOfHeart = Card("Heart", 14)
    aceOfSpade = Card("Spade", 14)
    twoOfSpade = Card("Spade", 2)
    sevenOfSpade = Card("Spade", 7)
    sixOfSpade = Card("Spade", 6)
    fiveOfSpade = Card("Spade", 5)
    print(sorted([fiveOfSpade, sixOfSpade, aceOfSpade, aceOfHeart, twoOfSpade, sevenOfSpade]))
