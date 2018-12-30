class Hand:

    def __init__(self):
        self.cards = []

    def __str__(self):
        s = ''
        for c in self.cards:
            s += str(c) + ","
        return s.rsplit(",", 1)[0]

    def add_card(self, card):
        self.cards.append(card)

    def clear_hand(self):
        self.cards.clear()

    def sort(self):
        """Will sort cards from low to high"""
        self.cards.sort(key=lambda cc: cc.rank, reverse=False)


# testing the sorting
if __name__ == "__main__":
    from entities import card

    aceOfHeart = card.Card("Heart", 14)
    aceOfSpade = card.Card("Spade", 14)
    twoOfSpade = card.Card("Spade", 2)
    sevenOfSpade = card.Card("Spade", 7)
    sixOfSpade = card.Card("Spade", 6)
    fiveOfSpade = card.Card("Spade", 5)
    hand = Hand()
    hand.add_card(aceOfSpade)
    hand.add_card(sixOfSpade)
    hand.add_card(twoOfSpade)
    hand.add_card(aceOfHeart)
    print(hand.cards)
    hand.sort()
    print(hand.cards)
