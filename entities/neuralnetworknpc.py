import numpy as np
from keras import Sequential
from keras.engine import InputLayer
from keras.layers import Dense
from keras.models import load_model, save_model


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
        return np.argmax(self.model.predict(encoded_state))


def create_empty_model():
    model = Sequential()
    model.add(InputLayer(input_shape=(58,)))
    model.add(Dense(10, activation='sigmoid'))
    model.add(Dense(2, activation='sigmoid'))
    model.compile(loss='mse', optimizer='adam')
    return model


def load_poker_model():
    return load_model('./NeuralNet/my_model.h5')


def save_poker_model(model):
    save_model(model, './NeuralNet/my_model.h5')


if __name__ == '__main__':
    npc = NeuralNetworkNPC()
    model = npc.model
    print(model.predict(np.zeros((1, 58))))
    save_poker_model(model)
    del model
    model = load_poker_model()
    print(model.predict(np.zeros((1, 58))))
