import gym

from entities import *


class PokerEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.g = Game("P1", "Qtable", "P2", "Qtable")
        self.reset()

    def step(self, action):
        """Step

        returns ob, rewards, episode_over, info : tuple

        ob (list[Player,Player]) : next stage observation
            [player who is small blind,player who is big blind].
        rewards ([float,float]) :
            amount of reward achieved by the previous action
        :param action: [small blind action, big blind action]
                0 if fold, 1 otherwise
         """
        if action[0]:
            # Small blind went all in
            if action[1]:
                # BB called
                # Need to compare hands
                for c in range(5):
                    new_card = g.deck.draw_card()
                    for ep in self.g.p:
                        ep.hand.add_card(new_card)
                for pl in self.g.p:
                    pl.hand.sort()
                # get the absolute score of the hand and the best five cards
                results = []
                for ep in self.g.p:
                    results.append(Game.score(ep.hand))
                # select the winner
                winners = Game.determine_winner(results)
                # award the pot to the winner
                if winners.__len__() > 1:
                    # split the pot
                    self.g.split_the_pot()
                    # Give both players small reward
                    rewards = [1, 1]
                else:
                    rewards = []
                    # Reward the winner with chips won
                    rewards.insert(winners[0], self.g.p[winners[0]].bet)
                    # Penalty the loser with chips lost
                    rewards.insert(1 - winners[0], -self.g.p[1 - winners[0]].bet)
                    # Actually transfer the chips between players
                    self.g.player_won(self.g.p[winners[0]])
            else:
                # BB folded
                # Reward SB with amount won
                # Penalty BB by amount lost
                rewards = [self.g.pot, -self.g.bb_player().bet]
                # Transfer chips to SB
                self.g.bb_player().bank += self.g.pot
        else:
            # Small blind folded
            # Reward BB with 0 since their move didn't matter
            # Penalty SB by amount lost
            rewards = [-self.g.sb_player().bet, 0]
            # Transfer chips to BB
            self.g.bb_player().bank += self.g.pot
        # Change who is SB
        self.g.sb = 1 - self.g.sb
        self.g.new_step()
        self.g.players_draw_cards()
        ob = [self.g.sb_player(), self.g.bb_player()]
        return ob, rewards

    def reset(self, bank=50):
        """Initial setup for training

        :param bank : initial bank size
        :returns [small blind player, big blind player]
        """
        self.g = Game("P1", "Qtable", "P2", "Qtable", bank)
        self.g.place_blinds()
        self.g.players_draw_cards()
        # Return observation
        # [ Small Blind Player, Big Blind Player ]
        ob = [self.g.sb_player(), self.g.bb_player()]
        return ob

    def render(self, mode='human'):
        self.g.render_game()

    @staticmethod
    def encode(hand, small_blind, _num_of_chips, initial_num_of_chips):
        """Encoding and decoding code was lifted from openAI taxi gym"""
        # Sort hand and extract cards
        _sorted_hand = sorted(hand.cards, reverse=True)
        _card1 = _sorted_hand[0].encode()
        _card2 = _sorted_hand[1].encode()
        # Calculate coefficient of number of chips
        _coef_chips = 2 * _num_of_chips // initial_num_of_chips
        # Encode
        encoded = _card2
        encoded *= 52
        encoded += _card1
        encoded *= 2
        encoded += small_blind
        encoded *= 4
        encoded += _coef_chips
        return encoded

    @staticmethod
    def decode(_code):
        """Encoding and decoding code was lifted from openAI taxi gym"""
        _out = [_code % 4]
        _code = _code // 4
        _out.append(_code % 2)
        _code = _code // 2
        _card1 = Card.decode(_code % 52)
        _code = _code // 52
        _card2 = Card.decode(_code)
        assert 0 <= _code < 52
        _hand = Hand()
        _hand.add_card(_card1)
        _hand.add_card(_card2)
        _out.append(_hand)
        return _out


def test_encoder_decoder():
    """Test encoder and decoder"""
    hand1 = Hand()
    initial_chips = 10

    for chips in range(initial_chips * 2):
        for sb in range(2):
            for card1_code in range(52):
                for card2_code in range(52):
                    if card1_code == card2_code:
                        continue
                    # Create hand
                    card1 = Card.decode(card1_code)
                    card2 = Card.decode(card2_code)
                    hand1.clear_hand()
                    hand1.add_card(card1)
                    hand1.add_card(card2)
                    hand1.cards = sorted(hand1.cards, reverse=True)
                    # Encode and decode
                    code = PokerEnv.encode(hand1, sb, chips, initial_chips)
                    [new_chips, new_small_blind, new_hand] = PokerEnv.decode(code)
                    assert new_chips == 2 * chips // initial_chips
                    assert new_small_blind == sb
                    assert new_hand.cards[0] == hand1.cards[0]
                    assert new_hand.cards[1] == hand1.cards[1]


if __name__ == "__main__":
    # test_encoder_decoder()
    pass
