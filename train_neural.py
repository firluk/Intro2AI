import sys

from entities.neuralnetworknpc import print_neural_network_predictions
from entities.neuralnetworktrainer import NeuralNetworkTrainer


def train_neural_network(enforce_play=False, save_every=100000, total_episodes=1000000, num_of_chips=20):
    nn = NeuralNetworkTrainer(num_of_chips)
    nn.train_agent(enforce_play=enforce_play, save_every=save_every, total_episodes=total_episodes)


if __name__ == "__main__":
    save_every_arg = 10000
    total_episodes_arg = 100000
    num_of_chips_arg = 20
    filename = "./NeuralNet/dump.txt"
    if len(sys.argv) > 1:
        save_every_arg = int(sys.argv[1])
        if len(sys.argv) > 2:
            total_episodes_arg = int(sys.argv[2])
            if len(sys.argv) > 3:
                num_of_chips_arg = int(sys.argv[3])
                if len(sys.argv) > 4:
                    filename = sys.argv[4]
                    if len(sys.argv) > 5:
                        verbose = sys.argv[5]
    else:
        print(
            "Usage: [save every i iterations: Int][total episodes: Int][number of chips: Int][filename of Q-table table repr]")
    train_neural_network(save_every=save_every_arg,
                         num_of_chips=num_of_chips_arg,
                         total_episodes=total_episodes_arg)
    print_neural_network_predictions(filename=filename, verbose=False)
