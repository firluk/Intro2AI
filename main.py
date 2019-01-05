from entities.game import Game
from entities.randomnpc import RandomNPC

player_types = {"h": "Human", "r": "Random", "q": "Qtable"}


def small_blind(p, game):
    move = False
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
        pass
    else:
        pass
    if not move:
        print(p.name, "folds")
        return False
    else:
        print(p.name, "goes all in")
        game.player_all_in(p)
        return True


def big_blind(p, g):
    move = False
    if p.mode.__eq__(player_types["h"]):
        retry = True
        while retry:
            inp = input("Do you want to (F)old or (C)all?").lower()
            if inp == "f":
                move = False
            elif inp == "c":
                retry = False
        g.render_game()
    elif p.mode.__eq__(player_types["r"]):
        move = RandomNPC.make_a_move()
    elif p.mode.__eq__(player_types["q"]):
        pass
    else:
        pass
    if not move:
        print(p.name, "folds")
        return False
    else:
        print(p.name, "calls")
        g.player_call(p, g.na_player().bet)
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
        g.player_won(p[winners[0]])


def main():
    # [0] player1 won accumulator, [1] player2 won accumulator
    # stats = [0, 0] WIP
    for games in range(10):
        # q - indicate q-table, indicate
        game = Game("Tegra", player_types["q"], "Firluk", player_types["r"])
        while not game.done:
            if game.a_player().bank <= 0 or game.na_player().bank <= 0:
                game.done = True
                break
            else:
                game.place_blinds()
            game.players_draw_cards()
            game.render_game()
            print(game.p[game.turn].name + " is small blind")
            result = small_blind(game.p[game.turn], game)
            game.next_player()
            if result:
                result = big_blind(game.p[game.turn], game)
                if result:
                    resolve_hands(game.p, game)
                else:
                    game.opponent_folded(game.na_player())
            else:
                game.opponent_folded(game.a_player())
            game.new_step()

        # region End game
        if game.done:
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

        # endregion


if __name__ == "__main__":
    main()
