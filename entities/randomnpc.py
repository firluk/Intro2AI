import random


class RandomNPC:

    @staticmethod
    def make_a_move():
        return bool(random.randrange(2))
