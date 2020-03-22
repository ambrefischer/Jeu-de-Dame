# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:51:07 2020

@author: Ambre
"""
import numpy as np


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
    print("    1  2  3  4  5  6  7  8  9  10", "\n")
    """
    Better to write :
    for index in range(gameboard):
        print(index + 1,gameboard[index])
    """
    numero_ligne = 1
    for gameLine in gameboard:
        if numero_ligne < 10:
            print(numero_ligne, "", gameLine)
            numero_ligne += 1
        else:
            print(numero_ligne, gameLine)
