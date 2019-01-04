import random

from entities.card import Card
from entities.hand import Hand
from entities.qtabletrainer import QTableTrainer


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


if __name__ == "__main__":
    qt = QTableTrainer(10)
    qt.train_agent()
