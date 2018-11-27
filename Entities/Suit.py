class Suit:
    name: None
    icon: None


def pull_suit():
    _suits = ["Spade", "Club", "Diamond", "Heart"]
    for i in range(4):
        yield _suits[i]


def get_icon(suit):
    suits = {"Spade": "♠", "Club": "♣", "Diamond": "♦", "Heart": "♥"}
    return suits[suit]
