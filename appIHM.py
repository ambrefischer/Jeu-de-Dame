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


        # self.J1 = play_with()
        self.J1 = Human(1, 0, 2, 1)
        self.J2 = Human(2, 0, 1, -1)
        self.gamebord = create_gameboard(self.J1, self.J2)

        self.painter = QtGui.QPainter()
        self.ui.conteneur.paintEvent = self.draw_pieces
        self.launch_game


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
        self.painter.begin(self.ui.conteneur)
        qp = self.painter

        for player in [self.J1, self.J2]:
            piece = player.where_piece(self.gamebord)[0]
            if player == self.J1:
                image = QtGui.QImage("icons/pion_noir.png")
            else:
                image = QtGui.QImage("icons/pion_blanc.png")

            for key in piece.keys():

                if piece[key][1] == 0:
                    if piece[key][2] == 1:
                        qp.drawImage(51, 1, image)
                    elif piece[key][2] == 3:
                        qp.drawImage(152, 1, image)
                    elif piece[key][2] == 5:
                        qp.drawImage(253, 1, image)
                    elif piece[key][2] == 7:
                        qp.drawImage(354, 1, image)
                    qp.drawImage(454, 1, image)

                if piece[key][1] == 1:
                    if piece[key][2] == 2:
                        qp.drawImage(1, 52, image)
                    elif piece[key][2] == 4:
                        qp.drawImage(102, 52, image)
                    elif piece[key][2] == 6:
                        qp.drawImage(203, 52, image)
                    elif piece[key][2] == 8:
                        qp.drawImage(304, 52, image)
                    qp.drawImage(404, 52, image)

                if piece[key][1] == 2:
                    if piece[key][2] == 1:
                        qp.drawImage(51, 102, image)
                    elif piece[key][2] == 3:
                        qp.drawImage(152, 102, image)
                    elif piece[key][2] == 5:
                        qp.drawImage(253, 102, image)
                    elif piece[key][2] == 7:
                        qp.drawImage(354, 102, image)
                    qp.drawImage(454, 102, image)

                if piece[key][1] == 3:
                    if piece[key][2] == 2:
                        qp.drawImage(1, 153, image)
                    elif piece[key][2] == 4:
                        qp.drawImage(102, 153, image)
                    elif piece[key][2] == 6:
                        qp.drawImage(203, 153, image)
                    elif piece[key][2] == 8:
                        qp.drawImage(304, 153, image)
                    qp.drawImage(404, 153, image)

                if piece[key][1] == 4:
                    if piece[key][2] == 1:
                        qp.drawImage(51, 203, image)
                    elif piece[key][2] == 3:
                        qp.drawImage(152, 203, image)
                    elif piece[key][2] == 5:
                        qp.drawImage(253, 203, image)
                    elif piece[key][2] == 7:
                        qp.drawImage(354, 203, image)
                    qp.drawImage(454, 203, image)

                if piece[key][1] == 5:
                    if piece[key][2] == 2:
                        qp.drawImage(1, 254, image)
                    elif piece[key][2] == 4:
                        qp.drawImage(102, 254, image)
                    elif piece[key][2] == 6:
                        qp.drawImage(203, 254, image)
                    elif piece[key][2] == 8:
                        qp.drawImage(304, 254, image)
                    qp.drawImage(404, 254, image)

                if piece[key][1] == 6:
                    if piece[key][2] == 1:
                        qp.drawImage(51, 304, image)
                    elif piece[key][2] == 3:
                        qp.drawImage(152, 304, image)
                    elif piece[key][2] == 5:
                        qp.drawImage(253, 304, image)
                    elif piece[key][2] == 7:
                        qp.drawImage(354, 304, image)
                    qp.drawImage(454, 304, image)

                if piece[key][1] == 7:
                    if piece[key][2] == 2:
                        qp.drawImage(1, 354, image)
                    elif piece[key][2] == 4:
                        qp.drawImage(102, 354, image)
                    elif piece[key][2] == 6:
                        qp.drawImage(203, 354, image)
                    elif piece[key][2] == 8:
                        qp.drawImage(304, 354, image)
                    qp.drawImage(404, 354, image)

                if piece[key][1] == 8:
                    if piece[key][2] == 1:
                        qp.drawImage(51, 405, image)
                    elif piece[key][2] == 3:
                        qp.drawImage(152, 405, image)
                    elif piece[key][2] == 5:
                        qp.drawImage(253, 405, image)
                    elif piece[key][2] == 7:
                        qp.drawImage(354, 405, image)
                    qp.drawImage(454, 405, image)

                if piece[key][1] == 9:
                    if piece[key][2] == 2:
                        qp.drawImage(1, 455, image)
                    elif piece[key][2] == 4:
                        qp.drawImage(102, 455, image)
                    elif piece[key][2] == 6:
                        qp.drawImage(203, 455, image)
                    elif piece[key][2] == 8:
                        qp.drawImage(304, 455, image)
                    qp.drawImage(404, 455, image)

        self.painter.end()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MonAppli()
    window.show()
    app.exec_()