from random import random

import numpy as np

from gym_poker.envs import PokerEnv


class QtableNPC:
    """ Q-table base agent for simple poker

    Observation Space includes:
    Card1, Card2, BB/SB, Chips Amount [0 -- n/2 -- n -- 1.5n -- 2n]
      52 ,   52 ,   2  ,     4
    """

    def __init__(self, num_of_chips, qtable, st=None):
        """Constructs an agent for poker game

        :param num_of_chips: How many starting chips each player has
        :param qtable: Table for decision making
        :param st: Initial state (default none)
        """
        self.qt = qtable

        self.state = st
        self.bank_size = num_of_chips

    def make_a_move(self, pl, is_sb):
        """Makes a decision whenever to fold or play

        :param pl: Player object
        :param is_sb: Is the player small blind or not?
        :return action 0 for fold 1 for play:
        """
        observation_code = PokerEnv.encode(pl.hand, is_sb, pl.bank, self.bank_size)
        action = np.argmax(self.qt[observation_code])
        # (bluff) If the decision is to fold give a 10% chance that will go all in instead
        if action == 0 and random() > 0.9:
            action = 1
        return action
