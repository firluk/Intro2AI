class Hand:

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def clear_hand(self):
        self.cards.clear()

    def to_string(self):
        s = ''
        for c in self.cards:
            s += c.to_string() + ","
        return s.rsplit(",", 1)[0]
