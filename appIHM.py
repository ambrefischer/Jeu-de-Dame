import sys
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from game import *


class MonAppliCommencement(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui1 = uic.loadUi('begin_interface.ui', self)
        self.ui1.check_joueur.stateChanged.connect(self.play_with_human)
        self.ui1.check_ordi_facile.stateChanged.connect(self.play_with_IA)
        self.ui1.bout_continuer.clicked.connect(self.get_nickname)



    def play_with_human(self):
        self.J1 = Human(1, 0, 2, 1)

    def play_with_IA(self):
        self.J1 = IA(1,0,2,1,"facile")


    def get_nickname(self):
        self.nickname = self.ui1.edit_surnom.toPlainText()
        self.ui1.close()




class MonAppli(QtWidgets.QMainWindow):
    def __init__(self, J1, nickname):
        super().__init__()
        self.ui = uic.loadUi('interface.ui', self)
        pixmap = QtGui.QPixmap("icons/fond_gameboard.png")
        pal = QtGui.QPalette()
        pal.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.ui.conteneur.lower()
        self.ui.conteneur.stackUnder(self)
        self.ui.conteneur.setAutoFillBackground(True)
        self.ui.conteneur.setPalette(pal)

        self.nickname = nickname
        self.J1 = J1
        self.J2 = Human(2, 0, 1, -1)
        self.gameboard = create_gameboard(self.J1, self.J2)



        self.painter = QtGui.QPainter()
        self.ui.conteneur.paintEvent = self.draw_pieces

        self.mousePressEvent

        self.row = []
        self.column = []
        # self.textBrowser.setText()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            print(x,y)
            if len(self.row) == 2:
                self.row = []
                self.column = []

            if y > 30 and y < 80:
                self.row.append(0)
                if x > 63 and x < 110:
                    self.column.append(1)
                elif x > 163 and x < 210:
                    self.column.append(3)
                elif x > 263 and x < 310:
                    self.column.append(5)
                elif x > 363 and x < 410:
                    self.column.append(7)
                elif x > 463 and x < 510:
                    self.column.append(9)

            elif y > 80 and y < 130:
                self.row.append(1)
                if x > 12 and x < 60:
                    self.column.append(0)
                elif x > 112 and x < 160:
                    self.column.append(2)
                elif x > 212 and x < 260:
                    self.column.append(4)
                elif x > 312 and x < 360:
                    self.column.append(6)
                elif x > 412 and x < 460:
                    self.column.append(8)

            elif y > 130 and y < 180:
                self.row.append(2)
                if x > 63 and x < 110:
                    self.column.append(1)
                elif x > 163 and x < 210:
                    self.column.append(3)
                elif x > 263 and x < 310:
                    self.column.append(5)
                elif x > 363 and x < 410:
                    self.column.append(7)
                elif x > 463 and x < 510:
                    self.column.append(9)

            elif y > 180 and y < 230:
                self.row.append(3)
                if x > 12 and x < 60:
                    self.column.append(0)
                elif x > 112 and x < 160:
                    self.column.append(2)
                elif x > 212 and x < 260:
                    self.column.append(4)
                elif x > 312 and x < 360:
                    self.column.append(6)
                elif x > 412 and x < 460:
                    self.column.append(8)

            elif y > 230 and y < 280:
                self.row.append(4)
                if x > 63 and x < 110:
                    self.column.append(1)
                elif x > 163 and x < 210:
                    self.column.append(3)
                elif x > 263 and x < 310:
                    self.column.append(5)
                elif x > 363 and x < 410:
                    self.column.append(7)
                elif x > 463 and x < 510:
                    self.column.append(9)

            elif y > 280 and y < 330:
                self.row.append(5)
                if x > 12 and x < 60:
                    self.column.append(0)
                elif x > 112 and x < 160:
                    self.column.append(2)
                elif x > 212 and x < 260:
                    self.column.append(4)
                elif x > 312 and x < 360:
                    self.column.append(6)
                elif x > 412 and x < 460:
                    self.column.append(8)

            elif y > 330 and y < 380:
                self.row.append(6)
                if x > 63 and x < 110:
                    self.column.append(1)
                elif x > 163 and x < 210:
                    self.column.append(3)
                elif x > 263 and x < 310:
                    self.column.append(5)
                elif x > 363 and x < 410:
                    self.column.append(7)
                elif x > 463 and x < 510:
                    self.column.append(9)

            elif y > 380 and y < 430:
                self.row.append(7)
                if x > 12 and x < 60:
                    self.column.append(0)
                elif x > 112 and x < 160:
                    self.column.append(2)
                elif x > 212 and x < 260:
                    self.column.append(4)
                elif x > 312 and x < 360:
                    self.column.append(6)
                elif x > 412 and x < 460:
                    self.column.append(8)

            elif y > 430 and y < 480:
                self.row.append(8)
                if x > 63 and x < 110:
                    self.column.append(1)
                elif x > 163 and x < 210:
                    self.column.append(3)
                elif x > 263 and x < 310:
                    self.column.append(5)
                elif x > 363 and x < 410:
                    self.column.append(7)
                elif x > 463 and x < 510:
                    self.column.append(9)

            elif y > 480 and y < 530:
                self.row.append(9)
                if x > 12 and x < 60:
                    self.column.append(0)
                elif x > 112 and x < 160:
                    self.column.append(2)
                elif x > 212 and x < 260:
                    self.column.append(4)
                elif x > 312 and x < 360:
                    self.column.append(6)
                elif x > 412 and x < 460:
                    self.column.append(8)


            print(self.row, self.column)



    def draw_pieces(self, *args):
        self.painter.begin(self.ui.conteneur)
        qp = self.painter
        for player in [self.J1, self.J2]:
            piece = player.where_piece(self.gameboard)[0]
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
                    else:
                        qp.drawImage(454, 1, image)

                if piece[key][1] == 1:
                    if piece[key][2] == 0:
                        qp.drawImage(1, 52, image)
                    elif piece[key][2] == 2:
                        qp.drawImage(102, 52, image)
                    elif piece[key][2] == 4:
                        qp.drawImage(203, 52, image)
                    elif piece[key][2] == 6:
                        qp.drawImage(304, 52, image)
                    else:
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
                    else:
                        qp.drawImage(454, 102, image)

                if piece[key][1] == 3:
                    if piece[key][2] == 0:
                        qp.drawImage(1, 153, image)
                    elif piece[key][2] == 2:
                        qp.drawImage(102, 153, image)
                    elif piece[key][2] == 4:
                        qp.drawImage(203, 153, image)
                    elif piece[key][2] == 6:
                        qp.drawImage(304, 153, image)
                    else:
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
                    else :
                        qp.drawImage(454, 203, image)

                if piece[key][1] == 5:
                    if piece[key][2] == 0:
                        qp.drawImage(1, 254, image)
                    elif piece[key][2] == 2:
                        qp.drawImage(102, 254, image)
                    elif piece[key][2] == 4:
                        qp.drawImage(203, 254, image)
                    elif piece[key][2] == 6:
                        qp.drawImage(304, 254, image)
                    else :
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
                    else :
                        qp.drawImage(454, 304, image)

                if piece[key][1] == 7:
                    if piece[key][2] == 0:
                        qp.drawImage(1, 354, image)
                    elif piece[key][2] == 2:
                        qp.drawImage(102, 354, image)
                    elif piece[key][2] == 4:
                        qp.drawImage(203, 354, image)
                    elif piece[key][2] == 6:
                        qp.drawImage(304, 354, image)
                    else :
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
                    else :
                        qp.drawImage(454, 405, image)

                if piece[key][1] == 9:
                    if piece[key][2] == 0:
                        qp.drawImage(1, 455, image)
                    elif piece[key][2] == 2:
                        qp.drawImage(102, 455, image)
                    elif piece[key][2] == 4:
                        qp.drawImage(203, 455, image)
                    elif piece[key][2] == 6:
                        qp.drawImage(304, 455, image)
                    else :
                        qp.drawImage(404, 455, image)

        self.painter.end()
        # self.ui.conteneur.update()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # window1 = MonAppliCommencement()
    # window1.show()
    # app.exec_()
    # window2 = MonAppli(window1.J1, window1.nickname)
    window2 = MonAppli(Human(1,0,2,1), "ambre")
    window2.show()
    app.exec_()