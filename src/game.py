from Blackjack.src.working import *


# TODO special funktionen

def draw_card(deck):
    return deck.pop()


def calculate_max_points(points, aces):
    """Calculates the best points from the original point count and the aces count.

    :returns: calculated amount of points
    """
    while aces > 0:
        if points + 10 <= 21:
            points += 10
            aces -= 1
        else:
            aces = 0

    return points


def shuffled_deck(no):
    """Creates a big card-deck out of multiple standard card decks.

    :param no: number of card decks
    :returns: the big card-deck created
    """
    cards = []
    for i in range(no):
        for e in islice(Color, 4):
            cards.append(Ace(e))
            cards.append(King(e))
            cards.append(Queen(e))
            cards.append(Joker(e))
            cards.append(Ten(e))
            cards.append(Nine(e))
            cards.append(Eight(e))
            cards.append(Seven(e))
            cards.append(Six(e))
            cards.append(Five(e))
            cards.append(Four(e))
            cards.append(Three(e))
            cards.append(Two(e))

    random.shuffle(cards)
    return cards


class Game(object):

    def __init__(self, ui):
        self.ui = ui
        self.money = 500
        self.bet = 0

        self.running = False
        self.player_blackjack = False
        self.dealer_blackjack = False
        self.pass_cards = False

        self.dealer_cards = []
        self.dealer_points = 0

        self.player_cards = []
        self.player_points = 0
        self.player_aces = 0

        self.cards = shuffled_deck(6)

        # self.blackjack_dealer = True

    def start(self, bet):
        """Player can make his bet for this round. Starts the game after the bet is done.
        """
        if not self.running:
            if self.bet_money(bet):
                self.running = True
                self.ui.deactivate_bet()
                self.initial_card()

    def next_game(self):
        self.running = False
        self.player_blackjack = False
        self.dealer_blackjack = False
        self.pass_cards = False

        self.dealer_cards = []
        self.dealer_points = 0

        self.player_cards = []
        self.player_points = 0
        self.player_aces = 0

        self.cards = shuffled_deck(6)

    def initial_card(self):
        """The dealer draws his first card.
        """
        card = draw_card(self.cards)
        self.dealer_cards.append(card)
        if isinstance(card, Ace):
            self.dealer_points += 10
            # TODO insurance
        #    # if the dealer's first card is an ace. the player can decide to insure himself against blackjack.
        #    # The player's money will be deposited into the insurance
        #    insured, insurance_lane = ask_insurance(money)
        #    money -= insurance_lane
        self.dealer_points += card.__get_value__()

        self.ui.update_cards(0, self.dealer_cards)

        self.first_player_cards()

    def first_player_cards(self):
        """Player draws his first two cards. If a blackjack is scored, the player's turn will be ended
        """
        for i in range(2):
            card = draw_card(self.cards)
            self.player_cards.append(card)
            self.player_points += card.__get_value__()
            if isinstance(card, Ace):
                self.player_aces += 1

        self.ui.update_cards(1, self.player_cards)

        # blackjack with first two cards
        if calculate_max_points(self.player_points, self.player_aces) == 21:
            self.player_blackjack = True
            self.ui.deactivate_draw()

    def draw(self):
        """Draws a card from the card stack. Adds points and counts Aces for further calculation.
        Calls the function to update the UI. If the player hits 21 points or more drawing is deactivated.
        """
        if not self.pass_cards:
            card = draw_card(self.cards)
            self.player_cards.append(card)
            self.player_points += card.__get_value__()
            if isinstance(card, Ace):  # ace gives 1 or 11 points. This counts how many aces were drawn
                self.player_aces += 1

            self.ui.update_cards(1, self.player_cards)
            points = calculate_max_points(self.player_points, self.player_aces)
            if points >= 21:
                if points == 21:
                    self.ui.deactivate_draw()
                else:
                    self.pass_turn(True)

    def pass_turn(self, overdraw):
        """Player passes from drawing more cards in his draw phase.
        Calls the function to deactivate the buttons in the UI,
        then starts the dealer phase."""
        if not self.pass_cards:
            strg = ""
            self.pass_cards = True
            self.ui.deactivate_buttons()

            self.player_points = calculate_max_points(self.player_points, self.player_aces)
            if self.player_blackjack:
                strg += "\nBlackjack"
            if self.player_points > 21:
                strg += "\nÜberzogen"

            strg += "\nPunkte: " + str(self.player_points)
            self.ui.add_text_to_textfield(1, strg)

        if not overdraw:
            self.dealer_draw_phase()
            self.game_results()

    def dealer_draw_phase(self):
        """Draw more cards while dealer has less then 17 points, but stops otherwise."""
        strg = ""
        while self.dealer_points <= 16:
            card = draw_card(self.cards)
            self.dealer_cards.append(card)
            # ace gives dealer 11 points if he does not overdraw and gives him 1 if he would overdraw otherwise
            if isinstance(card, Ace):
                if self.dealer_points + 11 > 21:
                    self.dealer_points += 1
                else:
                    self.dealer_points += 11
            else:
                self.dealer_points += card.__get_value__()

            # overdrawn
            if self.dealer_points > 21:
                strg += "\nÜberzogen"

            # blackjack
            if len(self.dealer_cards) == 2 and self.dealer_points == 21:
                strg += "\nBlackjack"
                self.blackjack_dealer = True

        self.ui.update_cards(0, self.dealer_cards)
        strg += "\nPunkte: " + str(self.dealer_points)
        self.ui.add_text_to_textfield(0, strg)

        self.game_results()

        # if insured:
        #   payout_insurance(insurance_lane, money)

    def bet_money(self, value):
        """Player bets an amount of his own money. Only works if he player has the necessary funds.

        :param value: amount of money the player wants to bet
        :returns: boolean weather betting was successful"""
        if isinstance(value, int) and 0 < value <= self.money:
            self.money -= value
            self.bet += value
            self.ui.print_bet_and_money(self.bet, self.money)
            return True
        return False

    def game_results(self):
        """Evaluates the dealer's and the player's points and calls the fitting function based on this."""
        if self.dealer_points > 21:  # dealer overdrew
            self.win()
        elif self.player_points > 21:  # player overdrew
            self.lose()
        elif self.player_points > self.dealer_points:  # player closer to 21
            self.win()
        elif self.player_points < self.dealer_points:  # dealer closer to 21
            self.lose()
        elif self.player_blackjack and not self.dealer_blackjack:  # only player BJ
            self.win()
        elif not self.player_blackjack and self.dealer_blackjack:  # only dealer BJ
            self.lose()
        elif self.player_points == self.dealer_points:  # draw between player and dealer
            self.undecided()

        self.running = False
        self.ui.activate_next_button()

    def win(self):
        """Player gets winnings based on his hand-cards."""
        winnings = self.calculate_winning()
        self.money += winnings
        self.bet = 0

        self.ui.print_bet_and_money(self.bet, self.money)

    def undecided(self):
        """Player gets his bet back."""
        self.money += self.bet
        self.bet = 0

        self.ui.print_bet_and_money(self.bet, self.money)

    def lose(self):
        """Player loses the money he bet this round."""
        self.bet = 0

        self.ui.print_bet_and_money(self.bet, self.money)

    def calculate_winning(self):
        """Calculate winnings based on hand cards.

        :returns: amount of money the player has won"""
        winning = 0
        if self.player_points < 21:  # normal win 2:1
            winning = 2 * self.bet
        elif self.player_points == 21:
            if len(self.player_cards) == 3 and all(c.__get_value__() == 7 for c in self.player_cards):  # 777 win 3:2
                winning = 3 * self.bet / 2 + self.bet
            elif len(self.player_cards) == 2:  # blackjack 3:2
                winning = 3 * self.bet / 2 + self.bet
            else:
                winning = 2 * self.bet  # no special win with 21 points

        return winning
