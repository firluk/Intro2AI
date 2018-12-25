import gym
from gym import spaces

from Entities.Card import Card
from Entities.Hand import Hand

SMALL_BLIND_COEFFICIENT = 52 * 53
CHIPS_COEFFICIENT = SMALL_BLIND_COEFFICIENT * 2


class PokerEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        """
        Observation Space includes:
        Card1, Card2, BB/SB, Chips Amount [0 -- n/2 -- n -- 1.5n -- 2n]
          52 ,   52 ,   2  ,     4
        """
        self.observation_space = spaces.Tuple(
            [spaces.Discrete(52), spaces.Discrete(52), spaces.Discrete(2), spaces.Discrete(4)])
        self.action_space = spaces.Discrete(2)

    def step(self, action):
        """
        Parameters
        ----------
        action :

        Returns
        -------
        ob, reward, episode_over, info : tuple
        ob (object) :
            an environment-specific object representing your observation of
            the environment.
        reward (float) :
            amount of reward achieved by the previous action. The scale
            varies between environments, but the goal is always to increase
            your total reward.
        episode_over (bool) :
            whether it's time to reset the environment again. Most (but not
            all) tasks are divided up into well-defined episodes, and done
            being True indicates the episode has terminated. (For example,
            perhaps the pole tipped too far, or you lost your last life.)
        info (dict) :
             diagnostic information useful for debugging. It can sometimes
             be useful for learning (for example, it might contain the raw
             probabilities behind the environment's last state change).
             However, official evaluations of your agent are not allowed to
             use this for learning.
         """
        pass

    def reset(self):
        pass

    def render(self, mode='human'):
        pass

    def _take_action(self, action):
        pass

    def _get_reward(self):
        pass

    @staticmethod
    def encode(hand, small_blind, _num_of_chips, initial_num_of_chips):
        """Encoding and decoding code was lifted from openAI taxi gym"""
        # Sort hand and extract cards
        _sorted_hand = sorted(hand.cards, reverse=True)
        _card1 = _sorted_hand[0].encode()
        _card2 = _sorted_hand[1].encode()
        # Calculate coefficient of small blind or big blind
        _coef_blind = 1 if small_blind else 0
        # Calculate coefficient of number of chips
        if _num_of_chips < initial_num_of_chips:
            _coef_chips = 0 if _num_of_chips < (initial_num_of_chips / 2) else 1
        else:
            _coef_chips = 2 if _num_of_chips < (initial_num_of_chips * 1.5) else 3
        # Encode
        encoded = _card2
        encoded *= 52
        encoded += _card1
        encoded *= 2
        encoded += _coef_blind
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
                    assert new_chips == int((chips / (2 * initial_chips)) * 4)
                    assert new_small_blind == sb
                    assert new_hand.cards[0] == hand1.cards[0]
                    assert new_hand.cards[1] == hand1.cards[1]


if __name__ == "__main__":
    # test_encoder_decoder()
    pass
