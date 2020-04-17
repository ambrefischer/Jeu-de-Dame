# -*- coding: utf-8 -*-
"""
Project : Jeu de Dames

@authors: Ambre Fischer & Charles Fortier (groupe TD 2)

Ce fichier est à faire tourner pour lancer le programme.
"""


from game import *
import numpy as np


if __name__ == "__main__":
    display_beginning()
    nickname = input("Veuillez indiquer un surnom : ")

    J1 = play_with()
    J2 = Human(2, 0, 1, -1)

    initialisation = initialisation(J1, J2)
    player_turn = initialisation["player_turn"]
    gameboard = initialisation["gameboard"]


    # Jeu
    while J1.score < 20 or J2.score < 20:
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
