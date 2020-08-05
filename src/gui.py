from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QInputDialog, QMainWindow, QMessageBox

from Blackjack.src.game import Game

font = QFont("Arial", 10)


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.onlyInt = QIntValidator()
        self.game = None
        self.MainWindow = QtWidgets.QMainWindow()
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.quit_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_game_button = QtWidgets.QPushButton(self.centralwidget)
        self.dealer_text_area = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.dealer_text_area.setFont(font)
        self.player_text_area = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.player_text_area.setFont(font)
        self.label_player = QtWidgets.QLabel(self.centralwidget)
        self.label_dealer = QtWidgets.QLabel(self.centralwidget)
        self.label_money = QtWidgets.QLabel(self.centralwidget)
        self.label_bet = QtWidgets.QLabel(self.centralwidget)
        self.label_insurance = QtWidgets.QLabel(self.centralwidget)
        self.label_bust_bet = QtWidgets.QLabel(self.centralwidget)
        self.pass_button = QtWidgets.QPushButton(self.centralwidget)
        self.draw_button = QtWidgets.QPushButton(self.centralwidget)
        self.bet_input = QtWidgets.QLineEdit(self.centralwidget)
        self.bet_button = QtWidgets.QPushButton(self.centralwidget)

        self.setupUi()

    def setupUi(self):
        """Places items in the GUI.
        """
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(731, 523)
        self.centralwidget.setObjectName("centralwidget")
        # draw button
        self.draw_button.setEnabled(False)
        self.draw_button.setGeometry(QtCore.QRect(610, 30, 75, 23))
        self.draw_button.setObjectName("draw_button")
        # pass button
        self.pass_button.setEnabled(False)
        self.pass_button.setGeometry(QtCore.QRect(610, 60, 75, 23))
        self.pass_button.setObjectName("pass_button")
        # dealer text
        self.label_dealer.setGeometry(QtCore.QRect(40, 70, 51, 21))
        self.label_dealer.setObjectName("label_dealer")
        # money text
        self.label_money.setGeometry(QtCore.QRect(40, 20, 100, 20))
        self.label_money.setObjectName("label_money")
        # bet text
        self.label_bet.setGeometry(QtCore.QRect(40, 35, 100, 21))
        self.label_bet.setObjectName("label_bet")
        # insurance text
        self.label_insurance.setGeometry(QtCore.QRect(140, 20, 100, 21))
        self.label_insurance.setObjectName("label_insurance")
        # bust bet text
        self.label_bust_bet.setGeometry(QtCore.QRect(140, 35, 100, 21))
        self.label_bust_bet.setObjectName("label_bust_bet")
        # player text
        self.label_player.setGeometry(QtCore.QRect(40, 250, 51, 20))
        self.label_player.setObjectName("label_player")
        # player text area
        self.player_text_area.setGeometry(QtCore.QRect(110, 250, 261, 151))
        self.player_text_area.setReadOnly(True)
        self.player_text_area.setObjectName("player_text_area")
        # dealer text area
        self.dealer_text_area.setGeometry(QtCore.QRect(110, 80, 261, 121))
        self.dealer_text_area.setReadOnly(True)
        self.dealer_text_area.setObjectName("dealer_text_area")
        # quit button
        self.quit_button.setGeometry(QtCore.QRect(620, 450, 75, 23))
        self.quit_button.setObjectName("quit_button")
        # next game button
        self.next_game_button.setGeometry(QtCore.QRect(550, 450, 75, 23))
        self.next_game_button.setObjectName("next_game_button")
        self.next_game_button.setEnabled(False)
        # bet button and input
        self.bet_button.setGeometry(500, 60, 75, 23)
        self.bet_button.setObjectName("bet_button")
        self.bet_input.setGeometry(500, 30, 75, 23)
        self.bet_input.setPlaceholderText("Wetteinsatz:")
        self.bet_input.setValidator(self.onlyInt)

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 731, 20))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self, MainWindow):
        """Connects GUI elements with functions and sets text to the elements.
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Blackjack"))
        self.draw_button.setText(_translate("MainWindow", "Karte ziehen"))
        self.pass_button.setText(_translate("MainWindow", "Zug beenden"))
        self.label_dealer.setText(_translate("MainWindow", "Dealer:"))
        self.label_player.setText(_translate("MainWindow", "Spieler:"))
        self.label_money.setText(_translate("MainWindow", "Guthaben: "))
        self.label_bet.setText(_translate("MainWindow", "Einsatz: "))
        self.label_insurance.setText(_translate("MainWindow", "Einsatz: "))

        self.quit_button.setText(_translate("MainWindow", "Beenden"))
        self.bet_button.setText(_translate("MainWindow", "Start"))
        self.next_game_button.setText(_translate("MainWindow", "Neues Spiel"))

        self.quit_button.clicked.connect(self.quit_clicked)
        self.draw_button.clicked.connect(self.draw_clicked)
        self.pass_button.clicked.connect(self.pass_clicked)
        self.bet_button.clicked.connect(self.start_clicked)
        self.next_game_button.clicked.connect(self.next_game_clicked)
        self.bet_input.returnPressed.connect(self.start_clicked)

        self.MainWindow.show()

    def reset_ui(self):
        """Called when restarting the game. Resets GUI elements to a state where the game is playable.
        """
        self.next_game_button.setEnabled(False)
        self.activate_buttons()
        self.player_text_area.clear()
        self.dealer_text_area.clear()

    def ask_bust_bet(self):
        """Shows an input dialog for user input. Calls the method to bet on bust in the game.
        """
        text = "Sie haben die Möglichkeit darauf zu wetten, dass sich der Dealer überkauft." \
               "\nGeben Sie einen Betrag ein, wenn Sie darauf wetten möchten:"
        num, ok = QInputDialog.getInt(self, "Eingabe:", text, 50, 1, 100000, 10)

        if ok:
            self.game.bust(num)

    def ask_insurance(self):
        """Shows an input dialog for user input. Calls the method to insure a player in the game.
        """
        text = "Der Dealer hat ein Ass. Sie können sich gegen einen Blackjack versichern. " \
               "\nGeben Sie einen Betrag ein, wenn Sie sich versichern möchten:"
        num, ok = QInputDialog.getInt(self, "Eingabe:", text, 50, 1, 100000, 10)

        if ok:
            self.game.insure(num)

    def ask_surrender(self):
        """Shows input dialog for accepting or rejecting to surrender the game.
                Calls the specific function in the game if the player wants to do so."""
        button_reply = QMessageBox.question(self, 'Aufgeben', "Möchten Sie aufgeben?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if button_reply == QMessageBox.Yes:
            self.game.surrender()

    def ask_double_down(self):
        """Shows input dialog for accepting or rejecting to double down.
        Calls the specific function in the game if the player wants to do so."""
        button_reply = QMessageBox.question(self, 'Verdoppeln', "Wollen Sie Ihren Einsatz verdoppeln?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if button_reply == QMessageBox.Yes:
            self.game.double_down()

    def set_game(self, game):
        self.game = game

    def quit_clicked(self):
        sys.exit(app.exec_())

    def draw_clicked(self):
        self.game.draw()

    def next_game_clicked(self):
        self.game.next_game()
        self.reset_ui()

    def start_clicked(self):
        input_amount = self.bet_input.text()
        if not input_amount == "":
            self.game.start(int(input_amount))

    def pass_clicked(self):
        self.draw_button.setEnabled(False)
        self.pass_button.setEnabled(False)
        self.game.pass_turn(False)

    def update_cards(self, n, cards):
        """Prints cards for a participant in the corresponding text area.

        :param n: indicates which text area. 0 for dealer, 1 for player.
        :param cards: list of cards to be displayed
        """
        strg = "\n".join(c.__to_string__() for c in cards)

        if n == 0:
            self.dealer_text_area.setPlainText(strg)
        elif n == 1:
            self.player_text_area.setPlainText(strg)

    def add_text_to_textfield(self, n, text):
        """Appends text for a participant in the corresponding text area.

        :param n: indicates which text area. 0 for dealer, 1 for player.
        :param text: text to be added to the text area.
        """
        if n == 0:
            self.dealer_text_area.appendPlainText(text)
        elif n == 1:
            self.player_text_area.appendPlainText(text)

    def print_money(self, money, bet, insurance, bust_bet):
        """Displays bet and money.

        :param money: current money, the player has.
        :param bet: current bet in the game.
        :param insurance: current amount the player insured himself with.
        :param bust_bet: the amout the player bet on the dealer busting (overdrawing)
        """
        self.label_bet.setText("Einsatz: " + str(bet))
        self.label_money.setText("Guthaben: " + str(money))
        self.label_insurance.setText("Versichert: " + str(insurance))
        self.label_bust_bet.setText("Bust Wette: " + str(bust_bet))

    def deactivate_buttons(self):
        self.deactivate_draw()
        self.deactivate_pass()
        self.deactivate_bet()

    def activate_buttons(self):
        self.activate_draw()
        self.activate_pass()
        self.activate_bet()

    def deactivate_pass(self):
        self.pass_button.setEnabled(False)

    def activate_pass(self):
        self.pass_button.setEnabled(True)

    def deactivate_draw(self):
        self.draw_button.setEnabled(False)

    def activate_draw(self):
        self.draw_button.setEnabled(True)

    def deactivate_bet(self):
        self.bet_button.setEnabled(False)
        self.bet_input.setEnabled(False)

    def activate_bet(self):
        self.bet_button.setEnabled(True)
        self.bet_input.setEnabled(True)

    def activate_next_button(self):
        self.next_game_button.setEnabled(True)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()

    game = Game(ui)
    ui.set_game(game)
    sys.exit(app.exec_())
