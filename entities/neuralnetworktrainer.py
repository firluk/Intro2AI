from random import random
from typing import List

from keras.layers import np

from entities import Player
from entities.neuralnetworknpc import NeuralNetworkNPC, save_poker_model, classify_prediction
from gym_poker.envs.neural_net_poker_env import NeuralNetPokerEnv


class NeuralNetworkTrainer:
    """ Neural network base agent for simple poker

        Observation Space includes:
        Card1, Card2, BB/SB, Chips Amount [0 -- n/2 -- n -- 1.5n -- 2n]
          52 ,   52 ,   2  ,     4
        """

    def __init__(self, num_of_chips=4):

        npc = NeuralNetworkNPC()
        self.model = npc.model
        self.nc = num_of_chips

    def train_agent(self, enforce_play=False, both_neural=False):
        num_episodes = 1000000

        env = NeuralNetPokerEnv(self.nc)

        alpha = 0.1
        eps = 0.9
        decay_factor = 0.999
        gamma = 0.6

        save_poker_model(self.model, "initial")

        for i in range(num_episodes):
            s: List[Player] = env.reset(self.nc, rand_bank_dist=True)
            player1: Player = s[0]
            player2: Player = s[1]
            eps *= decay_factor
            if i % 100 == 0:
                print("Episode {} of {}".format(i + 1, num_episodes))

            if both_neural:
                if np.random.random() < eps:
                    a1 = 0 if random() > 0.5 else 1
                else:
                    # encode state to vector
                    state: np.ndarray = NeuralNetPokerEnv.encode(player1.hand, 0, player1.bank, self.nc)
                    a1 = classify_prediction(self.model.predict(state))

                if np.random.random() < eps:
                    a2 = 0 if random() > 0.5 else 1
                else:
                    # encode state to vector
                    state: np.ndarray = NeuralNetPokerEnv.encode(player2.hand, 0, player2.bank, self.nc)
                    a2 = classify_prediction(self.model.predict(state))

                if enforce_play:
                    a1, a2 = 1, 1

                old_state1: np.ndarray = NeuralNetPokerEnv.encode(player1.hand, 0, player1.bank, self.nc)
                old_state2: np.ndarray = NeuralNetPokerEnv.encode(player2.hand, 0, player2.bank, self.nc)

                new_s, r, done, _ = env.step([a1, a2])
                # only interested in our agents reward as the opponent is random p
                old_reward1 = norm_reward(r[0])
                old_reward2 = norm_reward(r[1])
                old_value1 = self.model.predict(old_state1)
                old_value2 = self.model.predict(old_state2)
                if done:
                    # only relevant if we want to reward for opponent folds

                    post_action_value1 = (1 - alpha) * old_value1 + (alpha) * old_reward1
                    # self.model.fit(old_state1, np.array(post_action_value1), epochs=1, verbose=0)
                    # if old_reward2 != 0:
                    #     post_action_value2 = (1 - alpha) * old_value2 + (alpha) * old_reward2
                    #     self.model.fit(old_state2, np.array(post_action_value2), epochs=1, verbose=0)
                    # self.model.fit \
                    #     (np.array([old_state1, old_state2]),
                    #      np.array([post_action_value1, post_action_value2]),
                    #      epochs=1,
                    #      verbose=0)
                else:
                    # we take only 1 from as we
                    new_s, r, done, _ = env.step([a1, a2])
                    new_state1 = NeuralNetPokerEnv.encode(player1.hand, 0, player1.bank, self.nc)
                    new_state2 = NeuralNetPokerEnv.encode(player2.hand, 0, player2.bank, self.nc)
                    new_reward1 = norm_reward(r[0])
                    new_reward2 = norm_reward(r[1])
                    post_action_value1 = 0.5 + ((1 - alpha) * (old_value1 - 0.5) + alpha * gamma * new_reward1)
                    post_action_value2 = 0.5 + ((1 - alpha) * (old_value2 - 0.5) + alpha * gamma * new_reward2)
                    # self.model.fit\
                    #     (np.array([old_state1, new_state1, old_state2, new_state2]),
                    #      np.array([post_action_value1, post_action_value1, post_action_value2, post_action_value2]),
                    #      epochs=1,
                    #      verbose=0)
                    # self.model.fit(old_state1, np.array([classify_prediction(0.5 + post_action_value1/2)]), epochs=1, verbose=0)
                    # self.model.fit(old_state2, np.array([classify_prediction(0.5 + post_action_value1/2)]), epochs=1, verbose=0)
                    # self.model.fit(new_state1, np.array([classify_prediction(0.5 + new_reward1/2)]), epochs=1, verbose=0)
                    # self.model.fit(new_state2, np.array([classify_prediction(0.5 + new_reward2/2)]), epochs=1, verbose=0)
                    self.model.fit(old_state1, np.array(post_action_value1), epochs=1, verbose=0)
                    self.model.fit(old_state2, np.array(post_action_value2), epochs=1, verbose=0)
                    self.model.fit(new_state1, np.array(post_action_value1), epochs=1, verbose=0)
                    self.model.fit(new_state2, np.array(post_action_value2), epochs=1, verbose=0)

                if i % 1000 == 1:
                    save_poker_model(self.model, i)

            else:
                # episode is short (1 or 2 states in episode) no need for 'while not done'
                if player1.type == "n":
                    neural_player = player1
                    # small blind player
                    ind = 0
                    if np.random.random() < eps:
                        a1 = 0 if random() > 0.5 else 1
                    else:
                        # encode state to vector
                        state: np.ndarray = NeuralNetPokerEnv.encode(player1.hand, 0, player1.bank, self.nc)
                        a1 = classify_prediction(self.model.predict(state))
                    a2 = 0 if random() > 0.5 else 1
                else:
                    # big blind player
                    neural_player = player2
                    ind = 1
                    if np.random.random() < eps:
                        a2 = 0 if random() > 0.5 else 1
                    else:
                        # encode state to vector
                        state: np.ndarray = NeuralNetPokerEnv.encode(player2.hand, 1, player2.bank, self.nc)
                        a2 = classify_prediction(self.model.predict(state))
                    a1 = 0 if random() > 0.5 else 1

                if enforce_play:
                    a1, a2 = 1, 1

                old_state: np.ndarray = NeuralNetPokerEnv.encode(neural_player.hand, 0, neural_player.bank, self.nc)
                new_s, r, done, _ = env.step([a1, a2])
                # only interested in our agents reward as the opponent is random p
                old_reward = norm_reward(r[ind])
                old_value = self.model.predict(old_state)
                if done:
                    # only relevant if we want to reward for opponent folds
                    post_action_value = (1 - alpha) * old_value[0] + (alpha) * old_reward
                    # self.model.fit(old_state, np.array([1 if post_action_value > 0 else 0]), 1, verbose=0)
                    # self.model.fit(old_state, np.array([post_action_value]), epochs=1, verbose=0)
                else:
                    # we take only 1 from as we
                    new_s, r, done, _ = env.step([a1, a2])
                    new_state = NeuralNetPokerEnv.encode(neural_player.hand, 0, neural_player.bank, self.nc)
                    new_reward = norm_reward(r[ind])
                    post_action_value = old_value + ((1 - alpha) * old_reward + alpha * gamma * new_reward)
                    print("{},{},{}".format(old_reward, new_reward, post_action_value))
                    # self.model.fit(new_state, np.array([1 if post_action_value > 0 else 0]), epochs=1, verbose=0)

                    self.model.fit(old_state, np.array(post_action_value), epochs=1, verbose=0)
                    self.model.fit(new_state, np.array(post_action_value), epochs=1, verbose=0)

                if i % 1000 == 1:
                    save_poker_model(self.model, i)


def norm_reward(reward):
    # reward is between -10 and 10, old value is between -1 and 1 iirc
    if reward > 0:
        # reward = reward / 10 + 0.5
        reward = reward / 10
    elif reward < 0:
        # reward = 0.5 + reward / 10
        reward = reward / 10
    else:
        reward = 0
    return reward


if __name__ == "__main__":
    neural_network = NeuralNetworkTrainer(4)
    neural_network.train_agent()
