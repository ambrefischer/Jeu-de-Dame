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
    gameboard = np.zeros((10,10))
    for k in range(4): 
        for j in range(10):
            if (k+j)%2 == 1:
                gameboard[k][j]=1
    for k in range(6,10):
        for j in range(10):
            if (k+j)%2 == 1:
                gameboard[k][j]=2
                
    return gameboard
        
        
def view(gameboard):
    print("\n", gameboard)