from random import random

import numpy as np

from entities.qtablenpc import QtableNPC
from gym_poker.envs.poker_env import PokerEnv


class QTableTrainer:
    """ Q-table base agent for simple poker

        Observation Space includes:
        Card1, Card2, BB/SB, Chips Amount [0 -- n/2 -- n -- 1.5n -- 2n]
          52 ,   52 ,   2  ,     4
        """

    def __init__(self, num_of_chips):

        self.agent = QtableNPC()
        self.nc = num_of_chips

    def train_agent(self):
        env = PokerEnv(self.nc)
        alpha = 0.1
        epsilon_min = 0.1
        epsilon = 0.1
        cycles = 1000000  # 5000000 is one hour
        for i in range(cycles):  # replace later with 52 * 52 * 2 * 4 * 100
            # epsilon = max(epsilon_min, (cycles - i) / cycles)
            done = False
            while not done:
                player1 = env.ob[0]
                player2 = env.ob[1]
                p1_state = PokerEnv.encode(player1.hand, 0, player1.bank, self.nc)
                p2_state = PokerEnv.encode(player2.hand, 1, player2.bank, self.nc)

                # exploitation vs exploration

                if random() < epsilon:
                    action1 = 0 if random() > 0.5 else 1
                else:
                    action1 = self.agent.make_a_move(PokerEnv.encode(player1.hand, 0, player1.bank, self.nc))
                if random() < epsilon:
                    action2 = 0 if random() > 0.5 else 1
                else:
                    action2 = self.agent.make_a_move(PokerEnv.encode(player2.hand, 1, player2.bank, self.nc))

                observation, rewards, done = env.step([action1, action2])

                # if the game was lost completely, the punishment is multiplied
                if done:
                    for (ind, r) in enumerate(rewards):
                        if r < 0:
                            rewards[ind] = -20
                            rewards[1 - ind] = 40

                p1_reward, p2_reward = rewards[0], rewards[1]
                old_value = self.agent.qt[p1_state][action1]
                new_value = (1 - alpha) * old_value + alpha * p1_reward
                self.agent.qt[p1_state][action1] = new_value
                # if player 1 folded, nothing to learn here
                if p2_reward != 0:
                    old_value = self.agent.qt[p2_state][action2]
                    new_value = (1 - alpha) * old_value + alpha * p2_reward
                    self.agent.qt[p2_state][action2] = new_value
            if i % 10000 == 0:
                np.savez('Qtable/qtablenpc.npz', qtable=self.agent.qt)
                print(cycles - i)
            env.reset(self.nc)
