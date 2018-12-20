import numpy as np

from Entities import Card
from Entities import Hand


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


# testing the sorting
if __name__ == "__main__":
    aceOfHeart = Card.Card("Heart", 14)
    aceOfSpade = Card.Card("Spade", 14)
    # twoOfSpade = Card.Card("Spade", 2)
    # sevenOfSpade = Card.Card("Spade", 7)
    # sixOfSpade = Card.Card("Spade", 6)
    # fiveOfSpade = Card.Card("Spade", 5)
    # print(sorted([fiveOfSpade, sixOfSpade, aceOfSpade, aceOfHeart, twoOfSpade, sevenOfSpade]))
    # state1 = State(hand1, True)
    # print(state1.encoded)
    from Entities import Deck

    dictionary_based_q_table = {}

    deck = Deck.get_deck()
    deck2 = Deck.get_deck()
    codes = []
    for small_blind in [True, False]:
        for card1 in deck:
            for card2 in deck2:
                if card1 == card2:
                    continue
                # if card1.rank < card2.rank:
                #     continue
                hand = Hand.Hand()
                hand.add_card(card1)
                hand.add_card(card2)
                state = State(hand, small_blind)
                code = state.encoded
                if code not in codes:
                    codes.append(code)
                    dictionary_based_q_table[code] = (0, 0)

    import sys

    print("size dict " + str(sys.getsizeof(dictionary_based_q_table)))
    table_based_q_table = np.zeros([52 * 52 * 2, 2])

    print("size np " + str(sys.getsizeof(table_based_q_table)))

    codes.sort()
    print(codes)
    print(codes.__len__())
    print(set(codes).__len__())

    # print(sorted(deck, key=lambda i: i.encode()))
    #
    # hand = Hand.Hand()
    # hand.add_card(aceOfHeart)
    # hand.add_card(aceOfSpade)

    #
    # state = State(hand1, True)
    # print(state.tupled)
