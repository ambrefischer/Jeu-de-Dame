# -*- coding: utf-8 -*-
"""
Project : Jeu de Dames

@authors: Ambre Fischer & Charles Fortier (groupe TD 2)
"""

import numpy as np
from utils import *


# def create_gameboard(J1, J2):
#     gameboard = np.zeros((10,10))
#     for i in range(10):
#         for j in range(10):
#             gameboard[i][j] = 2
#     return gameboard

def create_gameboard(J1, J2):
    """
    Création d'un plateau initial avec 20 pions du joueur 1
    et 20 pions du joueur 2. Les cases 0 représentent des cases vides.

    Paramètres
    ----------
    J1, J2: player.Human
        Contient le numéro des joueurs.

    Renvoie
    ----------
    gameboard: array
        Définit le plateau initial.
    """

    gameboard = np.zeros((10, 10))
    for k in range(4):
        for j in range(10):
            if (k+j) % 2 == 1:
                gameboard[k][j] = J1.number
    for k in range(6, 10):
        for j in range(10):
            if (k+j) % 2 == 1:
                gameboard[k][j] = J2.number
    return gameboard



def view(gameboard):
    """
    Permet de visualiser le plateau sur le Shell.

    Paramètres
    ----------
    gameboard: array
        Définit le plateau en cours de jeu.
    """

    print("\n" "    1  2  3  4  5  6  7  8  9  10", "\n")
    for index in range(10):
        if index != 9:
            print(index + 1, "", gameboard[index])
        else:
            print(index + 1, gameboard[index])


def out_of_bounds(s_row, s_column, t_row, t_column):
    """
    Détermine si les coordonnées entrées par le joueur ne dépassent pas les limites du plateau.

    Paramètres
    ----------
    s_row, s_column: int
        Coordonnées de la pièce à jouer

    t_row, t_column: int
        Coordonnées de la case où se déplace la pièce.

    Renvoie
    ----------
    b: bool
    """

    if (s_row < 0 or s_row > 9) or (s_column < 0 or s_column > 9) or (t_row < 0 or t_row > 9) or (
            t_column < 0 or t_column > 9):
        display_message(
            "VEUILLEZ SAISIR DES COORDONNEES SUR LE PLATEAU.", "red")
        display_message("Allez, on recommence...", "black")
        return True


def out_of_bounds2(coords):
    if coords[0]<1 or coords[0]>9 or coords[1]<0 or coords[1]>9:
        return True
    else:
        return False
