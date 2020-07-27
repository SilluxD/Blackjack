import unittest

from Blackjack.src.working import *


class DeckTest(unittest.TestCase):

    def test_generating_0(self):
        cards = shuffled_deck(0)

        self.assertEqual(len(cards), 0)

    def test_generating_1(self):
        cards = shuffled_deck(1)

        self.assertEqual(len(cards), 52)

    def test_generating_2(self):
        cards = shuffled_deck(2)

        self.assertEqual(len(cards), 104)

    def test_drawing_from_deck_removes_card(self):
        cards = shuffled_deck(1)
        before = len(cards)

        draw_card(cards)

        self.assertEqual(len(cards), before - 1)


class CalculationTest(unittest.TestCase):

    def test_calculate_ace_as_1(self):
        player = [[], 20, 1]

        points = calculate_max_points(player)

        self.assertEqual(points, 20)

    def test_calculate_ace_as_11(self):
        player = [[], 10, 1]

        points = calculate_max_points(player)

        self.assertEqual(points, 20)

    def test_calculate_ace_as_1_and_another_as_11(self):
        player = [[], 3, 3]

        points = calculate_max_points(player)

        self.assertEqual(points, 13)

    def test_calculate_winnings_normal(self):
        player = [[], 20, 0]

        money = calculate_winning(100, player)

        self.assertEqual(money, 200)

    def test_calculate_winnings_triple_seven(self):
        player = [[Seven(Color.clubs), Seven(Color.clubs), Seven(Color.clubs)], 21, 0]

        money = calculate_winning(100, player)

        self.assertEqual(money, 250)

    def test_calculate_winning_blackjack(self):
        player = [[Ace(Color.clubs), King(Color.clubs)], 21, 0]

        winnings = calculate_winning(100, player)

        self.assertEqual(winnings, 250)

    def test_21_points_but_no_special_calculates_normal_winning_amount(self):
        player = [[Two(Color.hearts), Two(Color.hearts), Nine(Color.spades), Ace(Color.diamonds), Seven(Color.spades)],
                  21, 0]

        winnings = calculate_winning(50, player)

        self.assertEqual(winnings, 100)


if __name__ == '__main__':
    unittest.main()
