import random
import time

import numpy as np

from entities.card import Card
from entities.hand import Hand
from entities.qtabletrainer import QTableTrainer
from gym_poker.envs.poker_env import PokerEnv


def generate_tp(val=15, val2=15, val3=15):
    """Generate two pairs 5 cards hand"""
    suits = ["Spade", "Club", "Diamond", "Heart"]
    h = Hand()
    # First Pair
    choice = random.choice(suits)
    choice2 = random.choice(suits)
    while choice == choice2:
        choice2 = random.choice(suits)
    if val == 15:
        val = random.choice(range(2, 15))
    for su in suits:
        if not (su.__eq__(choice) or su.__eq__(choice2)):
            h.add_card(Card(su, val))
    # Second Pair
    choice = random.choice(suits)
    choice2 = random.choice(suits)
    while choice == choice2:
        choice2 = random.choice(suits)
    while val2 == 15 or val2 == val:
        val2 = random.choice(range(2, 15))
    for su in suits:
        if not (su.__eq__(choice) or su.__eq__(choice2)):
            h.add_card(Card(su, val2))
    # Last Card
    while val3 == 15 or val3 == val or val3 == val2:
        val3 = random.choice(range(2, 15))
    h.add_card(Card(random.choice(suits), val3))
    return h


def generate_tok(val=15, val2=15, val3=15):
    """Generate three of a kind 5 cards hand"""
    suits = ["Spade", "Club", "Diamond", "Heart"]
    choice = random.choice(suits)
    if val == 15:
        val = random.choice(range(2, 15))
    h = Hand()
    for su in suits:
        if not su.__eq__(choice):
            h.add_card(Card(su, val))
    while val2 == 15 or val2 == val:
        val2 = random.choice(range(2, 15))
    h.add_card(Card(random.choice(suits), val2))
    while val3 == 15 or val3 == val or val3 == val2:
        val3 = random.choice(range(2, 15))
    h.add_card(Card(random.choice(suits), val3))
    return h


def generate_fh(val=15, val2=15):
    """Generate Full house 5 cards hand"""
    suits = ["Spade", "Club", "Diamond", "Heart"]
    choice = random.choice(suits)
    if val == 15:
        val = random.choice(range(2, 15))
    h = Hand()
    for su in suits:
        if not su.__eq__(choice):
            h.add_card(Card(su, val))
    choice, choice2 = random.choice(suits), random.choice(suits)
    while choice2 == choice:
        choice2 = random.choice(suits)
    while val2 == 15 or val2 == val:
        val2 = random.choice(range(2, 15))
    for su in suits:
        if not (su.__eq__(choice) or su.__eq__(choice2)):
            h.add_card(Card(su, val2))
    return h


def train_agent(crds, chips):
    trainer = QTableTrainer(chips)
    trainer.train_agent(crds)


def print_qt(num, ch):
    _c = False
    _qt = None
    try:
        # Load Qtable from file
        with np.load('Qtable/qtablenpc.npz') as data:
            _qt = data['qtable']
        _c = True
    except IOError:
        print("error loading qtable")
    if not _c:
        exit(0)
    _h = Hand()
    _res = np.zeros(8, dtype=int)
    for i in range(num):
        print("Cards  --  big blind  --  money ranges  --  small blind  -- money ranges")
        for j in range(i + 1, num):
            _h.add_card(Card.decode(i))
            _h.add_card(Card.decode(j))
            for i1 in range(2):
                for j1 in range(4):
                    _res[i1 * 4 + j1] = PokerEnv.encode(_h, i1, 1 + (j1 * (ch / 2)), ch)
            _s = _h.__str__() + " - "
            for i2 in range(8):
                _s += str.format('{:.2f}', _qt[_res[i2]][0])
                _s += "|"
                _s += str.format('{:.2f}', _qt[_res[i2]][1])
                _s += " -- "
            print(_s)
            _h.clear_hand()


if __name__ == "__main__":
    strt = time.time()
    cards = 52
    starting_chips = 20
    penalty = 25
    train_agent(cards, starting_chips)
    print_qt(cards, starting_chips)
    elapsed = int(time.time() - strt)
    print("Time elapsed: {0:d}:{1:02d}".format(elapsed // 60, elapsed % 60))
