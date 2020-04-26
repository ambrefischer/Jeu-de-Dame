import sys
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from game import *


class MonAppli(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('interface.ui', self)

        pixmap = QtGui.QPixmap("icons/fond_gameboard.png")
        pal = QtGui.QPalette()
        pal.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.ui.conteneur.lower()
        self.ui.conteneur.stackUnder(self)
        self.ui.conteneur.setAutoFillBackground(True)
        self.ui.conteneur.setPalette(pal)

        self.painter = QtGui.QPainter()


        # self.J1 = play_with()
        self.J1 = Human(1, 0, 2, 1)
        self.J2 = Human(2, 0, 1, -1)
        self.gamebord = create_gameboard(self.J1, self.J2)

        self.ui.conteneur.paintEvent = self.draw_pieces


    def launch_game(self, *args):
        display_beginning()
        nickname = input("Veuillez indiquer un surnom : ")

        init = initialisation(self.J1, self.J2)
        player_turn = init["player_turn"]

        # Jeu
        while self.J1.where_piece(self.gameboard)[1] != 0 and self.J2.where_piece(self.gameboard)[1] != 0:
            play_turn(player_turn, self.J1, self.J2, self.gameboard)
            view(self.gameboard)
            self.draw_pieces
            player_turn["player_number"] += 1

        # Comdition de gagne
        if self.J1.score < self.J2.score:
            display_message("Le joueur 2 a gagné.", "green")
            add_player(nickname, self.J2.score)
        else:
            display_message("Le joueur 1 a gagné.", "blue")
            add_player(nickname, self.J1.score)


    def draw_pieces(self, *args):
        # on informe le peintre qu'on veut dessiner dans le widget conteneur
        self.painter.begin(self.ui.conteneur)
        # variable intermédiraire pour alléger le code
        qp = self.painter
        # boucle pour parcourir les insectes et gérer les images (vu ci-dessus)
        print(self.J1)
        print(self.J1.where_piece(self.gamebord))
        # for pieces in self.J1.where_piece(self.gameboard):
        #     image = QtGui.QImage("icons/pion_noir.png")
        #     qp.drawImage(pieces[1], pieces[2], image)
        #
        # for pieces in self.J2.where_piece(self.gameboard):
        #     image = QtGui.QImage("icons/pion_blanc.png")
        #     qp.drawImage(pieces[1], pieces[2], image)

        self.painter.end()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MonAppli()
    window.show()
    app.exec_()