from Blackjack.working import *

money = 500
blackjack_player, blackjack_dealer = False, False

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
        if decision == "n":
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

    # player loses if busted
    if player[1] > 21:
        lose(money)

else:  # blackjack
    player[1] = 21
    player[2] = 0
    blackjack_player = True

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

print_score("Dealer", dealer)
print(dealer[1])

if dealer[1] > 21:  # dealer overdrew
    win(money, calculate_winning(bet, player))

elif dealer[1] > player[1]:  # dealer is closer to 21 then player
    lose(money)

elif player[1] > dealer[1]:  # player is closer to 21 then dealer
    win(money, calculate_winning(bet, player))

elif dealer[1] == player[1]:  # draw
    draw(money, bet)
