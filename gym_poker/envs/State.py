from Entities import Hand
from Entities import Card


class State:
    """The State class represents the encoded hand to hashable to Q-table value
    """

    def __init__(self, hand: Hand, small_blind: bool):
        self.encoded = str(sorted(hand.cards))+str(small_blind)


# testing the sorting
if __name__ == "__main__":
    aceOfHeart = Card.Card("Heart", 14)
    aceOfSpade = Card.Card("Spade", 14)
    twoOfSpade = Card.Card("Spade", 2)
    sevenOfSpade = Card.Card("Spade", 7)
    sixOfSpade = Card.Card("Spade", 6)
    fiveOfSpade = Card.Card("Spade", 5)
    print(sorted([fiveOfSpade, sixOfSpade, aceOfSpade, aceOfHeart, twoOfSpade, sevenOfSpade]))
    hand1 = Hand.Hand()
    hand1.add_card(aceOfHeart)
    hand1.add_card(aceOfSpade)
    state1 = State(hand1, True)
    print(state1.encoded)
