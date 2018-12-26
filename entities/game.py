from entities.deck import Deck
from entities.player import Player


class Game:

    def __init__(self, player_1_name="Player 1", player_1_mode="Random",
                 player_2_name="Player 2", player_2_mode="Random", bank=10):
        """Create a new game

        :param player_1_name: player 1 name.
        :param player_1_mode: if a player is a human.
        :param player_2_name: player 2 name.
        :param player_2_mode: if a player is a human.
        """
        self.sb_chips = 1
        self.bb_chips = 2
        self.sb = 0
        self.turn = 0
        self.step = 0
        self.pot = 0
        self.done = False
        self._p1 = Player(player_1_name, bank)
        self._p2 = Player(player_2_name, bank)
        self._p1.mode = player_1_mode
        self._p2.mode = player_2_mode
        self.deck = Deck()
        self.p = [self._p1, self._p2]

    def next_player(self):
        self.turn = 1 - self.turn

    def end_round(self):
        self.sb = 1 - self.sb
        self.turn = self.sb

    def render_game(self):
        for i in range(self.p.__len__()):
            print(
                "Player " + str(i + 1) + "- " + self.p[i].name + ", Cards : " +
                str(self.p[i].hand) + " and " + str(self.p[i].bank) + " coins")

        print("The pot is", self.pot)

    def a_player(self):
        """Returns the player that have the turn now"""
        return self.p[self.turn]

    def na_player(self):
        """Returns the player that does not have the turn now"""
        return self.p[1 - self.turn]

    def sb_player(self):
        """Return the small blind player"""
        return self.p[self.sb]

    def bb_player(self):
        """Return the big blind player"""
        return self.p[1 - self.sb]

    def player_all_in(self, p):
        """Adds all players money to the pot"""
        p.bet += p.bank
        self.pot += p.bank
        p.bank = 0

    def player_call(self, p, opponent_bet):
        """Try to Call the opponent. If can't - bet as much as possible"""
        to_bet = min(opponent_bet - p.bet, p.bank)
        p.bank -= to_bet
        p.bet += to_bet
        self.pot += to_bet

    def opponent_folded(self, p):
        """Awards pot to the player because his opponent has folded

        Also resets the pot to 0
        :param p: The player that did not fold
        :return:
        """
        p.bank += self.pot
        self.pot = 0

    def split_the_pot(self):
        for pl in self.p:
            pl.bank += pl.bet
            self.pot -= pl.bet
            pl.bet = 0
        if self.pot > 0:
            print("Error! Pot still contains %d", self.pot)

    def player_won(self, winner):
        gain = min(winner.bet * 2, self.pot)
        winner.bank += gain
        self.pot -= gain
        if self.pot > 0:
            loser = [pl for pl in self.p if pl.name != winner.name]
            loser[0].bank += self.pot

    def place_blinds(self):
        """Places blinds of the corresponding players in the pot
        """
        sb = self.a_player()
        bb = self.na_player()
        sb.bet = self.sb_chips
        bb.bet = self.bb_chips
        sb.bank -= self.sb_chips
        bb.bank -= self.bb_chips
        self.pot += self.sb_chips + self.bb_chips

    def players_draw_cards(self):
        """Draws two cards for each player"""
        for p in self.p:
            for i in range(2):
                p.take_card(self.deck.draw_card())

    def new_step(self):
        """Clear players hands and resets the deck"""
        for a in self.p:
            a.hand.clear_hand()
            a.bet = 0
        self.deck = Deck()
        self.pot = 0

    # ===============================================
    # ------------------Name of Hand-----------------
    # ===============================================
    # noinspection PyMethodMayBeStatic
    def name_of_hand(self, type_of_hand):
        if type_of_hand == 0:
            return "High Card"
        elif type_of_hand == 1:
            return "Pair"
        elif type_of_hand == 2:
            return "2 Pair"
        elif type_of_hand == 3:
            return "3 of a Kind"
        elif type_of_hand == 4:
            return "Straight"
        elif type_of_hand == 5:
            return "Flush"
        elif type_of_hand == 6:
            return "Full House"
        elif type_of_hand == 7:
            return "Four of a Kind"
        elif type_of_hand == 8:
            return "Straight Flush"
        else:
            return "Royal Flush"

    # ===============================================
    # ---------------------Score---------------------
    # ===============================================
    @staticmethod
    def score(hand):
        """Before sending the hand to this function sort it first!!!

        :rtype: [int,[int]]
        :param hand: Sorted hand to assign a score
        :return: hand score, hand values
        """
        final_hand = None
        score = 0

        # ------------------------------------------------
        # -------------Checking for Pairs-----------------
        # ------------------------------------------------
        pairs = {}
        prev = 0

        # Keeps track of all the pairs in a dictionary where the key is
        # the pair's card value
        # and the value is the number occurrences. Eg. If there are 3
        # Kings -> {"13":3}
        for card in hand.cards:
            if prev == card.rank:
                key = card.rank
                if key in pairs:
                    pairs[key] += 1
                else:
                    pairs[key] = 2
            prev = card.rank

        # Keeps track of the number of pairs and sets. The value of the
        # previous dictionary is the key. Therefore if there is a pair of 4s
        # and 3 kings -> {"2":1,"3":1}
        nop = {}
        for k, v in pairs.items():
            if v in nop:
                nop[v] += 1
            else:
                nop[v] = 1

        # Here we determine the best possible combination the hand can be
        # knowing if the
        # hand has a four of a kind, three of a kind, and multiple pairs.

        if 4 in nop:  # Has 4 of a kind, assigns the score and the value of the
            score = 7
            final_hand = pairs.keys()
            # ensures the first kicker is the value of the 4 of a kind
            final_hand = [key for key in final_hand if pairs[key] == 4]
            key = final_hand[0]

            # Gets a list of all the cards remaining once the the 4 of a kind
            # is removed 
            temp = [card.rank for card in hand.cards if card.rank != key]
            # Gets the last card in the list which is the highest remaining
            # card to be used in the event of a tie 

            card_value = temp.pop()
            final_hand.append(card_value)

            return [score, final_hand]
            # Returns immediately because this is the best possible hand
            # doesn't  check get the best 5 card hand if all users have
            # a 4 of a kind

        elif 3 in nop:  # Has At least 3 of A Kind
            if nop[3] == 2 or 2 in nop:
                # Has two 3 of a kind, or a pair
                # and 3 of a kind (fullhouse)
                score = 6

                # gets a list of all the pairs and reverses it
                final_hand = list(pairs.keys())
                final_hand.reverse()

                temp = final_hand

                # ensures the first kicker is the value of the highest 3 of a
                # king
                final_hand = [key for key in final_hand if pairs[key] == 3]
                if final_hand.__len__() > 1:
                    # if there are two 3 of a kinds,
                    # take the higher as the first kicker
                    final_hand.pop()  # removes the lower one from the kicker

                # removes the value of the kicker already in the list
                temp.remove(final_hand[0])
                # Gets the highest pair or 3 of kind and adds that to the
                # kickers list
                card_value = temp[0]
                final_hand.append(card_value)

            else:  # Has Only 3 of A Kind
                score = 3

                final_hand = list(pairs.keys())  # Gets the value of the 3 of a
                # king
                key = final_hand[0]

                # Gets a list of all the cards remaining once the three
                # of a kind is removed
                temp = [card.rank for card in hand.cards if card.rank != key]
                # Get the 2 last cards in the list which are the 2 highest to
                # be used in the
                # event of a tie
                card_value = temp.pop()
                final_hand.append(card_value)

                card_value = temp.pop()
                final_hand.append(card_value)

        elif 2 in nop:  # Has at Least a Pair
            if nop[2] >= 2:  # Has at least 2  or 3 pairs
                score = 2

                # Gets the card value of all the pairs
                final_hand = list(pairs.keys())
                # reverses the key so highest pairs are used
                final_hand.reverse()

                if final_hand.__len__() == 3:  # if the user has 3 pairs takes
                    # only the highest 2
                    final_hand.pop()

                key1 = final_hand[0]
                key2 = final_hand[1]

                # Gets a list of all the cards remaining once the the 2
                # pairs are removed
                temp = [card.rank for card in hand.cards if
                        card.rank != key1 and card.rank != key2]
                # Gets the last card in the list which is the highest 
                # remaining card to be used in
                # the event of a tie
                card_value = temp.pop()
                final_hand.append(card_value)

            else:  # Has only a pair
                score = 1

                final_hand = list(pairs.keys())  # Gets the value of the pair
                key = final_hand[0]

                # Gets a list of all the cards remaining once pair are removed
                temp = [card.rank for card in hand.cards if card.rank != key]
                # Gets the last 3 cards in the list which are the highest 
                # remaining cards
                # which will be used in the event of a tie
                card_value = temp.pop()
                final_hand.append(card_value)

                card_value = temp.pop()
                final_hand.append(card_value)

                card_value = temp.pop()
                final_hand.append(card_value)

        # ------------------------------------------------
        # ------------Checking for Straight---------------
        # ------------------------------------------------
        # Doesn't check for the ace low straight
        counter = 0
        high = 0
        straight = False

        # Checks to see if the hand contains an ace, and if so starts
        # checking for the straight
        # using an ace low
        if hand.cards[6].rank == 14:
            prev = 1
        else:
            prev = None

        # Loops through the hand checking for the straight by comparing the 
        # current card to the
        # the previous one and tabulates the number of cards found in a row
        # ***It ignores pairs by skipping over cards that are similar to the 
        # previous one
        for card in hand.cards:
            if prev and card.rank == (prev + 1):
                counter += 1
                if counter >= 4:  # A straight has been recognized
                    straight = True
                    high = card.rank
            elif prev and prev == card.rank:  # ignores pairs when checking 
                # for the straight
                pass
            else:
                counter = 0
            prev = card.rank

        # If a straight has been realized and the hand has a lower score than
        # a straight
        if (straight or counter >= 4) and score < 4:
            straight = True
            score = 4
            final_hand = [high]
            # Records the highest card value in the straight in 
            # the event of a tie

        # ------------------------------------------------
        # -------------Checking for Flush-----------------
        # ------------------------------------------------
        total = {}

        # Loops through the hand calculating the number of cards of each suit.
        # The suit value is the key and for every occurrence the
        # counter is incremented
        for card in hand.cards:
            key = card.suit
            if key in total:
                total[key] += 1
            else:
                total[key] = 1

        # key represents the suit of a flush if it is within the hand
        key = "☻"
        for k, v in total.items():
            if v >= 5:
                key = k

        # If a flush has been realized and the hand has a lower score
        # than a flush
        if not "☻".__eq__(key) and score < 5:
            flush = True
            score = 5
            final_hand = [card.rank for card in hand.cards if card.suit == key]

            # ------------------------------------------------
            # -----Checking for Straight & Royal Flush--------
            # ------------------------------------------------
            if flush and straight:
                # Doesn't check for the ace low straight
                counter = 0
                high = 0
                straight_flush = False

                # Checks to see if the hand contains an ace, and if so starts
                # checking for the straight
                # using an ace low
                if final_hand[final_hand.__len__() - 1] == 14:
                    prev = 1
                else:
                    prev = None

                # Loops through the hand checking for the straight by 
                # comparing the current card to the the previous
                # one and tabulates the number of cards found in a row
                # It ignores pairs by skipping over cards that are similar
                # to the previous one
                for card in final_hand:
                    if prev and card == (prev + 1):
                        counter += 1
                        if counter >= 4:  # A straight has been recognized
                            straight_flush = True
                            high = card
                    elif prev and prev == card:  # ignores pairs when 
                        # checking for the straight
                        pass
                    else:
                        counter = 0
                    prev = card

                # If a straight has been realized and the hand has a lower
                # score than a straight
                if straight_flush:
                    if high == 14:
                        score = 9
                    else:
                        score = 8
                    final_hand = [high]
                    return [score, final_hand]

            elif flush:  # if there is only a flush then determines the kickers
                final_hand.reverse()

                # This ensures only the top 5 kickers are selected and not more.
                length = final_hand.__len__() - 5
                for i in range(0, length):
                    # Pops the last card of the list which is the lowest
                    final_hand.pop()

        # ------------------------------------------------
        # -------------------High Card--------------------
        # ------------------------------------------------
        if score == 0:  # If the score is 0 then high card is the best
            # possible hand

            # It will keep track of only the card's value
            final_hand = [int(card.rank) for card in hand.cards]
            # Reverses the list for easy comparison in the event of a tie
            final_hand.reverse()
            # Since the hand is sorted it will pop the two lowest cards
            # position 0, 1 of the list
            final_hand.pop()
            final_hand.pop()

            # The reason we reverse then pop is because lists are
            # inefficient at popping from the beginning of the list,
            # but fast at popping from the end therefore we reverse the
            # list and then pop the last two elements which will be the two
            # lowest cards in the hand

        # Return the score, and the kicker to be used in the event of a tie
        return [score, final_hand]

        # ===============================================
        # ---------------Determine Winner----------------
        # ===============================================

    @staticmethod
    def determine_winner(results):
        # the highest score if found
        high = 0
        for r in results:
            if r[0] > high:
                high = r[0]

        kicker = {}
        counter = 0
        # Only the kickers of the player's hands that are tied for the
        # win are analysed
        for r in results:
            if r[0] == high:
                kicker[counter] = r[1]

            counter += 1

        # if the kickers of multiple players are in the list then we have
        # a tie and need to begin comparing kickers
        if kicker.__len__() > 1:
            # Iterate through all the kickers
            # It is important to the number of kickers differ based on
            # the type of hand
            number_of_kickers = (kicker[list(kicker.keys())[0]]).__len__()
            for i in range(0, number_of_kickers):
                high = 0
                for k, v in kicker.items():
                    if v[i] > high:
                        high = v[i]

                # only hands matching the highest kicker remain in the
                # list to be compared
                kicker = {k: v for k, v in kicker.items() if v[i] == high}

                # if only one the kickers of one player remains that they
                # are the winner
                if kicker.keys().__len__() <= 1:
                    return [list(kicker.keys()).pop()]

        else:  # A clear winner was found
            return [list(kicker.keys()).pop()]

        # A tie occurred, a list of the winners is returned
        return list(kicker.keys())
