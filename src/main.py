from Blackjack.src.working import *

money = 500
blackjack_player, blackjack_dealer = False, False
insured, insurance_lane = False, 0

# card-list and points for participants
dealer = [[], 0]
player = [[], 0, 0]  # cards, points, number of ace cards

# player sets an amount he wants to bet
while True:
    # bet = input("Wieviel möchten Sie setzen?")
    bet = "50"
    if bet.isnumeric():
        bet = int(bet)
        if 0 < bet <= money:
            money -= bet
            break

# create deck of all cards
cards = shuffled_deck(6)

# initially dealer draws one card...
card = draw_card(cards)
dealer[0].append(card)
if isinstance(card, Ace):
    dealer[1] += 10
    # if the dealer's first card is an ace. the player can decide to insure himself against blackjack.
    # The player's money will be deposited into the insurance
    insured, insurance_lane = ask_insurance(money)
    money -= insurance_lane
dealer[1] += card.__get_value__()
print_score("Dealer", dealer)

# ...and player draws two cards
for i in range(2):
    card = draw_card(cards)
    player[0].append(card)
    player[1] += card.__get_value__()
    if isinstance(card, Ace):
        player[2] += 1
print_score("Spieler", player)

if not calculate_max_points(player) == 21:  # no blackjack
    # player - turn
    # draw cards but try not to hit 21 points (bust)
    while player[1] < 21:
        decision = input("\nMöchten Sie eine weitere Karte ziehen? [y/n]").lower()
        if not (decision == "y" or decision == "n"):
            continue
        if decision == "n" or calculate_max_points(player) == 21:
            break
        if decision == "y":
            card = draw_card(cards)
            player[0].append(card)
            player[1] += card.__get_value__()
            if isinstance(card, Ace):  # ace gives 1 or 11 points. This counts how many aces were drawn
                player[2] += 1
            print_score("Spieler", player)

    player[1] = calculate_max_points(player)
    print(player[1])

    # player wins if he has triple seven and is removed from the game
    if len(player[0]) == 3 and all(c.__get_value__() == 7 for c in player[0]):
        win(money, calculate_winning(bet, player))

    # player loses if busted
    if player[1] > 21:
        lose(money)

else:  # blackjack
    player[1] = 21
    player[2] = 0
    blackjack_player = True
    if isinstance(dealer[0][0], Ace):  # player has Blackjack and dealer has only Ace -> possibility for 1:1 payout
        dec, money = payout_option(bet, money)
        if dec:
            end_game()

# dealer - turn
while dealer[1] <= 16:
    card = draw_card(cards)
    dealer[0].append(card)
    # ace gives dealer 11 points if he does not overdraw and gives him 1 if he would overdraw otherwise
    if isinstance(card, Ace):
        if dealer[1] + 11 > 21:
            dealer[1] += 1
        else:
            dealer[1] += 11
    else:
        dealer[1] += card.__get_value__()
    if len(dealer[0]) == 2 and dealer[1] == 21:
        blackjack_dealer = True
        if insured:
            payout_insurance(insurance_lane, money)

print_score("Dealer", dealer)
print(dealer[1])

if dealer[1] > 21:  # dealer overdrew
    win(money, calculate_winning(bet, player))

elif dealer[1] > player[1]:  # dealer is closer to 21 then player
    lose(money)

elif player[1] > dealer[1]:  # player is closer to 21 then dealer
    win(money, calculate_winning(bet, player))

elif blackjack_player and not blackjack_dealer:
    win(money, calculate_winning(bet, player))

elif blackjack_dealer and not blackjack_player:
    lose(money)

elif blackjack_dealer and blackjack_player:
    draw(money, bet)

elif dealer[1] == player[1]:  # draw
    draw(money, bet)
