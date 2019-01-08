from random import random

import gym
import numpy as np

from entities import *


class NeuralNetPokerEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, num_of_chips):
        self._g = None
        self.ob = self.reset(num_of_chips)

    def step(self, action):
        """Step

        returns ob, rewards, episode_over, info : tuple

        ob (list[Player,Player]) : next stage observation
            [player who is small blind,player who is big blind].
        rewards ([float,float]) :
            amount of reward achieved by the previous action
        :param action: [small blind action, big blind action]
                0 if fold, 1 otherwise
         """
        sb_player = self._g.sb_player()
        bb_player = self._g.bb_player()
        if action[0]:
            # Small blind went all in
            self._g.player_all_in(sb_player)
            if action[1]:
                # BB called
                self._g.player_call(bb_player, sb_player.bet)
                # Need to compare hands
                for c in range(5):
                    new_card = self._g.deck.draw_card()
                    for ep in self._g.p:
                        ep.hand.add_card(new_card)
                for pl in self._g.p:
                    pl.hand.sort()
                # get the absolute score of the hand and the best five cards
                results = []
                for ep in [sb_player, bb_player]:
                    results.append(Game.score(ep.hand))
                # select the winner
                winners = Game.determine_winner(results)
                # award the pot to the winner
                if winners.__len__() > 1:
                    # split the pot
                    self._g.split_the_pot()
                    # Give both players small reward
                    rewards = [1, 1]
                else:
                    # Actually transfer the chips between players
                    self._g.player_won(self._g.p[winners[0]])
                    rewards = []
                    # Reward the winner with chips won
                    rewards.insert(winners[0], self._g.p[winners[0]].bank)
                    # Penalty the loser with chips lost
                    rewards.insert(1 - winners[0], self._g.p[1 - winners[0]].bank)

            else:
                # BB folded
                # Reward SB with amount won
                # Transfer chips to SB
                sb_player.bank += self._g.pot
                # Penalty BB by amount lost
                rewards = [sb_player.bank, bb_player.bank]
        else:
            # Small blind folded
            # Reward BB with 0 since their move didn't matter
            # Penalty SB by amount lost
            rewards = [sb_player.bank, 0]
            # Transfer chips to BB
            bb_player.bank += self._g.pot
        # Change who is SB
        self._g.sb = 1 - self._g.sb
        self._g.new_step()
        self._g.place_blinds()
        self._g.players_draw_cards()
        if self._g.a_player().bank <= 0 or self._g.na_player().bank <= 0:
            self._g.done = True
        self.ob = [sb_player, bb_player]
        return self.ob, rewards, self._g.done, None

    def reset(self, bank=50):
        """Initial setup for training

        :param model: model for the neural net player
        :param bank : initial bank size
        :returns [small blind player, big blind player]
        """
        # randomly pick neural and random
        if random() > 0.5:
            self._g = Game("NeuralNet", "NeuralNet", "Random", "Random", bank)
            self._g.p[0].type = "n"
            self._g.p[1].type = "r"
        else:
            self._g = Game("Random", "Random", "NeuralNet", "NeuralNet", bank)
            self._g.p[0].type = "r"
            self._g.p[1].type = "n"
        self._g.place_blinds()
        self._g.players_draw_cards()
        # Return observation
        # [ Small Blind Player, Big Blind Player ]
        self.ob = [self._g.sb_player(), self._g.bb_player()]
        return self.ob

    def render(self, mode='human'):
        self._g.render_game()

    @staticmethod
    def encode(hand, small_blind, _num_of_chips, initial_num_of_chips):
        """Encoding and decoding code was lifted from openAI taxi gym"""
        # encode vector of input value
        encoded_input_vector = np.zeros([1, 58])  # 52 for cards 2 for small or big blind 4 for money bins
        for card in hand.cards:
            encoded_input_vector[0, Card.encode(card)] = 1
        if small_blind:
            encoded_input_vector[0, 52 + 1] = 1
        else:
            encoded_input_vector[0, 52 + 2] = 1
        money_bin = 2 * _num_of_chips // initial_num_of_chips
        encoded_input_vector[0, 52 + 2 + money_bin] = 1

        return encoded_input_vector
