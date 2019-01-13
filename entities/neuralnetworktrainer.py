from random import random

from keras.layers import np

from entities.neuralnetworknpc import NeuralNetworkNPC, save_poker_model, encode_to_vector
from gym_poker.envs.neural_net_poker_env import NeuralNetPokerEnv


class NeuralNetworkTrainer:
    """ Neural network base agent for simple poker

        Observation Space includes:
        Card1, Card2, BB/SB, Chips Amount [0 -- n/2 -- n -- 1.5n -- 2n]
          52 ,   52 ,   2  ,     4
        """

    def __init__(self, num_of_chips=20):

        npc = NeuralNetworkNPC()
        self.model = npc.model
        self.nc = num_of_chips

    def train_agent(self, enforce_play=False, save_every=100000, total_episodes=100000):

        env = NeuralNetPokerEnv(self.nc)
        neural_npc = NeuralNetworkNPC()

        eps = 0.5
        gamma = 0.6

        for i in range(total_episodes):
            s = env.reset(self.nc, rand_bank_dist=True)

            if i % save_every == 0 and save_every:
                print("Episode {} of {}".format(i + 1, total_episodes))
                save_poker_model(self.model, i + 1)

            done = False
            post_river = False
            while not done:

                player1 = s[0]
                player2 = s[1]

                hole_cards1 = player1.hand.cards[0:2]
                hole_cards2 = player2.hand.cards[0:2]
                community_cards = player1.hand.cards[2:]

                state1, _ = encode_to_vector(hole_cards1, community_cards, 0, player1.bank, self.nc)
                state2, _ = encode_to_vector(hole_cards2, community_cards, 0, player2.bank, self.nc)

                a1 = self.neural_make_a_move(eps, neural_npc, player1, post_river)
                a2 = self.neural_make_a_move(eps, neural_npc, player2, post_river)

                if enforce_play or post_river:
                    a1, a2 = 1, 1

                new_s, r, done, _ = env.step([a1, a2])
                reward1 = r[0]
                reward2 = r[1]

                next_reward1 = np.zeros((2,))
                next_reward2 = np.zeros((2,))

                if new_s:
                    hole_cards1 = new_s[0].hand.cards[0:2]
                    hole_cards2 = new_s[1].hand.cards[0:2]
                    community_cards = player1.hand.cards[2:]

                    next_state1, _ = encode_to_vector(hole_cards1, community_cards, 0, player1.bank, self.nc)
                    next_state2, _ = encode_to_vector(hole_cards2, community_cards, 0, player2.bank, self.nc)

                    next_reward1[1] = self.model.predict(next_state1)[0, 1]
                    next_reward2[1] = self.model.predict(next_state2)[0, 1]

                target1 = reward1 + gamma * next_reward1[a1]
                target2 = reward2 + gamma * next_reward2[a2]

                target_vec1 = np.zeros((1, 2,))
                target_vec2 = np.zeros((1, 2,))

                target_vec1[0, a1] = target1
                target_vec2[0, a2] = target2

                self.model.fit(state1, target_vec1, epochs=1, verbose=0)
                if a1:
                    self.model.fit(state2, target_vec2, epochs=1, verbose=0)

                s = new_s

    def neural_make_a_move(self, eps, neural_npc, player, post_river):
        if post_river:
            return 1
        if np.random.random() < eps:
            a = 0 if random() > 0.5 else 1
        else:
            # encode_to_vector state to vector
            hole_cards = player.hand.cards[0:2]
            community_cards = player.hand.cards[2:]
            state, _ = encode_to_vector(hole_cards, community_cards, 0, player.bank, self.nc)
            a = neural_npc.make_a_move(state)
        return a
