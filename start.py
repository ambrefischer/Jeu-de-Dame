# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 15:00:30 2020

@author: Ambre
"""



from game import *
import numpy as np


if __name__ == "__main__":
    display_beginning()
    nickname = input("Veuillez indiquer un surnom : ")

    j1 = play_with()
    j2 = Human(2, 0, 1, -1)

    initialisation = initialisation(j1, j2)
    player_turn = initialisation["player_turn"]
    gameboard = initialisation["gameboard"]

    # Jeu
    while j1.score < 20 or j2.score < 20:
        play_turn(player_turn, j1, j2, gameboard)
        view(gameboard)
        player_turn["player_number"] += 1

    # Comdition de gagne
    if j1.score < j2.score:
        display_message("Le joueur 2 a gagné.", "green")
        add_player(nickname, j2.score)
    else:
        display_message("Le joueur 1 a gagné.", "blue")
        add_player(nickname, j1.score)
