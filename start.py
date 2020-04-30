# -*- coding: utf-8 -*-
"""
Project : Jeu de Dames

@authors: Ambre Fischer & Charles Fortier (groupe TD 2)

Ce fichier est à faire tourner pour lancer le programme.
"""


from game import *
from appIHM import MonAppli, MonAppliCommencement
from PyQt5 import QtGui, QtCore, QtWidgets, uic
import sys




def letsplay():
    print("letsplay")
    play_turn(player_turn, J1, J2, gameboard, window2)
    view(gameboard)
    window2.gameboard = gameboard
    window2.conteneur.update()

    player_turn["player_number"] += 1



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    # window1 = MonAppliCommencement()
    # window1.show()
    # app.exec_()
    # window2 = MonAppli(window1.J1, window1.nickname)
    window2 = MonAppli(Human(1, 0, 2, 1), "ambre")

    J1 = window2.J1
    J2 = window2.J2

    initialisation = initialisation(J1, J2, window2)
    player_turn = initialisation["player_turn"]
    gameboard = initialisation["gameboard"]

    window2.bout_valider.clicked.connect(letsplay)

    window2.show()
    app.exec_()


    # Jeu
    # while J1.where_piece(gameboard)[1] != 0 and J2.where_piece(gameboard)[1] != 0:


    # Comdition de gagne
    # if J1.score < J2.score:
    #     display_message("Le joueur 2 a gagné.", "green")
    #     add_player(nickname, J2.score)
    # else:
    #     display_message("Le joueur 1 a gagné.", "blue")
    #     add_player(nickname, J1.score)
