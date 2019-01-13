import sys

from entities.neuralnetworknpc import print_neural_network_predictions
from entities.neuralnetworktrainer import NeuralNetworkTrainer


def train_neural_network(enforce_play=False, save_every=100000, total_episodes=1000000, num_of_chips=20):
    nn = NeuralNetworkTrainer(num_of_chips)
    nn.train_agent(enforce_play=enforce_play, save_every=save_every, total_episodes=total_episodes)


if __name__ == "__main__":
    enforce_play = False
    save_every = 10000
    total_episodes = 100000
    num_of_chips = 20
    filename = "./NeuralNet/Q_after_training.json"
    if len(sys.argv) > 0:
        save_every = sys.argv[0]
        if len(sys.argv) > 1:
            episodes = sys.argv[1]
            if len(sys.argv) > 2:
                total_episodes = sys.argv[2]
                if len(sys.argv) > 3:
                    num_of_chips = sys.argv[3]
                    if len(sys.argv) > 4:
                        filename = sys.argv[4]
    train_neural_network(enforce_play=enforce_play, save_every=save_every, num_of_chips=num_of_chips)
    print_neural_network_predictions(filename=filename, verbose=True, )
