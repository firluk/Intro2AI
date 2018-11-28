from Entities.Deck import Deck
from Entities.Player import Player


class Game:

    def __init__(self, player_1_name = "Player 1", player_1_is_human = False,
                 player_2_name = "Player 2", player_2_is_human = False):
        """Create a new game

        player_1_name - player 1 name.
        player_1_is_human - if a player is a human.
        player_2_name - player 2 name.
        player_2_is_human - if a player is a human.
        """
        self.turn = 0
        self.step = 0
        self.pot = 0
        self.bet = 0
        self.done = False
        self._p1 = Player(player_1_name)
        self._p2 = Player(player_2_name)
        self._p1.h = player_1_is_human
        self._p2.h = player_2_is_human
        self.deck = Deck()
        self.p = [self._p1, self._p2]

    def next_player(self):
        self.turn = 1 - self.turn

    def render_game(self):
        print("Player 1 : " + self._p1.name + ", Cards : " +
              self._p1.hand.to_string())
        print("Player 2 : " + self._p2.name + ", Cards : " +
              self._p2.hand.to_string())
        print(self.p[self.turn].name + " is small blind")

    def a_player(self):
        return self.p[self.turn]

    def na_player(self):
        return self.p[1 - self.turn]

    def player_all_in(self, p):
        self.bet = p.bank
        self.pot += p.bank
        p.bank = 0

    def player_call(self, p):
        if p.bank <= self.bet:
            self.player_all_in(p)
        else:
            self.pot += self.bet
            p.bank -= self.bet

    def opponent_folded(self, p):
        p.bank += self.pot
        self.pot = 0

    def place_blinds(self):
        self.a_player().bank -= 1
        self.na_player().bank -= 2
        self.pot += 3

    def players_draw_cards(self):
        for p in self.p:
            for i in range(2):
                p.take_card(self.deck.draw_card())

    def new_step(self):
        for a in self.p:
            a.hand.clear_hand()
        self.deck = Deck()
