from random import random
from typing import List

from keras.layers import np

from entities import Player
from entities.neuralnetworknpc import NeuralNetworkNPC, save_poker_model
from gym_poker.envs.neural_net_poker_env import NeuralNetPokerEnv


class NeuralNetworkTrainer:
    """ Neural network base agent for simple poker

        Observation Space includes:
        Card1, Card2, BB/SB, Chips Amount [0 -- n/2 -- n -- 1.5n -- 2n]
          52 ,   52 ,   2  ,     4
        """

    def __init__(self, num_of_chips):

        npc = NeuralNetworkNPC()
        self.model = npc.model
        self.nc = num_of_chips

    def train_agent(self):
        num_episodes = 1000000

        env = NeuralNetPokerEnv(self.nc)

        alpha = 0.1
        eps = 0.5
        decay_factor = 0.999
        for i in range(num_episodes):
            s: List[Player] = env.reset(self.nc)
            player1: Player = s[0]
            player2: Player = s[1]
            eps *= decay_factor
            if i % 100 == 0:
                print("Episode {} of {}".format(i + 1, num_episodes))
            done = False
            while not done:

                if player1.type == "n":
                    # small blind player
                    ind = 0
                    if np.random.random() < eps:
                        a1 = 0 if random() > 0.5 else 1
                    else:
                        # encode state to vector
                        state: np.ndarray = NeuralNetPokerEnv.encode(player1.hand, 0, player1.bank, self.nc)
                        a1 = np.argmax(self.model.predict(state))
                    a = a1
                    a2 = 0 if random() > 0.5 else 1
                else:
                    # big blind player
                    ind = 1
                    if np.random.random() < eps:
                        a2 = 0 if random() > 0.5 else 1
                    else:
                        # encode state to vector
                        state: np.ndarray = NeuralNetPokerEnv.encode(player2.hand, 1, player2.bank, self.nc)
                        a2 = np.argmax(self.model.predict(state))
                    a = a2
                    a1 = 0 if random() > 0.5 else 1

                new_s, r, done, _ = env.step([a1, a2])

                state: np.ndarray = NeuralNetPokerEnv.encode(player1.hand, 0, player1.bank, self.nc)

                old_value = self.model.predict(state)
                post_action_value = (1 - alpha) * old_value[0][a] + alpha * r[ind]
                target_value = old_value
                target_value[0][a] = post_action_value

                self.model.fit(state, target_value, 1, verbose=0)

            if i % 1000 == 0:
                save_poker_model(self.model)


if __name__ == "__main__":
    neural_network = NeuralNetworkTrainer(50)
    neural_network.train_agent()
