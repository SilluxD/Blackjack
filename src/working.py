from itertools import islice
import random

from Blackjack.src.card import *


def end_game():
    exit()


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
            winning = 3 * bet / 2 + bet
        elif len(player[0]) == 2:  # blackjack 3:2
            winning = 3 * bet / 2 + bet
        else:
            winning = 2 * bet  # no special win with 21 points

    return winning


def lose(money):
    print("\nSie haben verloren \nGuthaben: " + str(money))
    end_game()


def draw(money, bet):
    money += bet
    print("\nSie haben unentschieden gespielt. Sie erhalten Ihren Einsatz zurück\nGuthaben:" + str(money))
    end_game()


def win(money, winnings):
    money = money + winnings
    print("\nSie haben gewonnen! Der Gewinn beträgt " + str(winnings))
    print("Guthaben: " + str(money))
    end_game()


# called when a player is insured and the dealer scores a blackjack
def payout_insurance(insurance_lane, money):
    print(
        "\nDer Dealer hatte einen Blackjack. Sie erhalten Ihre Versicherungsprämie, da sie gegen den "
        "Blackjack versichert sind.")
    money += insurance_lane * 2
    print("Guthaben: " + str(money))
    end_game()


# player has the option to insure himself with an amount he can specify himself.
# This amount is subtracted from his money
def ask_insurance(money):
    while not money == 0:
        decision = input(
            "Der Dealer hat ein Ass gelegt. Wollen Sie sich gegen einen Blackjack versichern? [y/n]").lower()
        if not (decision == "n" or decision == "y"):
            continue
        if decision == "n":
            return False, 0
        if decision == "y":
            while True:
                amount = input("Wieviel möchten Sie in die Versicherung einzahlen? (Abbruch: [n])")
                if amount == "n":
                    return False, 0
                if not amount.isnumeric():
                    continue
                else:
                    amount = int(amount)
                    if amount > money or amount == 0:
                        continue
                    money -= amount
                    return True, amount
    return False, 0


def payout_option(bet, money, insurance_lane):
    while True:
        decision = input(
            "Sie haben einen Blackjack und der Dealer hat ein Ass. Wollen Sie ihren Einsatz und eventuell "
            "gezahlte Versicherungsbeiträge zurückerhalten? [y/n]").lower()
        if not (decision == "y" or decision == "n"):
            continue
        if decision == "n":
            return False, money
        if decision == "y":
            money += bet + insurance_lane
            return True, money


def surrender(money):
    print("Sie haben aufgegeben und die Hälfte des Einsatzes zurückbekommen.\nGuthaben:" + str(money))
    end_game()


def ask_surrender():
    while True:
        decision = input("Sie haben die Möglichkeit aufzugeben. [y/n]")
        if not (decision == "y" or decision == "n"):
            continue
        if decision == "n":
            return False
        if decision == "y":
            return True
