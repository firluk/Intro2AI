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

    def sort(self):
        """Will sort cards from low to high"""
        self.cards.sort(key=lambda cc: cc.rank, reverse=False)


# testing the sorting
if __name__ == "__main__":
    from Entities import Card

    aceOfHeart = Card.Card("Heart", 14)
    aceOfSpade = Card.Card("Spade", 14)
    twoOfSpade = Card.Card("Spade", 2)
    sevenOfSpade = Card.Card("Spade", 7)
    sixOfSpade = Card.Card("Spade", 6)
    fiveOfSpade = Card.Card("Spade", 5)
    hand = Hand()
    hand.add_card(aceOfSpade)
    hand.add_card(sixOfSpade)
    hand.add_card(twoOfSpade)
    hand.add_card(aceOfHeart)
    print(hand.cards)
    hand.sort()
    print(hand.cards)
