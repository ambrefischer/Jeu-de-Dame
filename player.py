# -*- coding: utf-8 -*-
"""
Project : Jeu de Dames

@authors: Ambre Fischer & Charles Fortier (groupe TD 2)
"""

from utils import *
from gameboard import *
from constants import *



class Player():
    '''
    Cette classe décrit le comportement des joueurs. L'utilisateur suit le comportement de Human
    et il peut choisir de jouer contre quelqu'un d'autre sous forme de Human ou une IA.
    '''

    def __init__(self, number, score, opponent_number, factor):
        """
        Crée un joueur avec ses propres caractéristiques tout en mémorisant le numéro adverse.

        Paramètres
        ----------
        number, score: int
            Caractérise les paramètres propres du joueur.

        factor: int
            Les joueurs ne peuvent jouer que dans un sens. Le joueur 1 ne pourra que descendre
            avec ses pions. Son facteur sera +1. Le joueur 2 ne pourra que monter avec ses pions.
            Son facteur sera -1.

        opponent_number: int
            Enregistre le numéro de l'adversaire contre qui le joueur se bat.
            Sur le plateau, les pions adverses correspondent à opponent_number.
            Sur le plateau, les dames adverses correspondent à opponent_number+0.5.
        """

        self.number = number
        self.score = score
        self.opponent_number = opponent_number
        self.factor = factor


    def check_coords(self, s_row, s_column, t_row, t_column, gameboard):
        """
        Cette fonction verifie que c'est le bon joueur et que la case est bonne.

        Paramètres
        ----------
        s_row, s_column: int
            Coordonnées de la pièce à bouger.

        t_row, t_column: int
            Coordonnées de la case où mettre la pièce.

        gameboard: array
            Définit le plateau de jeu en cours.

        Renvoie
        -------
        {"message" = PB}: dict
            Les coordonnées ne respectent pas les règles du jeu,
        ou appelle la fonction take_checker,
        ou appelle la fonction take_king.
        """

        # Mauvaise entrée des coordonnées : hors plateau
        if out_of_bounds(s_row, s_column, t_row, t_column):
            return {"message": PB}

        # Le joueur prend bien un pion et le sien.
        if gameboard[s_row][s_column] == self.number:
            return self.take_checker(s_row, s_column, t_row,
                                     t_column, gameboard)

        # Le joueur prend une dame et la sienne.
        elif gameboard[s_row][s_column] == self.number+0.5:
            where_king = self.where_king(s_row, s_column, t_row, t_column)
            return self.take_king(s_row, s_column, t_row,
                                     t_column, gameboard, where_king)

        # Le joueur n'a pas pris son pion.
        display_message("VEUILLEZ PRENDRE UNE DE VOS PIECES.", "red")
        display_message(
            "PS : Au fait, vos pions sont les %d ." % self.number, "black")
        return {"message": PB}


    def take_checker(self, s_row, s_column, t_row, t_column, gameboard):
        """
        Détermine le type de mouvement voulu par le joueur avec son pion.

        Paramètres
        ----------
        s_row, s_column: int
            Coordonnées de la pièce à bouger.

        t_row, t_column: int
            Coordonnées de la case où mettre la pièce.

        gameboard: array
            Définit le plateau de jeu en cours.

        Renvoie
        -------
        dict
            "message": str
                indique le mouvement voulu.
                    I_M_ON_MY_WAY: Le pion se déplace juste.
                    I_CAPTURE: Le pion prend une pièce adverse.
                    PB: Les coordonnées ne respectent pas les règles du jeu.
            "target": str
                indique la direction et le sens du pion adverse à prendre.
                    None: pas de pièce adverse pour un simple déplacement.
                    RIGHT_DOWN: La pièce adverse ciblée se situe en bas à droite.
                    LEFT_DOWN: La pièce adverse ciblée se situe en bas à gauche.
                    RIGHT_UP: La pièce adverse ciblée se situe en haut à droite.
                    LEFT_UP: La pièce adverse ciblée se situe en haut à gauche.
            "type": str
                indique que la pièce est un Checker.
        """

        # Le joueur le met dans une case acceptée pour bouger (en bas pour j1, en haut pour j2).
        if t_row == s_row+self.factor and (t_column == s_column+1 or t_column == s_column-1) \
                and gameboard[t_row][t_column] == 0:
            return {"message": I_M_ON_MY_WAY, "target": None, "type": CHECKER}

        # Le joueur le met sur une case acceptée pour manger: 4 cas différents.
        #En bas à droite
        elif (t_row == s_row+2 and t_column == s_column+2) \
                and gameboard[t_row][t_column] == 0 \
                and (gameboard[s_row+1][s_column+1] == self.opponent_number \
                or gameboard[s_row+1][s_column+1] == self.opponent_number+0.5):
            return {"message": I_CAPTURE, "target": RIGHT_DOWN, "type": CHECKER}

        #En bas à gauche
        elif (t_row == s_row+2 and t_column == s_column-2) \
                and gameboard[t_row][t_column] == 0 \
                and (gameboard[s_row+1][s_column-1] == self.opponent_number \
                or gameboard[s_row+1][s_column+1] == self.opponent_number+0.5):
            return {"message": I_CAPTURE, "target": LEFT_DOWN, "type": CHECKER}

        #En haut à droite
        elif (t_row == s_row-2 and t_column == s_column+2) \
                and gameboard[t_row][t_column] == 0 \
                and (gameboard[s_row-1][s_column+1] == self.opponent_number\
                or gameboard[s_row+1][s_column+1] == self.opponent_number+0.5):
            return {"message": I_CAPTURE, "target": RIGHT_UP, "type": CHECKER}

        #En haut à gauche
        elif (t_row == s_row-2 and t_column == s_column-2) \
                and gameboard[t_row][t_column] == 0 \
                and (gameboard[s_row-1][s_column-1] == self.opponent_number\
                or gameboard[s_row+1][s_column+1] == self.opponent_number+0.5):
            return {"message": I_CAPTURE, "target": LEFT_UP, "type": CHECKER}

        # Le joueur ne met pas de bonnes coordonnées.
        display_message(
            "VOUS NE POUVEZ PAS PLACER VOTRE PION ICI. RECOMMENCEZ.", "red")
        display_message("PS : Faut lire les règles du jeu..." + "\n" +
                        "Heureusement que je sais coder sinon vous pourriez tricher !", "black")
        return {"message": PB}


    def where_king(self, s_row, s_column, t_row, t_column):
        """
        Détermine la direction et le sens de la diagonale de mouvement de la dame.

        Paramètres
        ----------
        s_row, s_column: int
            Coordonnées de la pièce à bouger.

        t_row, t_column: int
            Coordonnées de la case où mettre la pièce.

        Renvoie
        -------
        s: str
            RIGHT_DOWN: La dame se dirige vers en bas à droite.
            LEFT_DOWN: La dame se dirige vers en bas à gauche.
            RIGHT_UP: La dame se dirige vers en haut à droite.
            LEFT_UP: La dame se dirige vers en haut à gauche.
        """

        if s_row < t_row :
            if s_column < t_column :
                return RIGHT_DOWN
            return LEFT_DOWN
        if s_column < t_column :
                return RIGHT_UP
        return LEFT_UP


    def take_king(self, s_row, s_column, t_row, t_column, gameboard, where_king):
        """
        Détermine le type de mouvement voulu par le joueur avec sa dame.

        Paramètres
        ----------
        s_row, s_column: int
            Coordonnées de la pièce à bouger.

        t_row, t_column: int
            Coordonnées de la case où mettre la pièce.

        gameboard: array
            Définit le plateau de jeu en cours.

        where_king: str
            Indique la direction et le sens pris par le mouvement de la dame.
            Est déterminé en faisant appel à la fonction where_king

        Renvoie
        -------
        d: dict
            "message": str
                indique le mouvement voulu.
                    I_M_ON_MY_WAY: La dame se déplace juste.
                    I_CAPTURE: La dame prend une pièce adverse.
                    PB: Les coordonnées ne respectent pas les règles du jeu.
            "target": str
                indique la direction et le sens du pion adverse à prendre.
                    where_king: la méthode du même nom indique par un str la direction et le sens
                    None: pas de pièce adverse pour un simple déplacement.
            "opponent_row", "opponenent_column": int
                indique les coordonnées du pion adverse à prendre.
            "type": str
                indique le que la pièce est un King.
        """

        # Le joueur la met sur une case acceptée pour bouger : une case sur une diagonale.
        factor_king = abs(t_row - s_row)
        if abs(t_column - s_column) == factor_king and int(gameboard[t_row][t_column]) == 0:

            # La dame mange-t-elle une pièce au passage?
            count_capture = []
            # On parcourt toute la diagonale pour savoir combien de pièces elle mange
            for distance in range(factor_king):
                row_down = s_row + distance
                row_up = s_row - distance
                col_right = s_column + distance
                col_left = s_column - distance
                if where_king == RIGHT_UP and (gameboard[row_up][col_right] == self.opponent_number\
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
        """
        Cette fonction augmente le score d'un joueur lorsqu'il prend une pièce adverse.

        Paramètres
        ----------
        Aucun
        """

        self.score += 1
        display_message("Le joueur %d prend un point." %
                        (self.number), "purple")
        display_message("Joueur %d ne perdez pas espoir ! Respirez... Vous pouvez le faire ;)"
                        % (self.opponent_number), "black")


    def can_capture_again_with_checker(self, gameboard, s_row, s_column):
        """
        On est dans le cas où le joueur vient de prendre une pièce adverse avec son pion.
        Il ne peut rejouer que si il peut reprendre une pièce adverse.
        Cette fonction détermine si le joueur peut rejouer.

        Paramètres
        ----------
        s_row, s_column: int
            Coordonnées de la pièce à bouger.

        gameboard: array
            Définit le plateau de jeu en cours.

        Renvoie
        -------
        play_again: dict
            "bool": bool
                indique si le joueur est dans les conditions pour rejouer.
            "target_rd", "target_ld", "target_ru", "target_lu" : str
                indiquent la direction et le sens du pion adverse à prendre.
                    None: pas de pièce adverse pour un simple déplacement.
                    RIGHT_DOWN: La pièce adverse ciblée se situe en bas à droite.
                    LEFT_DOWN: La pièce adverse ciblée se situe en bas à gauche.
                    RIGHT_UP: La pièce adverse ciblée se situe en haut à droite.
                    LEFT_UP: La pièce adverse ciblée se situe en haut à gauche.

        """

        #On considère au début qu'il n'y a pas de possibilité de rejouer.
        play_again = {"bool": False, "target_rd": None, "target_ld": None, "target_ru": None, "target_lu": None}

        #On vérifie les cases en diagonales voisines si elles sont occupées par une pièce adverse
        # et que la case encore après est vide en faisant attention aux limites du terrain.
        #En bas à droite
        if (s_row < 8 and s_column > 1) \
                and (gameboard[s_row+1][s_column+1] == self.opponent_number \
                or gameboard[s_row+1][s_column+1] == self.opponent_number+0.5)\
                and gameboard[s_row+2][s_column+2] == 0:
            play_again["bool"] = True
            play_again["target_rd"] = RIGHT_DOWN

        #En bas à gauche
        if (s_row < 8 and s_column > 1) \
                and (gameboard[s_row+1][s_column-1] == self.opponent_number \
                or gameboard[s_row+1][s_column-1] == self.opponent_number+0.5) \
                and gameboard[s_row+2][s_column-2] == 0:
            play_again["bool"] = True
            play_again["target_ld"] = LEFT_DOWN

        #En haut à droite
        if (s_row > 1 and s_column < 8) \
                and (gameboard[s_row-1][s_column+1] == self.opponent_number \
                or gameboard[s_row-1][s_column+1] == self.opponent_number+0.5) \
                and gameboard[s_row-2][s_column+2] == 0:
            play_again["bool"] = True
            play_again["target_ru"] = RIGHT_UP

        #En haut à gauche
        if (s_row > 1 and s_column > 1) \
                and (gameboard[s_row-1][s_column-1] == self.opponent_number \
                or gameboard[s_row-1][s_column-1] == self.opponent_number+0.5) \
                and gameboard[s_row-2][s_column-2] == 0:
            play_again["bool"] = True
            play_again["target_lu"] = LEFT_UP

        return play_again


    def can_capture_again_with_king(self, gameboard, s_row, s_column):
        """
        Détermine si le joueur peut rejouer.

        Paramètres
        ----------
        s_row, s_column: int
            Coordonnées de la pièce à bouger.

        gameboard: array
            Définit le plateau de jeu en cours.

        Renvoie
        -------
        dict
            "bool": bool
                indique si le joueur est dans les conditions pour rejouer.
            "target": str
                indique la direction et le sens du pion adverse à prendre.
                    None: pas de pièce adverse pour un simple déplacement.
                    RIGHT_DOWN: La pièce adverse ciblée se situe en bas à droite.
                    LEFT_DOWN: La pièce adverse ciblée se situe en bas à gauche.
                    RIGHT_UP: La pièce adverse ciblée se situe en haut à droite.
                    LEFT_UP: La pièce adverse ciblée se situe en haut à gauche.

        Note
        -------
        On est dans le cas où le joueur vient de prendre une pièce adverse avec sa dame.
        Il ne peut rejouer que si il peut reprendre une pièce adverse.
        """

        #On considère au début qu'on ne remplit aucune condition.
        play_again = {"bool": False, "target_rd": None, "target_ld": None, "target_ru": None, "target_lu": None}

        #Vérification en descendant sur le plateau en faisant attention aux limites.
        col_right = s_column
        col_left = s_column
        row = s_row

        while row < 9:
            #A droite
            if col_right < 9 \
                    and (gameboard[row][col_right] == self.opponent_number \
                    or gameboard[row][col_right] == self.opponent_number+0.5) \
                    and gameboard[row+1][col_right+1] == 0:
                play_again["bool"] = True
                play_again["target_rd"] = RIGHT_DOWN

            #A gauche
            if col_left > 0 \
                    and (gameboard[row][col_left] == self.opponent_number \
                    or gameboard[row][col_left] == self.opponent_number+0.5) \
                    and gameboard[row+1][col_left-1] == 0:
                play_again["bool"] = True
                play_again["target_ld"] = LEFT_DOWN

            col_right +=1
            col_left -= 1
            row += 1

        #Vérification en montant sur le plateau en faisant attention aux limites.
        col_right = s_column
        col_left = s_column
        row = s_row

        while row > 0:
            #A droite
            if col_right < 9 \
                    and (gameboard[row][col_right] == self.opponent_number \
                    or gameboard[row][col_right] == self.opponent_number+0.5) \
                    and gameboard[row-1][col_right+1] == 0:
                play_again["bool"] = True
                play_again["target_ru"] = RIGHT_UP

            #A gauche
            if col_left > 0 \
                    and (gameboard[row][col_left] == self.opponent_number \
                    or gameboard[row][col_left] == self.opponent_number+0.5) \
                    and gameboard[row-1][col_left-1] == 0:
                play_again["bool"] = True
                play_again["target_lu"] = LEFT_UP

            col_right +=1
            col_left -= 1
            row -= 1

        return play_again





class Human(Player):
    '''
    La classe Human hérite de la classe Player.
    Human possède 4 méthodes qui demandent à l'utilisateur de choisir les coordonnées
    de la pièce à déplacer (s_row pour start row, s_column pour start column) et les
    coordonnées de la case ciblée (t_row pour target row, t_column pour target column).
    Le joueur rentre des coordonnées de 1 à 10 or gameboard est un tableau 10x10 avec
    les lignes et les colonnes commençant à 0 finissant à 9.
    On décrémente donc de 1 les coordonnées entrées par le joueur.
    '''

    def __init__(self, number, score, opponent_number, factor):
        super().__init__(number, score, opponent_number, factor)


    def choose_s_row(self, gameboard):
        """
        Demande au joueur sur quelle ligne se place sa pièce désirée.

        Paramètres
        ----------
        gameboard: array
            Définit le plateau de jeu en cours.

        Renvoie
        -------
        start_row: int
            Compris dans [1,10]
            Ligne sur laquelle se situe la pièce qui va faire un mouvement.

        Exception
        -------
        Si la coordonnée rentrée n'est pas un nombre.
        """

        display_message("Les lignes et les colonnes commencent à 1 !")
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
        return start_row - 1


    def choose_s_column(self, gameboard):
        """
        Demande au joueur sur quelle colonne se place sa pièce désirée.

        Paramètres
        ----------
        gameboard: array
            Définit le plateau de jeu en cours.

        Renvoie
        -------
        start_column: int
            Compris dans [1,10]
            Colonne sur laquelle se situe la pièce qui va faire un mouvement.

        Exception
        -------
        Si la coordonnée rentrée n'est pas un nombre.
        """

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

        return start_column - 1


    def choose_t_row(self, gameboard):
        """
        Demande au joueur sur quelle ligne il veut faire avancer sa pièce.

        Paramètres
        ----------
        gameboard: array
            Définit le plateau de jeu en cours.

        Renvoie
        -------
        target_row: int
            Compris dans [1,10]
            Ligne sur laquelle la pièce va avancer.

        Exception
        -------
        Si la coordonnée rentrée n'est pas un nombre.
        """

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

        return target_row - 1


    def choose_t_column(self, gameboard):
        """
        Demande au joueur sur quelle colonne il veut faire avancer sa pièce.

        Paramètres
        ----------
        gameboard: array
            Définit le plateau de jeu en cours.

        Renvoie
        -------
        target_column: int
            Compris dans [1,10]
            Colonne sur laquelle la pièce va avancer.

        Exception
        -------
        Si la coordonnée rentrée n'est pas un nombre.
        """

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

        return target_column - 1





# class IA():
