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
        self.assertEqual(pion.s_row, 1)
        self.assertEqual(pion.s_column, 2)
        self.assertEqual(pion.t_row, 3)
        self.assertEqual(pion.t_column, 4)
        self.assertEqual(pion.player_number, 5)


    def testcheck_king(self):
        '''
        Teste si les conditions sont réunies pour qu'un pion devienne une dame.
        '''

        joueur = Player(1,0,2,1)
        board = np.zeros((10,10))
        board[8][8] = 1
        board[7][7] = 1
        pion1 = Checker(8,8,9,9,1)
        pion2 = Checker(7,7,8,8,1)
        self.assertEqual(pion1.check_king(),True)
        self.assertEqual(pion2.check_king(),False)

    def testbecome_king(self):
        '''
        Teste si le pion devient correctement une dame.
        '''
        joueur = Player(1,0,2,1)
        board = np.zeros((10,10))
        board[0][0] = 1
        pion1 = Checker(8,8,9,9,1)
        pion1.move(board)
        pion1.become_king(board)
        self.assertEqual(board[9][9],1.5)


    def testmove(self):
        '''
        Création de 2 pions.
        Teste le mouvement correct des 2 pions.
        '''

        tab = np.zeros((2,2))
        tab[0][0] = 1
        tab[0][1] = 2
        pion1 = Piece(0,0,1,1,1)
        pion2 = Piece(0,1,1,0,2)
        pion1.move(tab)
        pion2.move(tab)
        self.assertEqual(tab[0][0], 0)
        self.assertEqual(tab[0][1], 0)
        self.assertEqual(tab[1][1], 1)
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


    def testcheck_coords(self):
        '''
        Crétion d'un joueur.
        Test l'entrée de mauvaises coordonnées.
        '''

        joueur = Player(1,0,2,-1)
        self.assertEqual(joueur.check_coords(0,100,1,1,[]),{"message": PB})


    def testtake_checker(self):
        '''
        Création d'un joueur.
        Teste des mouvements possibles du joueur.
        '''

        joueur = Player(1,0,2,1)
        board = np.zeros((10,10))
        board[0][0] = 1
        #test du déplacement vers une case vide
        self.assertEqual(joueur.take_checker(0,0,1,1,board),{"message": I_M_ON_MY_WAY, "target": None, "type": CHECKER})

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


    def testtake_king(self):
        '''
        Création d'un joueur et d'une dame pour tester les différents déplacements.
        '''

        #Teste le simple déplacement.
        joueur = Player(1,0,2,1)
        board = np.zeros((10,10))
        board[0][0] = 1.5
        # on souhaite effectuer un déplacement avec une dame depuis la case [0,0] vers la case [7,7]
        dame = King(0,0,7,7,1)
        where_king = joueur.where_king(0,0,7,7)
        self.assertEqual(joueur.take_king(0,0,7,7,board,where_king),{"message": I_M_ON_MY_WAY, "target": None, "type": KING})

        #Teste les mauvaises coordonnées
        joueur = Player(1,0,2,1)
        board = np.zeros((10,10))
        board[0][0] = 1.5
        # on souhaite effectuer un déplacement avec une dame depuis la case [0,0] vers la case [3,7]
        dame = King(0,0,3,7,1)
        where_king = joueur.where_king(0,0,3,7)
        self.assertEqual(joueur.take_king(0,0,3,7,board,where_king),{"message": PB})

        #Teste la prise d'une seule pièce (située aux coordonnées [1,1] en un seul déplacement
        joueur = Player(1,0,2,1)
        board = np.zeros((10,10))
        board[0][0] = 1.5
        board[1][1] = 2
        # on souhaite effectuer un déplacement avec une dame depuis la case [0,0] vers la case [7,7]
        dame = King(0,0,7,7,1)
        where_king = joueur.where_king(0,0,7,7)
        self.assertEqual(joueur.take_king(0,0,7,7,board,where_king),{"message": I_CAPTURE, "target": where_king, "opponent_row": 1,
                        "opponent_col": 1, "type": KING})

        #Teste la prise de plusieurs pièces en un seul déplacement
        joueur = Player(1,0,2,1)
        board = np.zeros((10,10))
        board[0][0] = 1.5
        board[1][1] = 2
        board[2][2] = 2
        # on souhaite effectuer un déplacement avec une dame depuis la case [0,0] vers la case [7,7]
        dame = King(0,0,7,7,1)
        where_king = joueur.where_king(0,0,7,7)
        self.assertEqual(joueur.take_king(0,0,7,7,board,where_king),{"message": PB})
        


        
        

        
        
    
         
    
        
        
        
        
        

if __name__ == "__main__":
    unittest.main()
