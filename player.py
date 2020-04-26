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


    def checker_capture_RIGHT_DOWN(self, gameboard, s_row, s_column):
        if (gameboard[s_row + 1][s_column + 1] == self.opponent_number \
                or gameboard[s_row + 1][s_column + 1] == self.opponent_number + 0.5) \
                and gameboard[s_row + 2][s_column + 2] == 0:
            return True
        return False


    def checker_capture_RIGHT_UP(self, gameboard, s_row, s_column):
        if (gameboard[s_row-1][s_column+1] == self.opponent_number \
                or gameboard[s_row-1][s_column+1] == self.opponent_number+0.5) \
                and gameboard[s_row-2][s_column+2] == 0:
            return True
        return False


    def checker_capture_LEFT_DOWN(self, gameboard, s_row, s_column):
        if (gameboard[s_row + 1][s_column - 1] == self.opponent_number \
                or gameboard[s_row + 1][s_column - 1] == self.opponent_number + 0.5) \
                and gameboard[s_row + 2][s_column - 2] == 0:
            return True
        return False


    def checker_capture_LEFT_UP(self, gameboard, s_row, s_column):
        if (gameboard[s_row-1][s_column-1] == self.opponent_number \
                or gameboard[s_row-1][s_column-1] == self.opponent_number+0.5) \
                and gameboard[s_row-2][s_column-2] == 0:
            return True
        return False


    def check_coords(self, s_row, s_column, t_row, t_column, gameboard, coords_pieces, must_capture):
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

        # Vérification que le joueur prenne une pièce qui peut manger si elle existe.
        compt_wrong_move = 0
        compt_correct_move = 0
        for key in coords_pieces:
            rule_row = coords_pieces[key][1]
            rule_col = coords_pieces[key][2]
            info_piece = must_capture[key]
            # Il existe une pièce qui peut manger une pièce adverse et le joueur doit la prendre.
            if info_piece["bool"] == True:
                if rule_row != s_row or rule_col != s_column:
                    compt_wrong_move += 1
                else:
                    compt_correct_move += 1

        # Le joueur n'a pas pris la bonne pièce selon les règles du jeu.
        if compt_wrong_move != 0 and compt_correct_move == 0:
            display_message("Vous devez prendre la pièce qui peut prendre un point.")
            return {"message": PB}

        # Le joueur prend bien un pion et le sien,
        if gameboard[s_row][s_column] == self.number:
            return self.take_checker(s_row, s_column, t_row, t_column,
                                     gameboard, info_piece)

        # Le joueur prend une dame et la sienne,
        elif gameboard[s_row][s_column] == self.number+0.5:
            where_king = self.where_king(s_row, s_column, t_row, t_column)
            return self.take_king(s_row, s_column, t_row, t_column,
                                  gameboard, where_king, info_piece)

        # Le joueur n'a pas pris son pion.
        display_message("VEUILLEZ PRENDRE UNE DE VOS PIECES.", "red")
        display_message(
            "PS : Au fait, vos pions sont les %d ." % self.number, "black")
        return {"message": PB}


    def take_checker(self, s_row, s_column, t_row, t_column, gameboard, info_checker):
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

        # Le joueur est dans le cas où un pion peut manger une pièce adverse,
        # donc le joueur doit jouer ce pion pour gagner un point.
        if info_checker["bool"] == True:
            if info_checker["target_rd"] == RIGHT_DOWN and (t_row == s_row+2 and t_column == s_column+2)\
                    and self.checker_capture_RIGHT_DOWN(gameboard, s_row, s_column):
                return {"message": I_CAPTURE, "target": RIGHT_DOWN, "type": CHECKER}

            elif info_checker["target_ld"] == LEFT_DOWN and (t_row == s_row+2 and t_column == s_column-2) \
                    and self.checker_capture_LEFT_DOWN(gameboard, s_row, s_column):
                return {"message": I_CAPTURE, "target": LEFT_DOWN, "type": CHECKER}

            elif info_checker["target_ru"] == RIGHT_UP and (t_row == s_row-2 and t_column == s_column+2) \
                    and self.checker_capture_RIGHT_UP(gameboard, s_row, s_column):
                return {"message": I_CAPTURE, "target": RIGHT_UP, "type": CHECKER}

            elif info_checker["target_lu"] == LEFT_UP and (t_row == s_row-2 and t_column == s_column-2) \
                    and self.checker_capture_LEFT_UP(gameboard, s_row, s_column):
                return {"message": I_CAPTURE, "target": LEFT_UP, "type": CHECKER}

            display_message("CE PION DOIT PRENDRE UNE PIECE ADVERSE.", "red")
            display_message("Ce sont les règles...", "black")
            return {"message": PB}

        # Le joueur est dans le cas où il peut faire ce qu'il veut.
        # Le joueur le met dans une case acceptée pour bouger (en bas pour J1, en haut pour J2).
        elif t_row == s_row+self.factor and (t_column == s_column+1 or t_column == s_column-1) \
                and gameboard[t_row][t_column] == 0:
            return {"message": I_M_ON_MY_WAY, "target": None, "type": CHECKER}

        # Le joueur le met sur une case acceptée pour manger: 4 cas différents.
        #En bas à droite
        elif (t_row == s_row+2 and t_column == s_column+2) \
                and self.checker_capture_RIGHT_DOWN(gameboard, s_row, s_column):
            return {"message": I_CAPTURE, "target": RIGHT_DOWN, "type": CHECKER}

        #En bas à gauche
        elif (t_row == s_row+2 and t_column == s_column-2) \
                and self.checker_capture_LEFT_DOWN(gameboard, s_row, s_column):
            return {"message": I_CAPTURE, "target": LEFT_DOWN, "type": CHECKER}

        #En haut à droite
        elif (t_row == s_row-2 and t_column == s_column+2) \
                and self.checker_capture_RIGHT_UP(gameboard, s_row, s_column):
            return {"message": I_CAPTURE, "target": RIGHT_UP, "type": CHECKER}

        #En haut à gauche
        elif (t_row == s_row-2 and t_column == s_column-2) \
                and self.checker_capture_LEFT_UP(gameboard, s_row, s_column):
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


    def take_king(self, s_row, s_column, t_row, t_column, gameboard, where_king, info_king):
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
        piece_blocking = False
        if abs(t_column - s_column) == factor_king and int(gameboard[t_row][t_column]) == 0:

            # La dame mange-t-elle une pièce au passage?
            count_capture = []
            count_must_capture = []
            # On parcourt toute la diagonale pour savoir combien de pièces elle mange
            for distance in range(1, factor_king):
                row_down = s_row + distance
                row_up = s_row - distance
                col_right = s_column + distance
                col_left = s_column - distance

                #Le joueur est dans le cas où un pion peut manger une pièce adverse,
                #donc le joueur doit jouer ce pion pour gagner un point.
                if info_king["bool"] == True:
                    if where_king == RIGHT_UP and (gameboard[row_up][col_right] == self.opponent_number \
                            or gameboard[row_up][col_right] == self.opponent_number + 0.5):
                        count_must_capture.append([row_up, col_right])
                    elif where_king == LEFT_UP and (gameboard[row_up][col_left] == self.opponent_number \
                            or gameboard[row_up][col_left] == self.opponent_number + 0.5):
                        count_must_capture.append([row_up, col_left])
                    elif where_king == RIGHT_DOWN and (gameboard[row_down][col_right] == self.opponent_number \
                            or gameboard[row_down][col_right] == self.opponent_number + 0.5):
                        count_must_capture.append([row_down, col_right])
                    elif where_king == LEFT_DOWN and (gameboard[row_down][col_left] == self.opponent_number \
                            or gameboard[row_down][col_left] == self.opponent_number + 0.5):
                        count_must_capture.append([row_down, col_left])

                elif where_king == RIGHT_UP and (gameboard[row_up][col_right] == self.opponent_number\
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

                # On vérifie qu'aucun de ses propres joueurs ne gène la diagonale.
                if gameboard[row_up][col_right] == self.number or gameboard[row_up][col_right] == self.number + 0.5 \
                        or gameboard[row_up][col_left] == self.number or gameboard[row_up][col_left] == self.number+0.5 \
                        or gameboard[row_down][col_right] == self.number or gameboard[row_down][col_right] == self.number+0.5 \
                        or gameboard[row_down][col_left] == self.number or gameboard[row_down][col_left] == self.number+0.5:
                    piece_blocking = True

            # Vérification que la dame ne prenne qu'un pion à la fois.
            if len(count_must_capture) == 1 and piece_blocking == False:
                return {"message": I_CAPTURE, "target": where_king, "opponent_row": count_must_capture[0][0],
                        "opponent_col": count_must_capture[0][1], "type": KING}

            elif len(count_capture) == 1 and piece_blocking == False:
                return {"message": I_CAPTURE, "target": where_king, "opponent_row": count_capture[0][0],
                        "opponent_col": count_capture[0][1], "type": KING}

            elif len(count_must_capture) >1 or len(count_capture) > 1 or piece_blocking == True:
                display_message(
                    "VOUS NE POUVEZ PAS PLACER VOTRE DAME ICI. RECOMMENCEZ.", "red")
                display_message("PS : Une Dame ne peut prendre qu'un joueur à la fois, sachez-le !" + "\n" +
                                "Heureusement que je sais coder sinon vous pourriez tricher !", "black")
                return {"message": PB}

            elif info_king["bool"] == True and len(count_must_capture) == 0:
                display_message("VOTRE DAME DOIT PRENDRE UNE PIECE ENNEMIE.", "red")
                display_message("Ce sont les règles...", "black")
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


    def can_capture_with_checker(self, gameboard, s_row, s_column):
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
        play_capture = {"bool": False, "target_rd": None, "target_ld": None, "target_ru": None, "target_lu": None}
        #On vérifie les cases en diagonales voisines si elles sont occupées par une pièce adverse
        # et que la case encore après est vide en faisant attention aux limites du terrain.
        #En bas à droite
        if (s_row < 8 and s_column < 8) \
                and self.checker_capture_RIGHT_DOWN(gameboard, s_row, s_column):
            play_capture["bool"] = True
            play_capture["target_rd"] = RIGHT_DOWN

        #En bas à gauche
        if (s_row < 8 and s_column > 1) \
                and self.checker_capture_LEFT_DOWN(gameboard, s_row, s_column):
            play_capture["bool"] = True
            play_capture["target_ld"] = LEFT_DOWN

        #En haut à droite
        if (s_row > 1 and s_column < 8) \
                and self.checker_capture_RIGHT_UP(gameboard, s_row, s_column):
            play_capture["bool"] = True
            play_capture["target_ru"] = RIGHT_UP

        #En haut à gauche
        if (s_row > 1 and s_column > 1) \
                and self.checker_capture_LEFT_UP(gameboard, s_row, s_column):
            play_capture["bool"] = True
            play_capture["target_lu"] = LEFT_UP

        return play_capture


    def can_capture_with_king(self, gameboard, s_row, s_column):
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
        play_capture = {"bool": False, "target_rd": None, "target_ld": None, "target_ru": None, "target_lu": None}
        piece_blocking = False

        #Vérification en descendant sur le plateau en faisant attention aux limites.
        col_right = s_column + 1
        col_left = s_column - 1
        row = s_row + 1

        while row < 9:
            #A droite
            if col_right < 9 \
                    and (gameboard[row][col_right] == self.opponent_number \
                    or gameboard[row][col_right] == self.opponent_number+0.5) \
                    and gameboard[row+1][col_right+1] == 0:
                play_capture["bool"] = True
                play_capture["target_rd"] = RIGHT_DOWN

            #A gauche
            if col_left > 0 \
                    and (gameboard[row][col_left] == self.opponent_number \
                    or gameboard[row][col_left] == self.opponent_number+0.5) \
                    and gameboard[row+1][col_left-1] == 0:
                play_capture["bool"] = True
                play_capture["target_ld"] = LEFT_DOWN

            if (col_right < 9 and col_left > 0) and play_capture["bool"] == False \
                    and (gameboard[row][col_right] == self.number or gameboard[row][col_right] == self.number + 0.5 \
                    or gameboard[row][col_left] == self.number or gameboard[row][col_left] == self.number + 0.5):
                piece_blocking = True

            col_right +=1
            col_left -= 1
            row += 1

        #Vérification en montant sur le plateau en faisant attention aux limites.
        col_right = s_column + 1
        col_left = s_column - 1
        row = s_row - 1

        while row > 0:
            #A droite
            if col_right < 9 \
                    and (gameboard[row][col_right] == self.opponent_number \
                    or gameboard[row][col_right] == self.opponent_number+0.5) \
                    and gameboard[row-1][col_right+1] == 0:
                play_capture["bool"] = True
                play_capture["target_ru"] = RIGHT_UP

            #A gauche
            if col_left > 0 \
                    and (gameboard[row][col_left] == self.opponent_number \
                    or gameboard[row][col_left] == self.opponent_number+0.5) \
                    and gameboard[row-1][col_left-1] == 0:
                play_capture["bool"] = True
                play_capture["target_lu"] = LEFT_UP

            if (col_right < 9 and col_left > 0) and play_capture["bool"] == False \
                    and (gameboard[row][col_right] == self.number or gameboard[row][col_right] == self.number + 0.5 \
                    or gameboard[row][col_left] == self.number or gameboard[row][col_left] == self.number + 0.5):
                piece_blocking = True

            col_right +=1
            col_left -= 1
            row -= 1

        if piece_blocking == True:
            play_capture["bool"] = False

        return play_capture


    def where_piece(self, gameboard):
        coords_pieces = {}
        index = 1
        for i in range(10):
            for j in range(10):
                if gameboard[i][j] == self.number \
                        or gameboard[i][j] == self.number +0.5:
                    coords_pieces[index] = [gameboard[i][j], i, j]
                    index += 1
        return [coords_pieces, index-1]



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


    def must_capture(self, gameboard):
        coords_pieces = self.where_piece(gameboard)[0]
        nb_pieces = self.where_piece(gameboard)[1]
        must_capture = {}
        for index in range(nb_pieces):
            coords = coords_pieces[index+1]
            if coords[0] == self.number:
                must_capture[index+1] = self.can_capture_with_checker(gameboard, coords[1], coords[2])
            else:
                must_capture[index+1] = self.can_capture_with_king(gameboard, coords[1], coords[2])
        return must_capture


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


class IA(Player):

    def __init__(self, number, score, opponent_number, factor, level):
        super().__init__(number, score, opponent_number, factor)
        self.level = level


    def must_capture(self, gameboard):  # défini la liste des prises possibles pour l'IA
        must_capture = []
        coords_pieces, nb_pieces = self.where_piece(gameboard)[0], self.where_piece(gameboard)[1]
        for index in range(nb_pieces):
            coords = coords_pieces[index + 1]

            # permet de déterminer les pions pouvant capturer une pièce adverse
            if coords[0] == self.number:
                angle1 = [coords[1] + 1, coords[2] + 1]
                angle2 = [coords[1] + 1, coords[2] - 1]
                angle3 = [coords[1] - 1, coords[2] + 1]
                angle4 = [coords[1] - 1, coords[2] - 1]

                destination1 = [coords[1] + 2, coords[2] + 2]
                destination2 = [coords[1] + 2, coords[2] - 2]
                destination3 = [coords[1] - 2, coords[2] + 2]
                destination4 = [coords[1] - 2, coords[2] - 2]

                if out_of_bounds2(destination1) == False and gameboard[angle1[0]][
                    angle1[1]] // 1 == self.opponent_number and gameboard[destination1[0]][destination1[1]] == 0:
                    # retient la position initiale, la position qui peut être jouée, la position de la pièce prise et le type de pièce à déplacer
                    must_capture.append([self.number, [coords[1], coords[2]], angle1,
                                         destination1])
                if out_of_bounds2(destination2) == False and gameboard[angle2[0]][
                    angle2[1]] // 1 == self.opponent_number and gameboard[destination2[0]][destination2[1]] == 0:
                    # retient la position initiale, la position qui peut être jouée, la position de la pièce prise et le type de pièce à déplacer
                    must_capture.append([self.number, [coords[1], coords[2]], angle2,
                                         destination2])
                if out_of_bounds2(destination3) == False and gameboard[angle3[0]][
                    angle3[1]] // 1 == self.opponent_number and gameboard[destination3[0]][destination3[1]] == 0:
                    # retient la position initiale, la position qui peut être jouée, la position de la pièce prise et le type de pièce à déplacer
                    must_capture.append([self.number, [coords[1], coords[2]], angle3,
                                         destination3])
                if out_of_bounds2(destination4) == False and gameboard[angle4[0]][
                    angle4[1]] // 1 == self.opponent_number and gameboard[destination4[0]][destination4[1]] == 0:
                    # retient la position initiale, la position qui peut être jouée, la position de la pièce prise et le type de pièce à déplacer
                    must_capture.append([self.number, [coords[1], coords[2]], angle4,
                                         destination4])

            # permet de déterminer les dames pouvant capturer une pièce adverse
            elif coords[0] == self.number + 0.5:

                # recherche vers le haut et à droite:
                k = 0
                while out_of_bounds2([coords[1] + k + 1, coords[2] + k + 1]) == False and gameboard[coords[1] + k + 1][
                    coords[2] + k + 1] == 0:
                    k += 1
                if out_of_bounds2([coords[1] + k + 2, coords[2] + k + 2]) == False and gameboard[coords[1] + k + 1][
                    coords[2] + k + 1] // 1 == self.opponent_number and gameboard[coords[1] + k + 2][
                    coords[2] + k + 2] // 1 == 0:
                    compteur = 1
                    while out_of_bounds2([coords[1] + k + 2 + compteur, coords[2] + k + 2 + compteur]) == False and \
                            gameboard[coords[1] + k + 2 + compteur][coords[2] + k + 2 + compteur] == 0:
                        compteur += 1
                    # retient la position initiale, la position de l'adversaire qui peut être mangé, le type de pièce et le nombre de 0 derrière la cible
                    must_capture.append(
                        [self.number + 0.5, [coords[1], coords[2]], [coords[1] + k + 1, coords[2] + k + 1],
                         compteur])

                # recherche vers le haut et à gauche:
                k = 0
                while out_of_bounds2([coords[1] + k + 1, coords[2] - k - 1]) == False and gameboard[coords[1] + k + 1][
                    coords[2] - k - 1] == 0:
                    k += 1
                if out_of_bounds2([coords[1] + k + 2, coords[2] - k - 2]) == False and gameboard[coords[1] + k + 1][
                    coords[2] - k - 1] // 1 == self.opponent_number and gameboard[coords[1] + k + 2][
                    coords[2] - k - 2] // 1 == 0:
                    compteur = 1
                    while out_of_bounds2([coords[1] + k + 2 + compteur, coords[2] - k - 2 - compteur]) == False and \
                            gameboard[coords[1] + k + 2 + compteur][coords[2] - k - 2 - compteur] == 0:
                        compteur += 1
                    # retient la position initiale, la position de l'adversaire qui peut être mangé, le type de pièce et le nombre de 0 derrière la cible
                    must_capture.append(
                        [self.number + 0.5, [coords[1], coords[2]], [coords[1] + k + 1, coords[2] - k - 1],
                         compteur])

                # recherche vers le bas et à droite:
                k = 0
                while out_of_bounds2([coords[1] - k - 1, coords[2] + k + 1]) == False and gameboard[coords[1] - k - 1][
                    coords[2] + k + 1] == 0:
                    k += 1
                if out_of_bounds2([coords[1] - k - 2, coords[2] + k + 2]) == False and gameboard[coords[1] - k - 1][
                    coords[2] + k + 1] // 1 == self.opponent_number and gameboard[coords[1] - k - 2][
                    coords[2] + k + 2] // 1 == 0:
                    compteur = 1
                    while out_of_bounds2([coords[1] - k - 2 - compteur, coords[2] + k + 2 + compteur]) == False and \
                            gameboard[coords[1] - k - 2 - compteur][coords[2] + k + 2 + compteur] == 0:
                        compteur += 1
                    # retient la position initiale, la position de l'adversaire qui peut être mangé, le type de pièce et le nombre de 0 derrière la cible
                    must_capture.append(
                        [self.number + 0.5, [coords[1], coords[2]], [coords[1] - k - 1, coords[2] + k + 1],
                         compteur])

                # recherche vers le bas et à gauche:
                k = 0
                while out_of_bounds2([coords[1] - k - 1, coords[2] - k - 1]) == False and gameboard[coords[1] - k - 1][
                    coords[2] - k - 1] == 0:
                    k += 1
                if out_of_bounds2([coords[1] - k - 2, coords[2] - k - 2]) == False and gameboard[coords[1] - k - 1][
                    coords[2] - k - 1] // 1 == self.opponent_number and gameboard[coords[1] - k - 2][
                    coords[2] - k - 2] // 1 == 0:
                    compteur = 1
                    while out_of_bounds2([coords[1] - k - 2 - compteur, coords[2] - k - 2 - compteur]) == False and \
                            gameboard[coords[1] - k - 2 - compteur][coords[2] - k - 2 - compteur] == 0:
                        compteur += 1
                    # retient la position initiale, la position de l'adversaire qui peut être mangé, le type de pièce et le nombre de 0 derrière la cible
                    must_capture.append(
                        [self.number + 0.5, [coords[1], coords[2]], [coords[1] - k - 1, coords[2] - k - 1],
                         compteur])

        return must_capture
