# -*- coding: utf-8 -*-
"""
Project : Jeu de Dames

@authors: Ambre Fischer & Charles Fortier (groupe TD 2)

Ce fichier est à faire tourner pour lancer le programme.
"""


from game import *
from appIHM import MonAppli
from PyQt5 import QtGui, QtCore, QtWidgets, uic
import sys


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    # window1 = MonAppliCommencement()
    # window1.show()
    # app.exec_()
    # window2 = MonAppli(window1.J1, window1.nickname)
    window2 = MonAppli(Human(1, 0, 2, 1), "ambre")
    window2.show()
    app.exec_()

    J1 = window2.J1
    J2 = window2.J2

    initialisation = initialisation(J1, J2)
    player_turn = initialisation["player_turn"]
    gameboard = initialisation["gameboard"]


    # Jeu
    while J1.where_piece(gameboard)[1] != 0 and J2.where_piece(gameboard)[1] != 0:
        play_turn(player_turn, J1, J2, gameboard)
        view(gameboard)
        player_turn["player_number"] += 1

    # Comdition de gagne
    if J1.score < J2.score:
        display_message("Le joueur 2 a gagné.", "green")
        add_player(nickname, J2.score)
    else:
        display_message("Le joueur 1 a gagné.", "blue")
        add_player(nickname, J1.score)
