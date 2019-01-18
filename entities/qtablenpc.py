from random import random

import numpy as np


class QtableNPC:
    """ Q-table base agent for simple poker

    Observation Space includes:
    Card1, Card2, BB/SB, Chips Amount [0 -- n/2 -- n -- 1.5n -- 2n]
      52 ,   52 ,   2  ,     4
    """

    def __init__(self, qtable=None, bluff=False):
        """Constructs an agent for poker game

        :param qtable: Table for decision making
        """
        self.b = bluff
        if qtable is not None:
            self.qt = qtable
        else:
            n_s = 52 * 52 * 2 * 4
            n_a = 2
            try:
                # Load Qtable from file
                with np.load('Qtable/qtablenpc.npz') as data:
                    self.qt = data['qtable']
            except IOError:
                # File does not exists
                self.qt = np.zeros([n_s, n_a])
                # Make the agent prefer to go all in and not to fold
                self.qt[range(n_s), 0] = 48
                self.qt[range(n_s), 1] = 50

    def make_a_move(self, observation_code):
        """Makes a decision whenever to fold or play

        :param observation_code: Code of the current state
        """
        action = np.argmax(self.qt[observation_code])
        # (bluff) If the decision is to fold give a 10% chance that will go all in instead
        if self.b and action == 0 and random() > 0.9:
            action = 1
        return action
