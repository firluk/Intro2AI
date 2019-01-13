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
        return self.suit == other.suit and self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank or (
                self.rank == other.rank and self.suit < other.suit)

    # for readability in debugging
    def __str__(self):
        return str(self.val) + get_icon(str(self.suit))

    def __repr__(self):
        return self.__str__()

    # for hashing to sets and dictionaries
    def __hash__(self):
        return hash(self.__str__())

    def encode(self):
        return (self.rank - 2) + 13 * get_suit_value(self.suit)

    @staticmethod
    def decode(cd):
        """"returns card corresponding to encode_to_vector"""
        rank = cd % 13 + 2
        suit = get_suit_from_value(int(cd / 13))
        return Card(suit, rank)


def rank_to_value(v):
    values = {"10": "T", "11": "J", "12": "Q", "13": "K", "14": "A"}
    if 1 < v < 10:
        return str(v)
    else:
        return values[str(v)]


def get_icon(suit):
    suits = {"Spade": "♠", "Club": "♣", "Diamond": "♦", "Heart": "♥"}
    return suits[suit]


def get_suit_value(suit):
    suits = {"Spade": 0, "Club": 1, "Diamond": 2, "Heart": 3}
    return suits[suit]


def get_suit_from_value(suit_code):
    suits = {0: "Spade", 1: "Club", 2: "Diamond", 3: "Heart"}
    return suits[suit_code]


# testing the sorting
if __name__ == "__main__":
    aceOfHeart = Card("Heart", 14)
    aceOfSpade = Card("Spade", 14)
    twoOfSpade = Card("Spade", 2)
    sevenOfSpade = Card("Spade", 7)
    sixOfSpade = Card("Spade", 6)
    fiveOfSpade = Card("Spade", 5)
    print(sorted([fiveOfSpade, sixOfSpade, aceOfSpade, aceOfHeart, twoOfSpade,
                  sevenOfSpade]))

# testing the sorting
if __name__ == "__main__":
    t_codes = []
    from entities import deck

    for t_card in deck.get_deck():
        t_code = t_card.encode()
        t_codes.append(t_code)
        decoded_card = Card.decode(t_code)
        if t_card != decoded_card:
            print(str(t_card) + " " + str(decoded_card))
    t_codes.sort()
    print(t_codes)
