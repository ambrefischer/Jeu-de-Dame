# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:51:23 2020

@author: Ambre
"""
from utils import *
from gameboard import *
from constants import *



class Player():
    def __init__(self, number, score, opponent_number, factor):
        self.number = number
        self.score = score
        self.opponent_number = opponent_number
        self.factor = factor

    # Cette fonction verifie que c'est le bon joueur et que la case est bonne
    def check_coords(self, start_row, start_column, target_row, target_column, gameboard):
        s_row = start_row - 1
        s_column = start_column - 1
        t_row = target_row - 1
        t_column = target_column - 1


        # Mauvaise entrée des coordonnées : hors plateau
        if out_of_bounds(s_row, s_column, t_row, t_column):
            return {"message": PB}

        # Le joueur prend bien un pion et le sien.
        if float(gameboard[s_row][s_column]) == self.number:
            return self.take_checker(s_row, s_column, t_row,
                                     t_column, gameboard)

        # Le joueur prend une dame et la sienne.
        elif float(gameboard[s_row][s_column]) == self.number+0.5:
            where_king = self.where_king(s_row, s_column, t_row, t_column)
            return self.take_king(s_row, s_column, t_row,
                                     t_column, gameboard, where_king)

        # Le joueur n'a pas pris son pion.
        display_message("VEUILLEZ PRENDRE UNE DE VOS PIECES.", "red")
        display_message(
            "PS : Au fait, vos pions sont les %d ." % self.number, "black")
        return {"message": PB}



    def take_checker(self, s_row, s_column, t_row, t_column, gameboard):

        # Le joueur le met dans une case acceptée pour bouger (en bas pour j1, en haut pour j2).
        if t_row == s_row+self.factor and (t_column == s_column+1 or t_column == s_column-1) \
                and int(gameboard[t_row][t_column]) == 0:
            return {"message": I_M_ON_MY_WAY, "target": None, "type": CHECKER}

        # Le joueur le met sur une case acceptée pour manger.
        elif (t_row == s_row+2 and t_column == s_column+2) \
                and int(gameboard[t_row][t_column]) == 0 \
                and (int(gameboard[s_row+1][s_column+1]) == self.opponent_number \
                or int(gameboard[s_row+1][s_column+1]) == self.opponent_number+0.5):
            return {"message": I_CAPTURE, "target": RIGHT_DOWN, "type": CHECKER}
        elif (t_row == s_row+2 and t_column == s_column-2) \
                and int(gameboard[t_row][t_column]) == 0 \
                and (int(gameboard[s_row+1][s_column-1]) == self.opponent_number \
                or int(gameboard[s_row+1][s_column+1]) == self.opponent_number+0.5):
            return {"message": I_CAPTURE, "target": LEFT_DOWN, "type": CHECKER}
        elif (t_row == s_row-2 and t_column == s_column+2) \
                and int(gameboard[t_row][t_column]) == 0 \
                and (int(gameboard[s_row-1][s_column+1]) == self.opponent_number\
                or int(gameboard[s_row+1][s_column+1]) == self.opponent_number+0.5):
            return {"message": I_CAPTURE, "target": RIGHT_UP, "type": CHECKER}
        elif (t_row == s_row-2 and t_column == s_column-2) \
                and int(gameboard[t_row][t_column]) == 0 \
                and (int(gameboard[s_row-1][s_column-1]) == self.opponent_number\
                or int(gameboard[s_row+1][s_column+1]) == self.opponent_number+0.5):
            return {"message": I_CAPTURE, "target": LEFT_UP, "type": CHECKER}

        # Le joueur ne met pas de bonnes coordonnées.
        display_message(
            "VOUS NE POUVEZ PAS PLACER VOTRE PION ICI. RECOMMENCEZ.", "red")
        display_message("PS : Faut lire les règles du jeu..." + "\n" +
                        "Heureusement que je sais coder sinon vous pourriez tricher !", "black")
        return {"message": PB}


    def where_king(self, s_row, s_column, t_row, t_column):
        if s_row < t_row :
            if s_column < t_column :
                return RIGHT_DOWN
            return LEFT_DOWN
        if s_column < t_column :
                return RIGHT_UP
        return LEFT_UP


    def take_king(self, s_row, s_column, t_row, t_column, gameboard, where_king):

        # Le joueur la met sur une case acceptée pour bouger : une case sur une diagonale.
        factor_king = abs(t_row - s_row)
        if abs(t_column - s_column) == factor_king and int(gameboard[t_row][t_column]) == 0:

            # La dame mange-t-elle un pion au passage?
            count_capture = []
            # On parcourt toute la diagonale pour savoir combien de pions elle mange
            for distance in range(factor_king):
                row_down = s_row + distance
                row_up = s_row - distance
                col_right = s_column + distance
                col_left = s_column - distance
                if where_king == RIGHT_UP and ([row_up][col_right] == self.opponent_number\
                        or gameboard[row_up][col_right] == self.opponent_number+0.5):
                    count_capture.append([row_up, col_right])
                elif where_king == LEFT_UP and (gameboard[row_up][col_left] == self.opponent_number\
                        or gameboard[row_up][col_left] == self.opponent_number+0.5):
                    count_capture.append([row_up, col_left])
                elif where_king == RIGHT_DOWN and (gameboard[row_down][col_right] == self.opponent_number\
                        or gameboard[row_down][col_right] == self.opponent_number+0.5):
                    count_capture.append([row_down, col_right])
                elif where_king == LEFT_DOWN and (gameboard[row_down][col_left] == self.opponent_number\
                        or gameboard[row_down][col_left] == self.opponent_number+0.5):
                    count_capture.append([row_down, col_left])

            # Vérification que la dame ne prenne qu'un pion à la fois.
            if len(count_capture) == 1:
                return {"message": I_CAPTURE, "target": where_king, "opponent_row": count_capture[0][0],
                        "opponent_col": count_capture[0][1], "type": KING}
            elif len(count_capture) > 1:
                display_message(
                    "VOUS NE POUVEZ PAS PLACER VOTRE DAME ICI. RECOMMENCEZ.", "red")
                display_message("PS : Une Dame ne peut prendre qu'un joueur à la fois, sachez-le !" + "\n" +
                                "Heureusement que je sais coder sinon vous pourriez tricher !", "black")
                return {"message": PB}

            # Si la dame ne mange aucun pion alors elle se déplace juste.
            return {"message": I_M_ON_MY_WAY, "target": None, "type": KING}

        # Le joueur ne mets pas de bonnes coordonnées.

        display_message(
            "VOUS NE POUVEZ PAS PLACER VOTRE DAME ICI. RECOMMENCEZ.", "red")
        display_message("PS : Faut lire les règles du jeu..." + "\n" +
                        "Heureusement que je sais coder sinon vous pourriez tricher !", "black")
        return {"message": PB}


    def win_one_point(self):
        self.score += 1
        display_message("Le joueur %d prend un point." %
                        (self.number), "purple")
        display_message("Joueur %d ne perdez pas espoir ! Respirez... Vous pouvez le faire ;)"
                        % (self.opponent_number), "black")


    def can_capture_again_with_checker(self, gameboard, s_row, s_column):
        s_row -= 1
        s_column -= 1
        if gameboard[s_row+1][s_column+1] == self.opponent_number \
                and gameboard[s_row+2][s_column+2] == 0:
            return {"bool": True, "target": RIGHT_DOWN}
        elif gameboard[s_row+1][s_column-1] == self.opponent_number \
                and gameboard[s_row+2][s_column-2] == 0:
            print("checker dl")
            return {"bool": True, "target": LEFT_DOWN}
        elif gameboard[s_row-1][s_column+1] == self.opponent_number \
                and gameboard[s_row-2][s_column+2] == 0:
            print("checker ur")
            return {"bool": True, "target": RIGHT_UP}
        elif gameboard[s_row-1][s_column-1] == self.opponent_number \
                and gameboard[s_row-2][s_column-2] == 0:
            print("checker ul")
            return {"bool": True, "target": LEFT_UP}
        return {"bool": False, "target": None}

    def can_capture_again_with_king(self, gameboard, s_row, s_column):
        s_row -= 1
        s_column -= 1
        #check en descendant sur le plateau
        column_right = s_column
        column_left = s_column
        for row in range(s_row, 10):
            if gameboard[row][column_right] == self.opponent_number \
                    and gameboard[row+1][column_right+1] == 0:
                print("king dr")
                return {"bool": True, "target": RIGHT_DOWN}
            elif gameboard[row][column_left] == self.opponent_number \
                    and gameboard[row+1][column_left-1] == 0:
                print("king dl")
                return {"bool": True, "target": LEFT_DOWN}
            column_right +=1
            column_left -= 1

        #check en montant sur le plateau
        column_right = s_column
        column_left = s_column
        for row in range(s_row-1, -1, -1):
            if gameboard[row][column_right] == self.opponent_number \
                    and gameboard[row+1][column_right+1] == 0:
                print("king ur")
                return {"bool": True, "target": RIGHT_UP}
            elif gameboard[row][column_left] == self.opponent_number \
                    and gameboard[row+1][column_left-1] == 0:
                print("king ul")
                return {"bool": True, "target": LEFT_UP}
            column_right +=1
            column_left -= 1

        return {"bool": False, "target": None}





class Human(Player):
    def __init__(self, number, score, opponent_number, factor):
        super().__init__(number, score, opponent_number, factor)

    # Cette fonction a pour but de demander au joueur ce qu'il veut faire pendant son tour.
    def choose_s_row(self, gameboard):
        print("Les lignes et les colonnes commencent à 1 !")
        while True:
           try:
               start_row = int(
                   input("Sur quelle ligne se situe votre pion ? "))
               break
           except ValueError:
               display_message(
                   "Veuillez rentrer des coordonnées de cases.", "red")
               display_message(
                   "Les lignes et les colonnes commencent à 1 !", "black")
               view(gameboard)
        return start_row

    def choose_s_column(self, gameboard):
        while True:
            try:
                start_column = int(
                    input("Sur quelle colonne se situe votre pion ? "))
                break
            except ValueError:
                display_message(
                    "Veuillez rentrer des coordonnées de cases.", "red")
                display_message(
                    "Les lignes et les colonnes commencent à 1 !", "black")
                view(gameboard)
        return start_column

    def choose_t_row(self, gameboard):
        while True:
            try:
                target_row = int(
                    input("Sur quelle ligne voulez-vous bouger votre pion ? "))
                break
            except ValueError:
                display_message(
                    "Veuillez rentrer des coordonnées de cases.", "red")
                display_message(
                    "Les lignes et les colonnes commencent à 1 !", "black")
                view(gameboard)
        return target_row

    def choose_t_column(self, gameboard):
        while True:
            try:
                target_column = int(
                    input("Sur quelle colonne voulez-vous bouger votre pion ? "))
                break
            except ValueError:
                display_message(
                    "Veuillez rentrer des coordonnées de cases.", "red")
                display_message(
                    "Les lignes et les colonnes commencent à 1 !", "black")
                view(gameboard)
        return target_column


# class IA():
