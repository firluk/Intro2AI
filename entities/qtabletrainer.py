import time
from random import random

import numpy as np
from prettytable import PrettyTable

from entities import Hand
from entities.qtablenpc import QtableNPC
from gym_poker.envs.poker_env import PokerEnv, Card


def calc_new_value(alpha, old_value, reward, gamma, next_max, done):
    if not done:
        return (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
    else:
        return ((1 - alpha) * old_value) + (alpha * reward)


class QTableTrainer:
    """ Q-table base agent for simple poker

        Observation Space includes:
        Card1, Card2, BB/SB, Chips Amount [0 -- n/2 -- n -- 1.5n -- 2n]
          52 ,   52 ,   2  ,     4
        """

    def __init__(self, num_of_chips):

        self.agent = QtableNPC(bluff=True)
        self.nc = num_of_chips

    def train_agent(self, ca=52):
        alpha = 0.5
        epsilon = 0.5
        lbda = 0.1
        tmr1 = time.time()
        tmr2 = 0

        # region Controlled Cards
        """
        env = PokerEnv(self.nc, 0, False, 0.8)
        cycles = 800  # int(52 * 52 * np.math.log(52 * 52) * 1000)
        for f1 in range(ca):
            for f2 in range(f1 + 1, ca):
                if f1 > f2:
                    continue
                now = 0
                for i in range(cycles):
                    done = False
                    while not done:
                        _deck = env.gm.deck
                        player1 = env.ob[0]
                        player2 = env.ob[1]
                        # generated cards
                        gc1, gc2 = Card.decode(f1), Card.decode(f2)
                        # remove generated cards from the deck
                        _deck.remove_card(f1)
                        _deck.remove_card(f2)
                        # pull random cards from deck
                        rc1, rc2 = _deck.draw_card(), _deck.draw_card()
                        # we are taking turns who has random cards and who has generated cards
                        if i % 2 == 0:
                            # generate player 2
                            player2.take_card(gc1)
                            player2.take_card(gc2)
                            action2 = 1
                            p2_state = PokerEnv.encode(player2.hand, 1, player2.bank, self.nc)
                            # give random cards from deck
                            player1.take_card(rc1)
                            player1.take_card(rc2)
                            p1_state = PokerEnv.encode(player1.hand, 0, player1.bank, self.nc)
                            action1 = 1
                        else:
                            # generate player 1
                            player1.take_card(gc1)
                            player1.take_card(gc2)
                            p1_state = PokerEnv.encode(player1.hand, 0, player1.bank, self.nc)
                            action1 = 1
                            player2.take_card(rc1)
                            player2.take_card(rc2)
                            p2_state = PokerEnv.encode(player2.hand, 1, player2.bank, self.nc)
                            action2 = 1

                        # Make a step in the environment
                        observation, rewards, done = env.step([action1, action2])
                        p1_reward, p2_reward = rewards[0], rewards[1]
                        # count victories of generated cards for statistics
                        if i % 2 == 0:
                            if ((p2_reward == env.win_rew) | (p2_reward == env.tot_win_rew)) & (
                                    (p1_reward == env.fld_pen) | (p1_reward == env.los_pen) | (
                                    p1_reward == env.tot_los_pen)):
                                now += 1
                        else:
                            if ((p1_reward == env.win_rew) | (p1_reward == env.tot_win_rew)) & (
                                    (p2_reward == env.los_pen) | (p2_reward == env.tot_los_pen) | (
                                    p2_reward == env.fld_pen)):
                                now += 1
                        # reward/punish the players
                        old_value = self.agent.qt[p1_state][action1]
                        new_value = ((1 - alpha) * old_value) + (alpha * p1_reward)
                        self.agent.qt[p1_state][action1] = new_value
                        # make sure small blind didn't fold before awarding reward
                        if action1 != 0:
                            old_value = self.agent.qt[p2_state][action2]
                            new_value = ((1 - alpha) * old_value) + (alpha * p2_reward)
                            self.agent.qt[p2_state][action2] = new_value
                    env.reset(self.nc)

                # after the hand has finished running write the data to disk
                np.savez('Qtable/qtablenpc.npz', qtable=self.agent.qt)
                # print hand and w/l statistics
                player1.hand.add_card(Card.decode(f1))
                player1.hand.add_card(Card.decode(f2))
                print(player1.hand.__str__(), " w/l = {0:2.4f}".format(now / (2 * cycles)))
                player1.hand.clear_hand()
                # calculate and display estimated time of run
                if tmr2 != 0:
                    cycles_left = ((52 - f1) * 52) + (52 - f2)
                    tmr1 = time.time()
                    seconds_for_one_cycle = tmr1 - tmr2
                    seconds_left = int(cycles_left * seconds_for_one_cycle)
                    minutes_left = int(seconds_left // 60)
                    seconds_left = int(seconds_left % 60)
                    print("Estimated time to completion: {0:d}:{1:02d}".format(minutes_left, seconds_left))
                tmr2 = tmr1
            if f1 % 13 == 0:
                print_q_table_to_file(self.nc, table=self.agent.qt, verbose=False,filename=".\Qtable\Q_table_dump" + str(f1) + ".txt")
        """
        # endregion

        # region Full exploration
        """
        env = PokerEnv(self.nc, 0, True, 0.8)
        cycles = 20000  # int(52 * 52 * np.math.log(52 * 52) * 1000)
        pulse = cycles // 20
        for i in range(cycles):
            done = False
            while not done:
                player1 = env.ob[0]
                player2 = env.ob[1]
                p1_state = PokerEnv.encode(player1.hand, 0, player1.bank, self.nc)
                p2_state = PokerEnv.encode(player2.hand, 1, player2.bank, self.nc)
                action1 = 0 if random() > 0.5 else 1
                action2 = 0 if random() > 0.5 else 1
                observation, rewards, done = env.step([action1, action2])

                p1_reward, p2_reward = rewards[0], rewards[1]
                old_value = self.agent.qt[p1_state][action1]
                new_value = ((1 - alpha) * old_value) + (alpha * p1_reward)
                self.agent.qt[p1_state][action1] = new_value
                # if player 1 folded, nothing to learn here
                if action1 != 0:
                    old_value = self.agent.qt[p2_state][action2]
                    new_value = ((1 - alpha) * old_value) + (alpha * p2_reward)
                    self.agent.qt[p2_state][action2] = new_value
            if i % pulse == 0:
                np.savez('Qtable/qtablenpc.npz', qtable=self.agent.qt)
                if tmr2 != 0:
                    pulses_left = (cycles - i) // pulse
                    tmr1 = time.time()
                    seconds_for_one_pulse = tmr1 - tmr2
                    seconds_left = int(pulses_left * seconds_for_one_pulse)
                    minutes_left = int(seconds_left // 60)
                    seconds_left = int(seconds_left % 60)
                    print("Estimated time to completion: {0:d}:{1:02d}".format(minutes_left, seconds_left))
                tmr2 = tmr1
                if i % (pulse * 10) == 0:
                    print_q_table_to_file(self.nc, table=self.agent.qt, verbose=False,
                                          filename=".\Qtable\Q_table_dump" + str(i) + ".txt")
            env.reset(self.nc)
        """
        # endregion

        # region Against Random
        """
        env = PokerEnv(self.nc, 0, True, 1)
        cycles = 600000  # int(52 * 52 * np.math.log(52 * 52) * 1000)
        pulse = cycles // 20
        for i in range(cycles):
            done = False
            while not done:
                player1 = env.ob[0]
                player2 = env.ob[1]
                p1_state = PokerEnv.encode(player1.hand, 0, player1.bank, self.nc)
                p2_state = PokerEnv.encode(player2.hand, 1, player2.bank, self.nc)

                if i % 2 == 0:
                    action1 = self.agent.make_a_move(PokerEnv.encode(player1.hand, 0, player1.bank, self.nc))
                    action2 = 0 if random() > 0.5 else 1
                else:
                    action1 = 0 if random() > 0.5 else 1
                    action2 = self.agent.make_a_move(PokerEnv.encode(player2.hand, 1, player2.bank, self.nc))

                observation, rewards, done = env.step([action1, action2])

                p1_reward, p2_reward = rewards[0], rewards[1]
                old_value = self.agent.qt[p1_state][action1]
                new_value = (1 - alpha) * old_value + alpha * p1_reward
                self.agent.qt[p1_state][action1] = new_value
                # if player 1 folded, nothing to learn here
                if action1 != 0:
                    old_value = self.agent.qt[p2_state][action2]
                    new_value = (1 - alpha) * old_value + alpha * p2_reward
                    self.agent.qt[p2_state][action2] = new_value
            if i % pulse == 0:
                np.savez('Qtable/qtablenpc.npz', qtable=self.agent.qt)
                if tmr2 != 0:
                    pulses_left = (cycles - i) // pulse
                    tmr1 = time.time()
                    seconds_for_one_pulse = tmr1 - tmr2
                    seconds_left = int(pulses_left * seconds_for_one_pulse)
                    minutes_left = int(seconds_left // 60)
                    seconds_left = int(seconds_left % 60)
                    print("Estimated time to completion: {0:d}:{1:02d}".format(minutes_left, seconds_left))
                tmr2 = tmr1
                if i % (pulse * 10) == 0:
                    print_q_table_to_file(self.nc, table=self.agent.qt, verbose=False,
                                          filename=".\Qtable\Q_table_dump" + str(i) + ".txt")
            env.reset(self.nc)
        """
        # endregion

        # region Some exploration
        """
        env = PokerEnv(self.nc, 0, True, 0.4)
        cycles = 20000  # int(52 * 52 * np.math.log(52 * 52) * 1000)
        pulse = cycles // 20
        for i in range(cycles):
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
                    action1 = self.agent.make_a_move(p1_state)
                if random() < epsilon:
                    action2 = 0 if random() > 0.5 else 1
                else:
                    action2 = self.agent.make_a_move(p2_state)

                observation, rewards, done = env.step([action1, action2])
                p1_reward, p2_reward = rewards[0], rewards[1]
                old_value = self.agent.qt[p1_state][action1]
                new_value = ((1 - alpha) * old_value) + (alpha * p1_reward)
                self.agent.qt[p1_state][action1] = new_value
                # if player 1 folded, nothing to learn here
                if action1 != 0:
                    old_value = self.agent.qt[p2_state][action2]
                    new_value = ((1 - alpha) * old_value) + (alpha * p2_reward)
                    self.agent.qt[p2_state][action2] = new_value
            if i % pulse == 0:
                np.savez('Qtable/qtablenpc.npz', qtable=self.agent.qt)
                cycles_left = cycles - i
                if tmr2 != 0:
                    tmr1 = time.time()
                    seconds_for_one_pulse = tmr1 - tmr2
                    seconds_left = int((cycles_left // pulse) * seconds_for_one_pulse)
                    minutes_left = int(seconds_left // 60)
                    seconds_left = int(seconds_left % 60)
                    print("Estimated time to completion: {0:d}:{1:02d}".format(minutes_left, seconds_left))
                tmr2 = tmr1
                print_q_table_to_file(self.nc, table=self.agent.qt, verbose=False,
                                      filename=".\Qtable\Q_table_dump" + str(i + 1) + ".txt")
            env.reset(self.nc)
        """
        # endregion

        # region No exploration
        """
        env = PokerEnv(self.nc, 0)
        cycles = 300000  # int(52 * 52 * np.math.log(52 * 52) * 1000)
        pulse = cycles // 20
        tmr1 = time.time()
        for i in range(cycles):
            done = False
            while not done:
                player1 = env.ob[0]
                player2 = env.ob[1]
                p1_state = PokerEnv.encode(player1.hand, 0, player1.bank, self.nc)
                p2_state = PokerEnv.encode(player2.hand, 1, player2.bank, self.nc)
                action1 = self.agent.make_a_move(PokerEnv.encode(player1.hand, 0, player1.bank, self.nc))
                action2 = self.agent.make_a_move(PokerEnv.encode(player2.hand, 1, player2.bank, self.nc))
                observation, rewards, done = env.step([action1, action2])
                p1_reward, p2_reward = rewards[0], rewards[1]
                old_value = self.agent.qt[p1_state][action1]
                new_value = (1 - alpha) * old_value + alpha * p1_reward
                self.agent.qt[p1_state][action1] = new_value
                # if player 1 folded, nothing to learn here
                if action1 != 0:
                    old_value = self.agent.qt[p2_state][action2]
                    new_value = (1 - alpha) * old_value + alpha * p2_reward
                    self.agent.qt[p2_state][action2] = new_value
            if i % pulse == 0:
                np.savez('Qtable/qtablenpc.npz', qtable=self.agent.qt)
                if tmr2 != 0:
                    pulses_left = (cycles - i) // pulse
                    tmr1 = time.time()
                    seconds_for_one_pulse = tmr1 - tmr2
                    seconds_left = int(pulses_left * seconds_for_one_pulse)
                    minutes_left = int(seconds_left // 60)
                    seconds_left = int(seconds_left % 60)
                    print("Estimated time to completion: {0:d}:{1:02d}".format(minutes_left, seconds_left))
                tmr2 = tmr1
                if i % (pulse * 10) == 0:
                    print_q_table_to_file(self.nc, table=self.agent.qt, verbose=False,
                                          filename=".\Qtable\Q_table_dump" + str(i) + ".txt")
            env.reset(self.nc)
        """
        # endregion

        # region Exploration vs exploitation

        env = PokerEnv(self.nc, 0)
        cycles = 300000  # int(52 * 52 * np.math.log(52 * 52) * 1000)
        pulse = cycles // 20
        tmr1 = time.time()
        for i in range(cycles):
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
                    action1 = self.agent.make_a_move(p1_state)
                if random() < epsilon:
                    action2 = 0 if random() > 0.5 else 1
                else:
                    action2 = self.agent.make_a_move(p2_state)

                observation, rewards, done = env.step([action1, action2])
                p1_reward, p2_reward = rewards[0], rewards[1]
                old_value = self.agent.qt[p1_state][action1]
                n_state = PokerEnv.encode(player1.hand, 1, player1.bank, self.nc)
                n_max = np.max(self.agent.qt[n_state])
                new_value = calc_new_value(alpha, old_value, p1_reward, lbda, n_max, done)
                self.agent.qt[p1_state][action1] = new_value
                # if player 1 folded, nothing to learn here
                if action1 != 0:
                    old_value = self.agent.qt[p2_state][action2]
                    n_state = self.agent.make_a_move(PokerEnv.encode(player2.hand, 0, player2.bank, self.nc))
                    n_max = np.max(self.agent.qt[n_state])
                    new_value = calc_new_value(alpha, old_value, p2_reward, lbda, n_max, done)
                    self.agent.qt[p2_state][action2] = new_value
            if i % pulse == 0:
                np.savez('Qtable/qtablenpc.npz', qtable=self.agent.qt)
                cycles_left = cycles - i
                if tmr2 != 0:
                    tmr1 = time.time()
                    seconds_for_one_pulse = tmr1 - tmr2
                    seconds_left = int((cycles_left // pulse) * seconds_for_one_pulse)
                    minutes_left = int(seconds_left // 60)
                    seconds_left = int(seconds_left % 60)
                    print("Estimated time to completion: {0:d}:{1:02d}".format(minutes_left, seconds_left))
                tmr2 = tmr1
                if i % (pulse * 6) == 0:
                    print_q_table_to_file(self.nc, table=self.agent.qt, verbose=False,
                                          filename=".\Qtable\Q_table_dump" + str(i + 1) + ".txt")
            env.reset(self.nc)

        # endregion

        print_q_table_to_file(self.nc, table=self.agent.qt, verbose=False, filename=".\Qtable\Q_table_dump_end.txt")
        np.savez('Qtable/qtablenpc.npz', qtable=self.agent.qt)


def print_q_table_to_file(starting_num_of_chips, table=None, verbose=False, filename=".\Qtable\q_table_dump.txt", ):
    t = PrettyTable(['Cards',
                     'FoldSB0', 'CallSB0', 'ActionSB0',
                     'FoldSB1', 'CallSB1', 'ActionSB1',
                     'FoldSB2', 'CallSB2', 'ActionSB2',
                     'FoldSB3', 'CallSB3', 'ActionSB3',
                     'FoldBB0', 'CallBB0', 'ActionBB0',
                     'FoldBB1', 'CallBB1', 'ActionBB1',
                     'FoldBB2', 'CallBB2', 'ActionBB2',
                     'FoldBB3', 'CallBB3', 'ActionBB3'])
    _c = False
    if table is None:
        try:
            # Load Qtable from file
            with np.load('Qtable/qtablenpc.npz') as data:
                _qt = data['qtable']
        except IOError:
            print("error loading qtable")
            return
    else:
        _qt = table
    _h = Hand()
    _res = np.zeros(8, dtype=int)
    for i in range(52):

        for j in range(i + 1, 52):
            _h.add_card(Card.decode(i))
            _h.add_card(Card.decode(j))
            for i1 in range(2):
                for j1 in range(4):
                    _res[i1 * 4 + j1] = PokerEnv.encode(_h, i1, 1 + (j1 * (starting_num_of_chips / 2)),
                                                        starting_num_of_chips)
            _s = _h.__str__() + " - "
            t.add_row([
                _s,
                round(_qt[_res[0]][0], 2), round(_qt[_res[0]][1], 2),
                "call" if _qt[_res[0]][1] > _qt[_res[0]][0] else "fold",
                round(_qt[_res[1]][0], 2), round(_qt[_res[1]][1], 2),
                "call" if _qt[_res[1]][1] > _qt[_res[1]][0] else "fold",
                round(_qt[_res[2]][0], 2), round(_qt[_res[2]][1], 2),
                "call" if _qt[_res[2]][1] > _qt[_res[2]][0] else "fold",
                round(_qt[_res[3]][0], 2), round(_qt[_res[3]][1], 2),
                "call" if _qt[_res[3]][1] > _qt[_res[3]][0] else "fold",
                round(_qt[_res[4]][0], 2), round(_qt[_res[4]][1], 2),
                "call" if _qt[_res[4]][1] > _qt[_res[4]][0] else "fold",
                round(_qt[_res[5]][0], 2), round(_qt[_res[5]][1], 2),
                "call" if _qt[_res[5]][1] > _qt[_res[5]][0] else "fold",
                round(_qt[_res[6]][0], 2), round(_qt[_res[6]][1], 2),
                "call" if _qt[_res[6]][1] > _qt[_res[6]][0] else "fold",
                round(_qt[_res[7]][0], 2), round(_qt[_res[7]][1], 2),
                "call" if _qt[_res[7]][1] > _qt[_res[7]][0] else "fold"
            ])

            _h.clear_hand()
    if verbose:
        print(t)
    if filename:
        with open(filename, 'w', encoding='utf8') as outfile:
            outfile.write(str(t))
