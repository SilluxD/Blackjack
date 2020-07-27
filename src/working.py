from itertools import islice
import random

from Blackjack.src.card import *


def shuffled_deck(number):
    cards = []
    for i in range(number):
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


def draw_card(deck):
    return deck.pop()


def print_score(strg, data):
    print("\n" + strg + ":")
    print_deck(data[0])
    # print(data[1])


def print_deck(deck):
    for c in deck:
        print(c.__to_string__())


def calculate_max_points(player):
    copy = player.copy()
    while copy[2] > 0:
        if copy[1] + 10 <= 21:
            copy[1] += 10
            copy[2] -= 1
        else:
            copy[2] = 0

    return copy[1]


def calculate_winning(bet, player):
    winning = 0
    if player[1] < 21:  # normal win 2:1
        winning = 2 * bet
    elif player[1] == 21:
        if len(player[0]) == 3 and all(c.__get_value__() == 7 for c in player[0]):  # 777 win 3:2
            winning = 3 * bet / 2
        elif len(player[0]) == 2:  # blackjack
            winning = 3 * bet / 2

    return winning


def lose(money):
    print("\nSie haben verloren \nGuthaben: " + str(money))
    exit()


def draw(money, bet):
    money += bet
    print("\nSie haben unentschieden gespielt. Sie erhalten Ihren Einsatz zurück\nGuthaben:" + money)
    exit()


def win(money, winnings):
    money = money + winnings
    print("\nSie haben gewonnen! Der Gewinn beträgt " + str(winnings))
    print("Guthaben: " + str(money))
    exit()
