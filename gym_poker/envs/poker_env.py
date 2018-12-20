import gym

from Entities import Card
from Entities.Hand import Hand


class PokerEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        pass

    def _step(self, action):
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
        # return ob, reward, episode_over, info

    def _reset(self):
        pass

    def _render(self, mode='human', close=False):
        pass

    def _take_action(self, action):
        pass

    def _get_reward(self):
        pass

    def encode(self, hand, small_blind):
        sorted_hand = sorted(hand.cards, reverse=True)
        coef_blind = 52 * 52 if small_blind else 0
        self.encoded = coef_blind + sorted_hand[0].encode() * 52 + sorted_hand[
            1].encode()
        # self.encoded = str(sorted(hand.cards)) + str(small_blind)

    @staticmethod
    def decode(code):
        small_blind = False
        hand = Hand()
        if code > 52 * 52:
            small_blind = True
            code -= 52 * 52
        # encode = 52*code1 + encode
        # % 52
        card2 = Card.decode(code % 52)
        code = code - (code % 52)
        card1 = Card.decode(int(code / 52))
        hand.add_card(card1)
        hand.add_card(card2)
        return small_blind, hand
