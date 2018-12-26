from entities.card import Card
from entities.hand import Hand


class QtableNPC:
    """ Q-table base agent for simple poker

    Observation Space includes:
    Card1, Card2, BB/SB, Chips Amount [0 -- n/2 -- n -- 1.5n -- 2n]
      52 ,   52 ,   2  ,     4
    """

    def __init__(self):
        n_s = 52 * 52 * 2 * 4
        n_a = 2
        # This will initialize the starting Q-Table to incentify the agent to always go all in
        # The table stores only rewards, nothing more
        self.qt = {s: {a: -1 if a == 0 else 1 for a in range(n_a)} for s in range(n_s)}
        self.state = 0

    @staticmethod
    def encode(hand, small_blind, _num_of_chips, initial_num_of_chips):
        """Encoding and decoding code was lifted from openAI taxi gym"""
        # Sort hand and extract cards
        _sorted_hand = sorted(hand.cards, reverse=True)
        _card1 = _sorted_hand[0].encode()
        _card2 = _sorted_hand[1].encode()
        # Calculate coefficient of number of chips
        _coef_chips = 2 * _num_of_chips // initial_num_of_chips
        # Encode
        encoded = _card2
        encoded *= 52
        encoded += _card1
        encoded *= 2
        encoded += small_blind
        encoded *= 4
        encoded += _coef_chips
        return encoded

    @staticmethod
    def decode(_code):
        """Encoding and decoding code was lifted from openAI taxi gym"""
        _out = [_code % 4]
        _code = _code // 4
        _out.append(_code % 2)
        _code = _code // 2
        _card1 = Card.decode(_code % 52)
        _code = _code // 52
        _card2 = Card.decode(_code)
        assert 0 <= _code < 52
        _hand = Hand()
        _hand.add_card(_card1)
        _hand.add_card(_card2)
        _out.append(_hand)
        return _out
