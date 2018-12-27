import numpy as np

from entities.qtablenpc import QtableNPC
from gym_poker.envs import PokerEnv


class QTableTrainer:
    """ Q-table base agent for simple poker

        Observation Space includes:
        Card1, Card2, BB/SB, Chips Amount [0 -- n/2 -- n -- 1.5n -- 2n]
          52 ,   52 ,   2  ,     4
        """

    def __init__(self, num_of_chips):
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1
        n_s = 52 * 52 * 2 * 4
        n_a = 2
        try:
            # Load Qtable from file
            with np.load('/qtablenpc.npz') as data:
                self.qt = data['qtable']
        except IOError:
            # File does not exists
            self.qt = np.zeros([n_s, n_a])
            # Make the agent prefer to go all in and not to fold
            self.qt[range(n_s), 0] = -1
            self.qt[range(n_s), 1] = 1
        self.agent = QtableNPC(num_of_chips, self.qt)
        self.nc = num_of_chips

    def train_agent(self):
        env = PokerEnv(self.nc)
        for i in range(100):  # replace later with 52 * 52 * 2 * 4 * 100
            done = False
            while not done:
                player1 = env.ob[0]
                player2 = env.ob[1]
                p1_state = PokerEnv.encode(player1.hand, 0, player1.bank, self.nc)
                p2_state = PokerEnv.encode(player2.hand, 1, player2.bank, self.nc)
                action1 = self.agent.make_a_move(player1, 0)
                action2 = self.agent.make_a_move(player2, 1)
                observation, rewards, done = env.step([action1, action2])
                p1_reward, p2_reward = rewards[0], rewards[1]

                old_value = self.qt[p1_state][action1]
                new_value = (1 - self.alpha) * old_value + self.alpha * p1_reward
                self.qt[p1_state][action1] = new_value

                old_value = self.qt[p2_state][action2]
                new_value = (1 - self.alpha) * old_value + self.alpha * p2_reward
                self.qt[p2_state][action2] = new_value
            if i % 1000 == 0:
                np.savez('/qtablenpc.npz', qtable=self.qt)
            env.reset(self.nc)
