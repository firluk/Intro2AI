from random import random

from keras.layers import np

from entities.neuralnetworknpc import NeuralNetworkNPC, save_poker_model, encode_to_vector
from gym_poker.envs.neural_net_poker_env import NeuralNetPokerEnv


class NeuralNetworkTrainer:
    """ Trainer for neural network based agent for toy poker """
    def __init__(self, num_of_chips=20):

        npc = NeuralNetworkNPC()
        self.model = npc.model
        self.nc = num_of_chips

    """ Training of the neural network for toy poker """
    def train_agent(self, enforce_play=False, save_every=100000, total_episodes=100000):

        env = NeuralNetPokerEnv(self.nc)
        neural_npc = NeuralNetworkNPC()

        # exploration vs exploitation
        eps = 0.5
        # future reward factor
        gamma = 0.5

        all_rewards = [0, 0]

        for i in range(1, total_episodes + 1):
            s = env.reset(self.nc, rand_bank_dist=True)

            # saving the model for keras and saving q-table like results in readable format
            if save_every and (i % save_every == 0 or i == 1):
                print("Episode {} of {}".format(i, total_episodes))
                save_poker_model(self.model, all_rewards)

            # episode flags
            done = False
            post_river = False

            # iterations over single episode
            while not done:

                # getting player objects from state, either after reset of environment or next step
                player1 = s[0]
                player2 = s[1]

                # separating the player hand to hole and community cards
                # hole cards - player's unique cards
                # community cards - mutual cards for players
                hole_cards1 = player1.hand.cards[0:2]
                hole_cards2 = player2.hand.cards[0:2]
                community_cards = player1.hand.cards[2:]

                # state encoding to consumable format for neural network
                state1, _ = encode_to_vector(hole_cards1, community_cards, 0, player1.bank, self.nc)
                state2, _ = encode_to_vector(hole_cards2, community_cards, 0, player2.bank, self.nc)

                # choosing the action via epsilon exploration vs exploitation
                a1 = self.epsilon_choice_action(eps, neural_npc, player1, post_river)
                a2 = self.epsilon_choice_action(eps, neural_npc, player2, post_river)

                # checking whether the state action is to be enforced
                if enforce_play or post_river:
                    a1, a2 = 1, 1

                # moving to next in accordance to action and states
                new_s, r, done, _ = env.step([a1, a2])

                # reward for both players
                reward1 = r[0]
                reward2 = r[1]
                all_rewards[0] += reward1 + reward2
                all_rewards[1] += 2

                # predicted future reward
                next_reward1 = np.zeros((2,))
                next_reward2 = np.zeros((2,))
                if new_s:
                    # separating the player hand to hole and community cards
                    # hole cards - player's unique cards
                    # community cards - mutual cards for players
                    hole_cards1 = new_s[0].hand.cards[0:2]
                    hole_cards2 = new_s[1].hand.cards[0:2]
                    community_cards = player1.hand.cards[2:]
                    # encoding and predicting future reward
                    next_state1, _ = encode_to_vector(hole_cards1, community_cards, 0, player1.bank, self.nc)
                    next_state2, _ = encode_to_vector(hole_cards2, community_cards, 0, player2.bank, self.nc)
                    next_reward1[1] = self.model.predict(next_state1)[0, 1]
                    next_reward2[1] = self.model.predict(next_state2)[0, 1]

                # deep-q learning combining immediate and future reward
                target1 = reward1 + gamma * next_reward1[a1]
                target2 = reward2 + gamma * next_reward2[a2]
                # in case of future reward - only call is relevant
                target_vec1 = np.zeros((1, 2,))
                target_vec2 = np.zeros((1, 2,))

                target_vec1[0, a1] = target1
                target_vec2[0, a2] = target2

                # fitting the model to combined reward
                self.model.fit(state1, target_vec1, epochs=1, verbose=0)
                if a1:
                    # takes place only if SB called
                    self.model.fit(state2, target_vec2, epochs=1, verbose=0)

                # advancing to next step
                s = new_s

    """ Action choice based on epsilon and neural network model """

    def epsilon_choice_action(self, eps, neural_npc, player, post_river):
        if post_river:
            return 1
        if np.random.random() < eps:
            a = 0 if random() > 0.5 else 1
        else:
            # encode state to vector
            hole_cards = player.hand.cards[0:2]
            community_cards = player.hand.cards[2:]
            state, _ = encode_to_vector(hole_cards, community_cards, 0, player.bank, self.nc)
            a = neural_npc.make_a_move(state)
        return a
