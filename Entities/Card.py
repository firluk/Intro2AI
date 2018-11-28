from Entities.Suit import get_icon


class Card:

    def __init__(self):
        self.suit = None
        self.val = None
        self.rank = None

    def to_string(self):
        return str(self.val) + get_icon(str(self.suit))
