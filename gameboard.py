# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:51:07 2020

@author: Ambre
"""
import numpy as np

"""
Remarques Amaury dans create_gameboard, tu devrais injecter j1 j2, et utiliser j1.number et j2.number plutot que marquer 1 et 2,
des fois que t'auraix envie de changer 1 ou 2 par X et Y faut que ton code puisse fonctionner :)
cf la remarque dans take_king de player.py
"""


def create_gameboard():
    '''Création d'un plateau initial avec 20 pions du joueur 1
        et 20 pions du joueur 2. Les cases 0 représentent des cases vides.
        '''
    gameboard = np.zeros((10, 10))
    for k in range(4):
        for j in range(10):
            if (k+j) % 2 == 1:
                gameboard[k][j] = 1
    for k in range(6, 10):
        for j in range(10):
            if (k+j) % 2 == 1:
                gameboard[k][j] = 2

    return gameboard


def view(gameboard):
    print("\n" "    1  2  3  4  5  6  7  8  9  10", "\n")
    for index in range(10):
        if index != 9:
            print(index + 1, "", gameboard[index])
        else:
            print(index + 1, gameboard[index])
