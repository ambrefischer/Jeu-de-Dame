# -*- coding: utf-8 -*-
"""
Project : Jeu de Dames

@authors: Ambre Fischer & Charles Fortier (groupe TD 2)
"""

import unittest
from piece import Piece, Checker, King
import numpy as np
from player import Player
from constants import *




class TestPiece (unittest.TestCase):
    """
    Cette classe permet de faire les tests unitaires sur les Pieces.
    """

    def testInit(self):
        '''
        Test de l'initialisaion
        '''

        pion = Piece(1,2,3,4,5)
        self.assertEqual(pion.s_row, 0)
        self.assertEqual(pion.s_column, 1)
        self.assertEqual(pion.t_row, 2)
        self.assertEqual(pion.t_column, 3)
        self.assertEqual(pion.player_number, 5)


    def testKing(self):
        '''
        Création d'une dame.
        Teste si la dame reste une dame après mouvement.
        '''

        joueur = Player(1,0,2,1)
        board = np.zeros((10,10))
        board[0][0] = 1.5
        dame = King(1,1,5,5,1)
        dame.move(board)
        self.assertEqual(board[4][4],1.5)
        self.assertEqual(board[0][0], 0)


    def testmove(self):
        '''
        Création de 2 pions.
        Teste le mouvement correct des 2 pions.
        '''

        tab = np.zeros((2,2))
        tab[0][0] = 1
        tab[1][1] = 2
        pion1 = Piece(1,1,1,2,1)
        pion2 = Piece(2,2,2,1,2)
        pion1.move(tab)
        pion2.move(tab)
        self.assertEqual(tab[0][0], 0)
        self.assertEqual(tab[0][1], 1)
        self.assertEqual(tab[1][1], 0)
        self.assertEqual(tab[1][0], 2)





class TestPlayer(unittest.TestCase):
    '''
    Ce Test permet de faire les tests unitaires sur les Joueurs.
    '''

    def testInit(self):
        '''
        Test de l'initialisaion
        '''

        joueur = Player(1,0,2,-1)
        self.assertEqual(joueur.number, 1)
        self.assertEqual(joueur.score, 0)
        self.assertEqual(joueur.opponent_number, 2)
        self.assertEqual(joueur.factor, -1)


    def testone_turn(self):
        '''
        Crétion d'un joueur.
        Test l'entrée de mauvaises coordonnées.
        '''

        joueur = Player(1,0,2,-1)
        self.assertEqual(joueur.one_turn(0,1,1,1,[]),{"message": PB})


    def testtake_checker(self):
        '''
        Création d'un joueur.
        Teste des mouvements possibles du joueur.
        '''

        joueur = Player(1,0,2,1)
        board = np.zeros((10,10))
        board[0][0] = 1
        #test du déplacement vers une case vide
        self.assertEqual(joueur.take_checker(0,0,1,1,board),{"message": I_M_ON_MY_WAY, "type": CHECKER})

        #test de la prise de pion en bas à droite
        board[1][1] = 2
        self.assertEqual(joueur.take_checker(0,0,2,2,board),{"message": I_CAPTURE, "target": RIGHT_DOWN, "type": CHECKER})

        #test de la prise de pion en bas à gauche
        board = np.zeros((10,10))
        board[0][2] = 1
        board[1][1] = 2
        self.assertEqual(joueur.take_checker(0,2,2,0,board),{"message": I_CAPTURE, "target": LEFT_DOWN, "type": CHECKER})
        
        #test des coordonnées erronnées
        self.assertEqual(joueur.take_checker(0,2,5,5,board), {"message": PB})


    def testwin_one_point(self):
        '''
        Création d'un joueur.
        Teste l'incrémentation d'un point au joueur.
        '''

        joueur = Player(1,3,2,1)
        joueur.win_one_point()
        self.assertEqual(joueur.score, 4)
         
    
        
        
        
        
        

if __name__ == "__main__":
    unittest.main()
