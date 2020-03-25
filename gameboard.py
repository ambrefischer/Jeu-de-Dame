# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:51:07 2020

@author: Ambre
"""
import numpy as np
from utils import *



def create_gameboard(j1, j2):
    '''Création d'un plateau initial avec 20 pions du joueur 1
        et 20 pions du joueur 2. Les cases 0 représentent des cases vides.
        '''
    gameboard = np.zeros((10, 10))
    for k in range(4):
        for j in range(10):
            if (k+j) % 2 == 1:
                gameboard[k][j] = j1.number
    for k in range(6, 10):
        for j in range(10):
            if (k+j) % 2 == 1:
                gameboard[k][j] = j2.number

    return gameboard


def view(gameboard):
    print("\n" "    1  2  3  4  5  6  7  8  9  10", "\n")
    for index in range(10):
        if index != 9:
            print(index + 1, "", gameboard[index])
        else:
            print(index + 1, gameboard[index])


def out_of_bounds(s_row, s_column, t_row, t_column):
    if (s_row < 0 or s_row > 9) or (s_column < 0 or s_column > 9) or (t_row < 0 or t_row > 9) or (
            t_column < 0 or t_column > 9):
        display_message(
            "VEUILLEZ SAISIR DES COORDONNEES SUR LE PLATEAU.", "red")
        display_message("Allez, on recommence...", "black")
        return True
