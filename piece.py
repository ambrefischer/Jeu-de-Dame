# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:50:58 2020

@author: Ambre
"""


class Piece():
    def __init__(self, start_row, start_column, target_row, target_column, player_number):
        self.s_row = start_row - 1
        self.s_column = start_column - 1
        self.t_row = target_row - 1
        self.t_column = target_column - 1
        self.player_number = player_number

    # Déplacement d'une pièce
    def move(self, gameboard):
        gameboard[self.s_row][self.s_column] = 0
        gameboard[self.t_row][self.t_column] = self.player_number

        return gameboard


class Checker(Piece):
    def __init__(self, start_row, start_column, target_row, target_column, player_number):
        super().__init__(start_row, start_column, target_row, target_column, player_number)

    # Effacement du pion adverse

    def capture(self, gameboard, make_a_move):
        if make_a_move["target"] == "right - down":
            gameboard[self.s_row+1][self.t_column+1] = 0
        elif make_a_move["target"] == "left - down":
            gameboard[self.t_row+1][self.t_column-1] = 0
        elif make_a_move["target"] == "right - up":
            gameboard[self.t_row-1][self.t_column+1] = 0
        else:
            gameboard[self.t_row-1][self.t_column-1] = 0

        return gameboard

    def check_king(self):
        # Si le joueur 1 arrive tout en bas
        if self.player_number == 1 and self.t_row == 9:
            return True
        # Si le joueur 2 arrive tout en haut
        elif self.player_number == 2 and self.t_row == 0:
            return True

        else:
            return False

    def become_king(self, gameboard):
        # Modification du pion du joueur 1 en dame
        if int(gameboard[self.t_row][self.t_column]) == 1:
            gameboard[self.t_row][self.t_column] = 1.5
        # Modification du pion du joueur 2 en dame
        elif int(gameboard[self.t_row][self.t_column]) == 2:
            gameboard[self.t_row][self.t_column] = 2.5

        return gameboard


class King(Piece):
    '''La dame peut aller d'avant en arrière et peut se déplacer 
        d'autant de cases qu'elle le désire.'''

    def __init__(self, start_row, start_column, target_row, target_column, player_number):
        super().__init__(start_row, start_column, target_row, target_column, player_number)

    # Effacement du pion adverse
    def capture(self, gameboard, make_a_move):
        opponent_row = make_a_move[opponent_row]
        opponent_column = make_a_move[opponent_col]
        gameboard[opponent_row][opponent_col] = 0

        return gameboard
