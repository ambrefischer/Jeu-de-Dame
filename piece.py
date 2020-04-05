# -*- coding: utf-8 -*-
"""
Project : Jeu de Dames

@authors: Ambre Fischer & Charles Fortier (groupe TD 2)
"""

from constants import *



class Piece():
    '''
    Cette classe décrit le comportement des pièces. La pièce sélectionnée par le joueur
    peut suivre le comportement d'un Checker (pion) ou d'un King (dame).
    '''

    def __init__(self, start_row, start_column, target_row, target_column, player_number):
        """
        Crée une pièce avec deux système de coordonnées et un numéro déterminant son camp.

        Paramètres
        ----------
        start_row, start_column: int
            Coordonnées de la pièce à jouer

        target_row, target_column: int
            Coordonnées de la case où se déplace la pièce.

        player_number: int
            Enregistre le numéro du joueur à qui elle appartient.
            Sur le plateau, les pions correspondent à player_number.
            Sur le plateau, les dames correspondent à player_number+0.5.
        """

        self.s_row = start_row
        self.s_column = start_column
        self.t_row = target_row
        self.t_column = target_column
        self.player_number = player_number


    def move(self, gameboard):
        """
        Déplace une pièce.

        Paramètres
        ----------
        gameboard: array
            Définit le plateau de jeu en cours.

        Renvoie
        -------
        gameboard: array
            Plateau modifié après avoir déplacé la pièce.
        """

        #La case cible prend le contenu de la case de départ: caractérise un déplacement.
        gameboard[self.t_row][self.t_column] = gameboard[self.s_row][self.s_column]
        #La case de départ devient une case vide.
        gameboard[self.s_row][self.s_column] = 0

        return gameboard





class Checker(Piece):
    '''Un pion ne peut se déplacer que d'une case en diagonale en avant (vers le haut pour joueur 2
    et vers le bas pour joueur 1).
    Un pion peut prendre un pion adverse dans n'importe quelle direction mais sur une case
    en diagonale voisine.
    Le pion peut devenir une dame lorsqu'il atteint la première ligne ennemie.
    '''

    def __init__(self, start_row, start_column, target_row, target_column, player_number):
        super().__init__(start_row, start_column, target_row, target_column, player_number)


    def capture(self, gameboard, make_a_move):
        """
        Simuler la prise de pièce adverse avec un pion.

        Paramètres
        ----------
        gameboard: array
            Définit le plateau de jeu en cours.

        make_a_move: dict
            Est définie par la méthode check_coords de la classe Player.
            Définit à travers la clé "target" l'emplacement de la pièce adverse.

        Renvoie
        -------
        gameboard: array
            Plateau modifié après avoir pris la pièce adverse.

        Note
        -------
        Elle ne simule pas le déplacement du pion mais juste la disparition de la pièce adverse.
        """

        #4 cas possibles:
        #En bas à droite
        if make_a_move["target"] == RIGHT_DOWN:
            gameboard[self.s_row+1][self.s_column+1] = 0
        #En bas à gauche
        elif make_a_move["target"] == LEFT_DOWN:
            gameboard[self.s_row+1][self.s_column-1] = 0
        #En haut à droite
        elif make_a_move["target"] == RIGHT_UP:
            gameboard[self.s_row-1][self.s_column+1] = 0
        #En haut à gauche
        else:
            gameboard[self.s_row-1][self.s_column-1] = 0

        return gameboard


    def check_king(self):
        """
        Cette fonction propre aux pions détermine si le pion est dans les conditions pour passer dame.

        Paramètres
        ----------
        Aucun

        Renvoie
        -------
        b: bool
            Renvoie un booléen indiquant si les conditions sont réunies.
        """

        # Si le joueur 1 arrive tout en bas
        if self.player_number == 1 and self.t_row == 9:
            return True
        # Si le joueur 2 arrive tout en haut
        elif self.player_number == 2 and self.t_row == 0:
            return True
        #Les conditions ne sont pas réunies.
        return False


    def become_king(self, gameboard):
        """
        Cette fonction propre aux pions transforme le pion en dame.

        Paramètres
        ----------
        gameboard: array
            Définit le plateau de jeu en cours.

        Renvoie
        -------
        gameboard: array
           Plateau modifié après avoir transformé un pion en dame.

        Note
        -------
        Le pion doit au préalable remplir les conditions de check_king.
        """

        gameboard[self.t_row][self.t_column] = self.player_number + 0.5
        return gameboard





class King(Piece):
    '''
    La dame peut aller en avant et en arrière en diagonale et peut se déplacer
    d'autant de cases qu'elle le désire.
    Une dame ne peut prendre qu'une pièce adverse lors d'un déplacement.
    '''

    def __init__(self, start_row, start_column, target_row, target_column, player_number):
        super().__init__(start_row, start_column, target_row, target_column, player_number)


    def capture(self, gameboard, make_a_move):
        """
       Simule la prise de pièce adverse avec une dame.

       Paramètres
       ----------
       gameboard: array
           Définit le plateau de jeu en cours.

       make_a_move: dict
           Est définie par la méthode check_coords de la classe Player.
           Définit à travers les clés "opponent_row" et "opponent_column"
                l'emplacement de la pièce adverse.

       Renvoie
       -------
       gameboard: array
           Renvoie le plateau modifié après avoir pris la pièce adverse.

        Note
        -------
        Elle ne simule pas le déplacement de la dame mais juste la disparition de la pièce adverse.
       """

        opponent_row = make_a_move["opponent_row"]
        opponent_col = make_a_move["opponent_col"]
        gameboard[opponent_row][opponent_col] = 0

        return gameboard
