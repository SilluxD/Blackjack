from enum import Enum


class Color(Enum):
    clubs = "Kreuz"
    spades = "Pik"
    hearts = "Herz"
    diamonds = "Karo"


class Card:
    def __init__(self, name, color, value):
        self.name = name
        self.color = color
        self.value = value

    def __get_value__(self):
        return self.value

    def __get_color__(self):
        return self.color.value

    def __get_name__(self):
        return self.name

    def __to_string__(self):
        return self.color.value + " " + self.name


class Ace(Card):
    def __init__(self, color):
        Card.__init__(self, "Ass", color, 1)


class King(Card):
    def __init__(self, color):
        Card.__init__(self, "König", color, 10)


class Queen(Card):
    def __init__(self, color):
        Card.__init__(self, "Königin", color, 10)


class Joker(Card):
    def __init__(self, color):
        Card.__init__(self, "Bube", color, 10)


class Ten(Card):
    def __init__(self, color):
        Card.__init__(self, "Zehn", color, 10)


class Nine(Card):
    def __init__(self, color):
        Card.__init__(self, "Neun", color, 9)


class Eight(Card):
    def __init__(self, color):
        Card.__init__(self, "Acht", color, 8)


class Seven(Card):
    def __init__(self, color):
        Card.__init__(self, "Sieben", color, 7)


class Six(Card):
    def __init__(self, color):
        Card.__init__(self, "Sechs", color, 6)


class Five(Card):
    def __init__(self, color):
        Card.__init__(self, "Fünf", color, 5)


class Four(Card):
    def __init__(self, color):
        Card.__init__(self, "Vier", color, 4)


class Three(Card):
    def __init__(self, color):
        Card.__init__(self, "Drei", color, 3)


class Two(Card):
    def __init__(self, color):
        Card.__init__(self, "Zwei", color, 2)
