from Entities.Suit import get_icon


class Card:
    suit = None
    val = None

    def to_string(self):
        return str(self.val) + get_icon(self.suit)
