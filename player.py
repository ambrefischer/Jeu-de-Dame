# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:51:23 2020

@author: Ambre
"""
from utils import *
from gameboard import *


class Player():
    def __init__(self, number, score):
        self.number = number
        self.score = score

    # Cette fonction verifie que c'est le bon joueur et que la case est bonne
    def one_turn(self, start_row, start_column, target_row, target_column, gameboard):
        s_row = start_row - 1
        s_column = start_column - 1
        t_row = target_row - 1
        t_column = target_column - 1

        # Mauvaise entrée des coordonnées : hors plateau
        if (s_row < 0 or s_row > 9) or (s_column < 0 or s_column > 9) or (t_row < 0 or t_row > 9) or (t_column < 0 or t_column > 9):
            display_message(
                "VEUILLEZ SAISIR DES COORDONNEES SUR LE PLATEAU.", "red")
            display_message("Allez, on recommence...", "black")
            return {"message": "pb"}

        # On reste dans les coordonnées du plateau.
        else:
            # Le joueur prend bien un pion et le sien.
            if int(gameboard[s_row][s_column]) == self.number:
                return self.take_checker(s_row, s_column, t_row,
                                  t_column, gameboard)

            # Le joueur prend une dame et la sienne.
            elif float(gameboard[s_row][s_column]) == self.number+0.5:
                return self.take_king(gameboard, s_row, s_column)

            # Le joueur n'a pas pris son pion.
            else:
                display_message("VEUILLEZ PRENDRE UNE DE VOS PIECES.", "red")
                display_message(
                    "PS : Au fait, vos pions sont les %d ." % self.number, "black")
                return {"message": "pb"}

    def take_checker(self, s_row, s_column, t_row, t_column, gameboard):
        if self.number == 1:
            factor = 1
            opponent_number = 2
        else:
            factor = -1
            opponent_number = 1

        # Le joueur le met dans une case acceptée pour bouger (en bas pour j1, en haut pour j2).
        if t_row == s_row+factor and (t_column == s_column+1 or t_column == s_column-1) \
                and int(gameboard[t_row][t_column]) == 0:
            return {"message": "I'm on my way", "type": "Checker"}

        # Le joueur le met sur une case acceptée pour manger.
        elif (t_row == s_row+2 and t_column == s_column+2) \
                and int(gameboard[s_row+1][s_column+1]) == opponent_number:
            return {"message": "I capture", "target": "right - down", "type": "Checker"}
        elif (t_row == s_row+2 and t_column == s_column-2) \
                and int(gameboard[s_row+1][s_column-1]) == opponent_number:
            return {"message": "I capture", "target": "left - down", "type": "Checker"}
        elif (t_row == s_row-2 and t_column == s_column+2) \
                and int(gameboard[s_row-1][s_column+1]) == opponent_number:
            return {"message": "I capture", "target": "right - up", "type": "Checker"}
        elif (t_row == s_row-2 and t_column == s_column-2) \
                and int(gameboard[s_row-1][s_column-1]) == opponent_number:
            return {"message": "I capture", "target": "left - up", "type": "Checker"}

        # Le joueur ne met pas de bonnes coordonnées.
        else:
            display_message(
                "VOUS NE POUVEZ PAS PLACER VOTRE PION ICI. RECOMMENCEZ.", "red")
            display_message("PS : Faut lire les règles du jeu..." + "\n" +
                            "Heureusement que je sais coder sinon vous pourriez tricher !", "black")
            return {"message": "pb"}

    def take_king(self, s_row, s_column, t_row, t_column, gameboard):
        # Le joueur la met sur une case acceptée pour bouger : une case sur une diagonale.
        factor_king = abs(t_row - s_row)
        if abs(t_column - s_column) == factor_king and int(gameboard[t_row][t_column]) == 0:

            # La dame mange-t-elle un pion au passage?
            count_capture = []
            for distance in range(factor_king):
                row_down = s_row + distance
                row_up = s_row - distance
                col_right = s_column + distance
                col_left = s_column - distance
                if gameboard[row_up][col_right] == opponent_number:
                    count_capture.append([row_up, col_right])
                elif gameboard[row_up][col_left] == opponent_number:
                    count_capture.append([row_up, col_left])
                elif gameboard[row_down][col_right] == opponent_number:
                    count_capture.append([row_down, col_right])
                elif gameboard[row_down][col_left] == opponent_number:
                    count_capture.append([row_down, col_left])

            # Vérification que la dame ne prenne qu'un pion à la fois.
            if len(count_capture) == 1:
                return {"message": "I capture", "opponent_row": count_capture[0][0],
                        "opponent_col": count_capture[0][1], "type": "King"}
            elif len(count_capture) > 1:
                display_message(
                    "VOUS NE POUVEZ PAS PLACER VOTRE DAME ICI. RECOMMENCEZ.", "red")
                display_message("PS : Une Dame ne peut prendre qu'un joueur à la fois, sachez-le !" + "\n" +
                                "Heureusement que je sais coder sinon vous pourriez tricher !", "black")
                return {"message": "pb"}

            # Si la dame ne mange aucun pion alors elle se déplace juste.
            else:
                return {"message": "I'm on my way", "type": "King"}

        # Le joueur ne mets pas de bonnes coordonnées.
        else:
            display_message(
                "VOUS NE POUVEZ PAS PLACER VOTRE DAME ICI. RECOMMENCEZ.", "red")
            display_message("PS : Faut lire les règles du jeu..." + "\n" +
                            "Heureusement que je sais coder sinon vous pourriez tricher !", "black")
            return {"message": "pb"}

    def win_one_point(self):
        self.score += 1
        display_message("Le joueur %d prend un point." %
                        (self.number), "purple")

        opponent_number = 1
        if self.number == 1:
            opponent_number = 2

        display_message("Joueur %d ne perdez pas espoir ! Respirez... Vous pouvez le faire ;)"
                        % (opponent_number), "black")


class Human(Player):
    def __init__(self, number, score):
        super().__init__(number, score)

    # Cette fonction a pour but de demander au joueur ce qu'il veut faire pendant son tour.
    def play(self, gameboard):
        print("Les lignes et les colonnes commencent à 1 !")
        
        start_row = int(input("Sur quelle ligne se situe votre pion ? "))

#        while True:
#            try:
#                start_row = int(
#                    input("Sur quelle ligne se situe votre pion ? "))
#                break
#            except ValueError:
#                display_message(
#                    "Veuillez rentrer des coordonnée de cases.", "red")
#                display_message(
#                    "Les lignes et les colonnes commencent à 1 !", "black")
#                view(gameboard)

        while True:
            try:
                start_column = int(
                    input("Sur quelle colonne se situe votre pion ? "))
                break
            except ValueError:
                display_message(
                    "Veuillez rentrer des coordonnée de cases.", "red")
                display_message(
                    "Les lignes et les colonnes commencent à 1 !", "black")
                view(gameboard)

        while True:
            try:
                target_row = int(
                    input("Sur quelle ligne voulez-vous bouger votre pion ? "))
                break
            except ValueError:
                display_message(
                    "Veuillez rentrer des coordonnée de cases.", "red")
                display_message(
                    "Les lignes et les colonnes commencent à 1 !", "black")
                view(gameboard)

        while True:
            try:
                target_column = int(
                    input("Sur quelle colonne voulez-vous bouger votre pion ? "))
                break
            except ValueError:
                display_message(
                    "Veuillez rentrer des coordonnée de cases.", "red")
                display_message(
                    "Les lignes et les colonnes commencent à 1 !", "black")
                view(gameboard)

        return {"s_row": start_row, "s_column": start_column,
                "t_row": target_row, "t_column": target_column
                }

# class IA():
