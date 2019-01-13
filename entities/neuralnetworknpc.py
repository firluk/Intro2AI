from pprint import pprint

import numpy as np
from keras import Sequential
from keras.engine import InputLayer
from keras.layers import Dense
from keras.models import load_model, save_model

from entities import Hand, Card
from entities.deck import get_deck


class NeuralNetworkNPC:
    """ Q-table base agent for simple poker

    Observation Space includes:
    Card1, Card2, BB/SB, Chips Amount [0 -- n/2 -- n -- 1.5n -- 2n]
      52 ,   52 ,   2  ,     4
    """

    def __init__(self, model=None):
        """Constructs an agent for poker game

        :param model: Neural network Model (default none)
        """
        if model is None:
            try:
                # Load model
                self.model = load_poker_model()
            except OSError:
                self.model = create_empty_model()

        else:
            self.model = model

    def make_a_move(self, encoded_state, opp_state=None):
        """Makes a decision whenever to fold or play by forward feeding

        :param encoded_state: encoded representation of the state
        :return action 0 for fold 1 for play:
        """
        if opp_state is not None:
            my_prediction = self.model.predict(encoded_state)
            opp_prediction = self.model.predict(opp_state)
            if my_prediction[0, 1] > opp_prediction[0, 1]:
                return 1
            else:
                return 0
        return np.argmax(self.model.predict(encoded_state))


def create_empty_model():
    model = Sequential()
    model.add(InputLayer(input_shape=(106,)))
    model.add(Dense(53))
    model.add(Dense(2))
    model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    return model


def load_poker_model():
    return load_model('./NeuralNet/my_model.h5')


def save_poker_model(model, i="_end"):
    save_model(model, './NeuralNet/my_model' + str(i) + '.h5')
    save_model(model, './NeuralNet/my_model.h5')
    print_neural_network_predictions(model, './NeuralNet/Q_my_model' + str(i) + ".json")


def print_neural_network_predictions(model=None, filename=None, verbose=False):
    ordered_deck = get_deck()
    nn_npc = NeuralNetworkNPC(model)
    if model is None:
        model = nn_npc.model

    output = []

    ind = 0
    for card1 in ordered_deck:
        for card2 in ordered_deck:
            code1 = card1.encode()
            code2 = card2.encode()
            if code1 < code2:
                hand = Hand()
                hand.cards = [card1, card2]
                initial_num_chips = 20
                for money_bin in range(4):
                    for sb in range(2):
                        bank = int(initial_num_chips / 4) * money_bin
                        my_state, _ = encode_to_vector(hand.cards, [], sb, bank, initial_num_chips)
                        prediction = model.predict(my_state)
                        output.append([str(card1),
                                       str(card2),
                                       str(money_bin),
                                       "SB" if sb else "BB",
                                       str(prediction),
                                       str("call" if nn_npc.make_a_move(my_state) else "fold")])
                        ind += 1
    import json
    if verbose:
        pprint(output)
    if filename:
        with open(filename, 'w', encoding='utf8') as outfile:
            data = (json.dumps(output, sort_keys=True, ensure_ascii=False))
            outfile.write(data)
        with open(filename + "pretty.json", 'w', encoding='utf8') as outfile:
            data = (json.dumps(output, sort_keys=True, indent=1, ensure_ascii=False))
            outfile.write(data)


def encode_to_vector(hole_cards, community_cards, small_blind, num_of_chips, initial_num_of_chips):
    """Encode the preflop or river knowing 2 players cards"""
    # encode_to_vector vector of input value
    # structure of the feature vector is the following:
    # [0-51] indicate the probability of having specific card: 1 -> having 0 -> not 0.02 -> 0.02 probability for card
    # this property is used when player knows his own cards
    # for example if player1 has 2H and 2C: [ 0 ... 1[index of 2H], 0 ... 0 , 1[index of 2H], 0 ...]
    # opponents hand from player1 point of view [ 0.02 ... 0[index of 2H], 0.02 ... 0.02 , 0[index of 2H], 0.02 ...]
    # [52] probability of small blind 0 - big blind 1 - small blind
    # [53] money in player's bank 0 - no money at all, 1 - all the money possible  0.5 - half the money possible
    # for example num of chips for both players at start is 10 - both have 0.5 in corresponding vector
    # if at some point during this game player1 has 16 coins and player2 has 4 it corresponds to: [0.8] , 0.2]
    # [54-105] probability of card to be in community cards
    # during pre-flop similar to how from player1 point of view
    # after river - solid 1 and 0 on corresponding rivers
    encoded_vector = np.zeros([1, 106])
    hole_cards_codes = []
    for card in hole_cards:
        hole_card_code = Card.encode(card)
        encoded_vector[0, hole_card_code] = 1
        hole_cards_codes.append(hole_card_code)
    encoded_vector[0, 52] = 1 if small_blind else 0
    encoded_vector[0, 53] = num_of_chips / (2 * initial_num_of_chips)
    unknown_cards = 50
    community_cards_codes = []
    for card in community_cards:
        index = Card.encode(card)
        encoded_vector[0, 54 + index] = 1
        unknown_cards -= 1
        community_cards_codes.append(index)
    # pseudo probability, counting with repetitions
    unknown_card_prob = 1 / unknown_cards
    for i in range(0, 52):
        if i not in hole_cards_codes + community_cards_codes:
            encoded_vector[0, 54 + i] = (5 - len(community_cards)) * unknown_card_prob

    opponent_encoded_vector = np.copy(encoded_vector)

    unknown_cards -= 2
    unknown_card_prob = 1 / unknown_cards
    for i in range(0, 52):
        opponent_encoded_vector[0, i] = 2 * unknown_card_prob
    for i in hole_cards_codes + community_cards_codes:
        opponent_encoded_vector[0, i] = 0
    opponent_encoded_vector[0, 52] = 1 - encoded_vector[0, 52]  # sb / bb
    opponent_encoded_vector[0, 53] = 1 - encoded_vector[0, 53]  # money

    return encoded_vector, opponent_encoded_vector


if __name__ == '__main__':
    hole_cards = [Card("Heart", 14), Card("Heart", 13)]
    # community_cards = []
    community_cards = [Card("Heart", 12), Card("Heart", 11), Card("Heart", 10), Card("Heart", 9), Card("Heart", 8)]
    small_blind = 1
    _num_of_chips = 10
    initial_num_of_chips = 10
    my_vect, opp_vect = encode_to_vector(hole_cards, community_cards, small_blind, _num_of_chips, initial_num_of_chips)
    print(my_vect)
    print(opp_vect)
    print(my_vect - opp_vect)
