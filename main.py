from Entities.Game import Game


def small_blind(p, game):
    if p.h:
        retry = True
        while retry:
            inp = input("Do you want to (F)old or go (A)ll in?").lower()
            if inp == "f":
                return False
            elif inp == "a":
                game.player_all_in(p)
                retry = False
            game.render_game()
        return True
    else:
        pass


def big_blind(p, g):
    if p.h:
        retry = True
        while retry:
            inp = input("Do you want to (F)old or (C)all?").lower()
            if inp == "f":
                return False
            elif inp == "c":
                g.player_call(p)
                retry = False
        g.render_game()
        return True
    else:
        pass


def resolve_hands(p, g):
    pass


def main():
    game = Game("Tegra", True, "Firluk", True)
    while not game.done:
        game.place_blinds()
        if game.a_player().bank < 0 or game.na_player().bank < 0:
            game.done = True
            break
        game.players_draw_cards()
        game.render_game()
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
    if game.done:
        if game.p[0].bank <= 0 < game.p[1].bank:
            s = game.p[1].name + " has won the game with "
            s += game.p[1].bank + " coins"
            print(s)
        elif game.p[1].bank <= 0 < game.p[0].bank:
            s = game.p[0].name + " has won the game with "
            s += game.p[0].bank + " coins"
            print(s)


if __name__ == "__main__":
    main()
