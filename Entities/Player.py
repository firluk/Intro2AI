from Entities.Hand import Hand


class Player:

    def __init__(self, n, b = 10):
        self.hand = Hand()
        self.name = n
        self.bank = b
        self.bet = 0

    def draw_new_card_from_deck(self, deck):
        self.hand.add_card(deck.draw_card())

    def take_card(self, card):
        self.hand.add_card(card)
