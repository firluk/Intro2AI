from random import randint
from random import random

import gym

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
        neutral_grade = 0
        sb_chips = 1
        bb_chips = 2
        bankrupt_qualifier = 1.1

        sb_player: Player = self._g.sb_player()
        bb_player: Player = self._g.bb_player()
        info = {}
        # consideration : award and punish win/loss by fixed value not by money value
        # 1 / -1 sb in bb fold
        # -1 / 0 sb fold bb irrelevant
        # pot is awarded as a reward to winner
        # -pot as a punishment for loser
        ######################################
        # mdp continuation:
        # 1)sb and bb 2 cards each
        # -action->
        # 2)a) 7 vs 7 in which case, due to simplicity of the game, we assume the call as only option
        #   b) fold happened somewhere in between
        ######################################
        # case when 7 cards on players hands for hand resolution
        # assumption that both players called and 5 of the cards are mutual to both hands
        # but in 7 cards situation the decision was either taken and we have only 1 action - resolve
        # we neglect the game flow and the bank operations as we view episode over if new cards are drawn
        ######################################

        if (len(sb_player.hand.cards) == 7) and (len(sb_player.hand.cards) == 7):
            pot = self._g.pot
            results = []
            for ep in [sb_player, bb_player]:
                ep.hand.sort()
                results.append(Game.score(ep.hand))
            # select the winner
            winners = Game.determine_winner(results)
            if winners.__len__() > 1:
                # split the pot
                self._g.split_the_pot()
                # Give both players small reward
                # rewards = [0, 0]
                rewards = [neutral_grade, neutral_grade]
            else:
                # Actually transfer the chips between players
                self._g.player_won(self._g.p[winners[0]])
                rewards = []
                # Reward the winner with chips won

                if sb_player.bank == 0:
                    rewards = [-bankrupt_qualifier * pot, bankrupt_qualifier * pot]
                elif bb_player.bank == 0:
                    rewards = [bankrupt_qualifier * pot, -bankrupt_qualifier * pot]
                else:
                    gain = min(pot, self._g.p[winners[0]].bet * 2)
                    rewards.insert(winners[0], gain)
                    rewards.insert(1 - winners[0], -gain)
            done = True
            next_state = None
        # due to simplicity of our game model immediate alternative is having 2 cards in the hand
        elif (len(sb_player.hand.cards) == 2) and (len(bb_player.hand.cards) == 2):
            # here we want to transition to 7 card case if both call
            # otherwise resolve immediately by awarding 1 and -1 correspondingly
            if action[0]:
                # SB called
                self._g.player_all_in(sb_player)
                if action[1]:
                    # BB called
                    self._g.player_call(bb_player, sb_player.bet)
                    # Need to compare hands
                    for c in range(5):
                        # give same card to both hands
                        new_card = self._g.deck.draw_card()
                        for ep in self._g.p:
                            ep.hand.add_card(new_card)
                    # immediate reward - 0 for both
                    done = False
                    rewards = [neutral_grade, neutral_grade]
                    next_state = [sb_player, bb_player]
                else:
                    # BB fold - episode over
                    done = True
                    # rewards = [0, 0]
                    rewards = [bb_chips, -bb_chips]
                    next_state = None
            else:
                # SB fold - episode over
                done = True
                # rewards = [0, 0]
                rewards = [-sb_chips, neutral_grade]
                next_state = None
        else:
            raise ValueError(
                'Illegal state in the training enviroment P1 {} P2 {}'.format(sb_player.hand, bb_player.hand))
        return next_state, rewards, done, info

    def reset(self, bank=4, rand_bank_dist=False):
        """Initial setup for training

        :param bank : initial bank size
        :param rand_bank_dist: boolean field indicating used for covering unbalanced setups for money distribution
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
        # randomly distribute the bank between players - emulate random bank situation in game
        if rand_bank_dist and random() < 0.2:
            self._g.p[0].bank = randint(2, bank * 2 - 2)
            self._g.p[1].bank = bank * 2 - self._g.p[0].bank
        # prepare the game
        self._g.place_blinds()
        self._g.players_draw_cards()
        # Return observation
        # [ Small Blind Player, Big Blind Player ]
        self.ob = [self._g.sb_player(), self._g.bb_player()]
        return self.ob

    def render(self, mode='human'):
        self._g.render_game()
