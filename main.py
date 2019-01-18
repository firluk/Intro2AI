import copy
import sys
from random import random

from entities.game import Game
from entities.neuralnetworknpc import NeuralNetworkNPC, encode_to_vector
from entities.qtablenpc import QtableNPC
from entities.randomnpc import RandomNPC
from gym_poker.envs.poker_env import PokerEnv

player_types = {"h": "Human", "r": "Random", "q": "Qtable", "n": "NeuralNet"}


def small_blind(p, game, neural_model_npc=None, q_table_npc=None):
    move = False
    if p.bank == 0:
        print(p.name + " can't fold - no money left to play next hand")
        move = 1
    else:
        if p.mode.__eq__(player_types["h"]):
            retry = True
            while retry:
                inp = input("Do you want to (F)old or go (A)ll in?").lower()
                if inp == "f":
                    move = False
                elif inp == "a":
                    move = True
                    retry = False
                game.render_game()
        elif p.mode.__eq__(player_types["r"]):
            move = RandomNPC.make_a_move()
        elif p.mode.__eq__(player_types["q"]):
            move = q_table_npc.make_a_move(PokerEnv.encode(p.hand, 0, p.bank, game.bank))
        elif p.mode.__eq__(player_types["n"]):
            hole_cards = p.hand.cards[0:2]
            community_cards = p.hand.cards[2:]
            small_blind = 1
            num_of_chips = p.bank
            initial_num_of_chips = game.bank
            state, _ = encode_to_vector(hole_cards, community_cards, small_blind, num_of_chips,
                                        initial_num_of_chips)
            move = neural_model_npc.make_a_move(state)
        else:
            pass
    if not move:
        print(p.name, "folds")
        return False
    else:
        print(p.name, "goes all in")
        game.player_all_in(p)
        return True


def big_blind(p, game, neural_model_npc=None, q_table_npc=None):
    if p.bank == 0:
        print(p.name + " can't fold - no money left to play next hand")
        move = 1
    else:
        if p.mode.__eq__(player_types["h"]):
            retry = True
            while retry:
                inp = input("Do you want to (F)old or (C)all?").lower()
                if inp == "f":
                    move = False
                elif inp == "c":
                    retry = False
            game.render_game()
        elif p.mode.__eq__(player_types["r"]):
            move = RandomNPC.make_a_move()
        elif p.mode.__eq__(player_types["q"]):
            move = q_table_npc.make_a_move(PokerEnv.encode(p.hand, 1, p.bank, game.bank))
        elif p.mode.__eq__(player_types["n"]):
            hole_cards = p.hand.cards[0:2]
            community_cards = p.hand.cards[2:]
            small_blind = 0
            num_of_chips = p.bank
            initial_num_of_chips = game.bank
            state, _ = encode_to_vector(hole_cards, community_cards, small_blind, num_of_chips,
                                        initial_num_of_chips)
            move = neural_model_npc.make_a_move(state)
        else:
            pass
    if not move:
        print(p.name, "folds")
        return False
    else:
        print(p.name, "calls")
        game.player_call(p, game.na_player().bet)
        return True


def resolve_hands(p, g):
    """Check who has strongest hand and divide the pot accordingly

    :param p: List of players to resolve the winner
    :param g: Game object
    :return:
    """
    # take five additional cards from the deck
    # add them to users hand
    for c in range(5):
        new_card = g.deck.draw_card()
        for player in p:
            player.hand.add_card(new_card)

    # sort the hands
    for pl in p:
        pl.hand.sort()

    print("Resolving player hands")
    g.render_game()

    # get the absolute score of the hand and the best five cards
    results = []
    for player in p:
        results.append(Game.score(player.hand))
    for i in range(g.p.__len__()):
        print(g.p[i].name, "has", g.name_of_hand(results[i][0]))

    # select the winner
    winners = Game.determine_winner(results)
    # award the pot to the winner
    if winners.__len__() > 1:
        # split the pot
        print("No winner - split the pot")
        g.split_the_pot()
    else:
        print(p[winners[0]].name, "has taken the pot")
        print(p[winners[0]].name, "gained", min(p[winners[0]].bet * 2, g.pot))
        g.player_won(p[winners[0]])


def main(p1, p2, num_of_games, num_of_chips):
    import time
    start_time = time.time()
    # [0] player1 won accumulator, [1] player2 won accumulator
    stats = [0, 0]
    game_lengths_won_by_p1 = [0]
    game_lengths_won_by_p2 = [0]
    #  successful bluff is when p1 is when SB goes all-in, and opponent folds, but would have won if called
    bluffs_p1 = [0, 0]
    bluffs_p2 = [0, 0]
    if "n" in [p1, p2]:
        neural_npc = NeuralNetworkNPC()
    else:
        neural_npc = None
    if "q" in [p1, p2]:
        q_table_npc = QtableNPC()
    else:
        q_table_npc = None
    for games in range(num_of_games):
        # q - indicate q-table, indicate
        game = Game(player_types[p1], player_types[p1], player_types[p2], player_types[p2], bank=num_of_chips)
        if random() > 0.5:
            game.end_round()
        game_length = 0
        while not game.done:
            if game.a_player().bank <= 0 or game.na_player().bank <= 0:
                game.done = True
                break
            else:
                game.render_game()
                print(game.p[game.turn].name + " is small blind")
                print("Placing blinds")
                game.place_blinds()
                game.render_game()
            game.players_draw_cards()
            current_player_index = game.turn
            result = small_blind(game.p[game.turn], game, neural_model_npc=neural_npc, q_table_npc=q_table_npc)
            game.next_player()
            if result:
                result = big_blind(game.p[game.turn], game, neural_model_npc=neural_npc, q_table_npc=q_table_npc)
                if result:
                    resolve_hands(game.p, game)
                else:
                    # bluff?
                    results = []
                    community_cards = []
                    for i in range(5):
                        community_cards.append(game.deck.draw_card())
                    for ep in game.p:
                        hand = copy.deepcopy(ep.hand)
                        hand.cards.extend(community_cards)
                        hand.sort()
                        results.append(Game.score(hand))
                    # select the winner
                    winners = Game.determine_winner(results)
                    if winners[0] == current_player_index:
                        if current_player_index == 0:
                            bluffs_p1[0] += 1
                        else:
                            bluffs_p2[0] += 1
                    if current_player_index == 0:
                        bluffs_p1[1] += 1
                    else:
                        bluffs_p2[1] += 1
                    game.opponent_folded(game.na_player())
            else:
                game.opponent_folded(game.a_player())
            game.new_step()
            print()
            game_length += 1

        # region End game
        if game.done:
            if game.p[0].bank > game.p[1].bank:
                stats[0] += 1
                game_lengths_won_by_p1.append(game_length)
            else:
                stats[1] += 1
                game_lengths_won_by_p2.append(game_length)
            for pl in game.p:
                pl.bank += pl.bet
                pl.bet = 0
            if game.a_player().bank <= 0:
                pl = game.na_player()
            else:
                pl = game.a_player()
            s = pl.name + " has won the game with "
            s += str(pl.bank) + " coins"

            print(s)
        print('\n')
        # endregion
        print(stats)
    print("In total: Player1[" + player_types[p1] + "] has won " + str(stats[0]))
    print("In total: Player2[" + player_types[p2] + "] has won " + str(stats[1]))
    if len(game_lengths_won_by_p1) > 1:
        print("Average game length when Player1[" + player_types[p1] + "] has won "
              + str(round(sum(game_lengths_won_by_p1) / len(game_lengths_won_by_p1), 2)))
    if len(game_lengths_won_by_p2) > 1:
        print("Average game length when Player2[" + player_types[p2] + "] has won "
              + str(round(sum(game_lengths_won_by_p2) / len(game_lengths_won_by_p2), 2)))
    print("Successful bluffs by Player1[" + player_types[p1] + "] "
          + str(bluffs_p1[0])
          + " / "
          + str(bluffs_p1[1]))
    print("Successful bluffs by Player2[" + player_types[p2] + "] "
          + str(bluffs_p2[0])
          + " / "
          + str(bluffs_p2[1]))
    print("time elapsed: {:.2f}s".format(time.time() - start_time))


if __name__ == "__main__":
    # args - player1 , player2
    # allow to play versus neural net's q-table
    # allow to play versus q-learning q-table
    # allow to play versus random
    # allow to play as human
    # args - [h/r/n/q] [h/r/n/q] [number of games] [number of chips]
    if len(sys.argv) > 1:
        p1_arg = sys.argv[1]
        p2_arg = sys.argv[2]
        num_of_games_arg = int(sys.argv[3])
        num_of_chips_arg = int(sys.argv[4])
    else:
        print("Usage: [h/r/n/q] [h/r/n/q] [number of games] [number of chips]")
        print("h - human | r - random | n-neural network | q - q-learning q-table")
        print("Using default run configurations: p1 - r, p2 - n, number of games - 100")
        p1_arg = "r"
        p2_arg = "n"
        num_of_games_arg = 100
        num_of_chips_arg = 20
    main(p1=p1_arg, p2=p2_arg, num_of_games=num_of_games_arg, num_of_chips=num_of_chips_arg)
