from pprint import pprint

import numpy as np
from keras import Sequential
from keras.engine import InputLayer
from keras.layers import Dense
from keras.models import load_model, save_model

from entities import Hand
from entities.deck import get_deck
from gym_poker.envs.neural_net_poker_env import NeuralNetPokerEnv


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

    def make_a_move(self, encoded_state):
        """Makes a decision whenever to fold or play by forward feeding

        :param encoded_state: encoded representation of the state
        :return action 0 for fold 1 for play:
        """
        return 1 if (self.model.predict(encoded_state)) > 0.5 else 0


def create_empty_model():
    model = Sequential()
    model.add(InputLayer(input_shape=(58,)))
    model.add(Dense(58, activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid', kernel_initializer='normal', ))
    model.compile(loss='binary_crossentropy', optimizer='adam')
    return model


def load_poker_model():
    return load_model('./NeuralNet/my_model.h5')


def save_poker_model(model, i="_end"):
    save_model(model, './NeuralNet/my_model' + str(i) + '.h5')
    save_model(model, './NeuralNet/my_model.h5')
    print_neural_network_predictions(model, './NeuralNet/Q_my_model' + str(i) + ".json")


if __name__ == '__main__':
    npc = NeuralNetworkNPC()
    model = npc.model
    print(model.predict(np.zeros((1, 58))))
    save_poker_model(model)
    del model
    model = load_poker_model()
    print(model.predict(np.zeros((1, 58))))


def classify_prediction(prediction):
    return 1 if prediction > 0.5 else 0


def print_neural_network_predictions(model=None, filename=None, verbose=False):
    ordered_deck = get_deck()
    if model is None:
        nn_npc = NeuralNetworkNPC(model)
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
                        prediction = (model.predict(
                            NeuralNetPokerEnv.encode(hand, sb, int(initial_num_chips / 4) * money_bin,
                                                     initial_num_chips)))
                        # print('{},{},{},{},{},{}'.format(card1, card2, money_bin, "SB" if sb else "BB", prediction,
                        #                                  np.argmax(np.array(prediction))))
                        output.append([str(card1),
                                       str(card2),
                                       str(money_bin),
                                       "SB" if sb else "BB",
                                       str(prediction),
                                       str("call" if classify_prediction(prediction) else "fold")])
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
