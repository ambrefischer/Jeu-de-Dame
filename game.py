# -*- coding: utf-8 -*-
"""
Project : Jeu de Dames

@authors: Ambre Fischer & Charles Fortier (groupe TD 2)
"""

from piece import Checker, King
from player import Human, IA
from gameboard import *
from constants import *
from highscore import *
from appIHM import MonAppli
import numpy as np



def play_with():
    """
    Demande à l'utilisateur s'il désire jouer contre un autre joueur ou contre un ordinateur.

    Paramètres
    ----------
    Aucun

    Renvoie
    -------
    J2: player.Human
        Le joueur adverse est créé sous la forme d'un Objet. L'Objet IA n'est pas encore implémenté.
    """

    choice = input("Voulez-vous jouer contre un 'joueur' ou un 'ordi' ? ")

    # Selection de l'adversaire
    if choice == "joueur":
        return Human(1, 0, 2, 1)

    elif choice == "ordi":
        correct = False
        while correct == False:
            level_choice = input("veuillez choisir la difficulté de l'ordi parmi celles proposées: 'facile' \n")
            if level_choice == "facile":
                return IA(1,0,2,1,"facile")
            else: display_message("Le niveau de difficulté choisi n'est pas disponible")

    display_message("Les autres modes ne sont pas encore disponibles...")
    return Human(1, 0, 2, 1)

def initialisation(J1, J2, appli):
    """
    Initialise le jeu.

    Paramètres
    ----------
    J1: player.Human
        Caractérise le joueur 1.

    J2: player.Human
        Caractérise le joueur 2.

    Renvoie
    -------
    d: dict
        "player_turn": dict
            "player_number": float
                modulo 2 indique le numéro du joueur entrain de jouer.
                    1.0: le joueur 1 est entrain de jouer.
                    2.0: le joueur 2 est entrain de jouer.
            "status": str
                indique le status du joueur entrain de jouer.
                    None: pas de status particulier (uniquement pour l'initialisation).
                    STILL_PLAYING: le joueur peut rejouer car il peut reprendre une pièce adverse.
                    END_OF_TURN: le joueur a fini son tour.

        "gameboard": array
            contient le plateau du jeu en cours

    """

    #Visualisation des meilleurs scores.
    view_highscore(appli)

    # Création du plateau
    gameboard = create_gameboard(J1, J2)
    view(gameboard)

    # Définition du tour du premier joueur
    first_turn = {"player_number": 2.0, "status": None}

    return {"player_turn": first_turn, "gameboard": gameboard}


def who_plays(player_turn, J1, J2):
    """
    Définit le joueur qui doit jouer.

    Paramètres
    ----------
    player_turn: dict
        Contient le numéro du joueur qui doit jouer.

    J1, J2: player.Human
        Caractérisent les joueurs.

    Renvoie
    -------
    j: player.Human
        L'Objet joueur qui doit faire son tour.

    Note
    -------
    Pour définir le tour du joueur on incrémente player_number à chaque fin de tour
    et à chaque début de tour on détermine si player_number modulo 2
    renvoie le joueur 1 ou le joueur 2.
    """

    # Tour du joueur 1
    if player_turn["player_number"] % 2 == 1.0:
        return J1
    # Tour du joueur 2
    return J2


def choice_piece(coords, make_a_move, player):
    """
    Crée la pièce correspondante aux attentes du joueur.

    Paramètres
    ----------
    coords: dict
        Contient les coordonnées de la pièce à bouger et de la case ciblée pour le mouvement.

    make_a_move: dict
        Contient via la clé "type" la catégorie de pièce que le joueur souhaite déplacer.

    player: player.Human
        Contient les caractéristiques du joueur entrain de jouer.

    Renvoie
    -------
    Piece: piece.Piece
        L'Objet Piece peut être soit un Checker (pion) soit un King (dame).
    """

    if make_a_move["type"] == CHECKER:
        Piece = Checker(coords["s_row"], coords["s_column"],
                        coords["t_row"], coords["t_column"], player.number)
    else:
        Piece = King(coords["s_row"], coords["s_column"],
                     coords["t_row"], coords["t_column"], player.number)
    return Piece


def play_turn(player_turn, J1, J2, gameboard, appli):
    """
    Simule le tour entier d'un joueur.

    Paramètres
    ----------
    player_turn: dict
        Contient le numéro du joueur qui doit jouer.

    J1, J2: player.Human
        Caractérisent les joueurs.

    gameboard: array
        Définit le plateau de jeu en cours.
    """

    # Détermination du joueur qui doit jouer le tour
    player = who_plays(player_turn, J1, J2)
    coords_pieces = player.where_piece(gameboard)[0]
    must_capture = player.must_capture(gameboard)

    display_message(
        "Joueur %d, à vous de jouer. Votre score est de %d."
        % (player.number, player.score)
    )

    #Si le joueur est un humain
    if isinstance(player, Human) == True:
        human_play_turn(player_turn, player, gameboard, appli, coords_pieces, must_capture)

    # Si le joueur est l'ordi
    else:
        IA_play_turn(player_turn, player, gameboard, coords_pieces, must_capture)


def human_play_turn(player_turn, player, gameboard, appli, coords_pieces, must_capture):
    # Choix du déplacement
    coords = {"s_row": player.choose_s_row(appli), "s_column": player.choose_s_column(appli), \
              "t_row": player.choose_t_row(appli), "t_column": player.choose_t_column(appli)}

    make_a_move = player.check_coords(coords["s_row"], coords["s_column"],
                                coords["t_row"], coords["t_column"], gameboard, coords_pieces, must_capture)

    # Problème dans les coordonnées
    while make_a_move["message"] == PB:
        view(gameboard)
        coords = {"s_row": player.choose_s_row(gameboard), "s_column": player.choose_s_column(gameboard), \
                  "t_row": player.choose_t_row(gameboard), "t_column": player.choose_t_column(gameboard)}
        make_a_move = player.check_coords(coords["s_row"], coords["s_column"],
                                      coords["t_row"], coords["t_column"], gameboard, coords_pieces, must_capture)

    # Acceptation des coordonnées : la pièce est un pion ou une dame
    Piece = choice_piece(coords, make_a_move, player)

    # Si le joueur désire se déplacer.
    if make_a_move["message"] == I_M_ON_MY_WAY:
        gameboard = Piece.move(gameboard)

    # Ou le joueur désire manger un pion adverse.
    elif make_a_move["message"] == I_CAPTURE:
        gameboard = Piece.move(gameboard)
        gameboard = Piece.capture(gameboard, make_a_move)
        player.win_one_point()
        #Vérification si le joueur peut rejouer, dans ce cas : "status" = STILL_PLAYING
        #avec son pion.
        if make_a_move["type"] == CHECKER:
            play_again = player.can_capture_with_checker(gameboard, coords["t_row"], coords["t_column"])
            if play_again["bool"] == True:
                player_turn["status"] = STILL_PLAYING
                display_message("Vous pouvez rejouer avec le même pion uniquement pour manger un pion adverse.")
        #avec sa dame.
        else:
            play_again = player.can_capture_with_king(gameboard, coords["t_row"], coords["t_column"])
            if play_again["bool"] == True:
                player_turn["status"] = STILL_PLAYING
                display_message("Vous pouvez rejouer avec le même pion uniquement pour manger un pion adverse.")


    # Vérification si le pion ne devient pas une dame
    if make_a_move["type"] == CHECKER and Piece.check_king():
        gameboard = Piece.become_king(gameboard)

    #Le joueur est dans le cas où il peut rejouer.
    if player_turn["status"] == STILL_PLAYING:
        view(gameboard)
        play_turn_again(play_again, player_turn, player, coords["t_row"], coords["t_column"], gameboard)

    #Le joueur a fini de jouer.
    player_turn["status"] = END_OF_TURN


def IA_play_turn(player_turn, player, gameboard, coords_pieces, must_capture):

    possible_capture = len(must_capture)

    #Si le pion se déplace juste.
    if possible_capture == 0:
        possible_move = []
        nb_pieces = player.where_piece(gameboard)[1]
        #On teste tous les coups possibles de toutes les pièces.
        for index in range(nb_pieces):
            coords = coords_pieces[index + 1]
            row_possible = coords[1] + player.factor
            col_possible = coords[2] + 1
            #déplacement à droite
            if col_possible < 10 and gameboard[row_possible][col_possible] == 0:
                possible_move.append([index + 1, row_possible, col_possible])
            col_possible = coords[2] - 1
            #déplacement à gauche
            if col_possible >= 0 and gameboard[row_possible][col_possible] == 0:
                possible_move.append([index + 1, row_possible, col_possible])
        #On détermine quel mouvement l'ordi peut faire.
        n = len(possible_move)
        index2 = np.random.randint(0, n)  # détermine aléatoirement le coup joué
        print(possible_move)
        move_kept = possible_move[index2]

        Piece = Checker(coords_pieces[move_kept[0]][1], coords_pieces[move_kept[0]][2],
                        move_kept[1], move_kept[2], player.number)
        gameboard = Piece.move(gameboard)

        if Piece.check_king() == True:
            Piece.become_king(gameboard)

    #La pièce peut prendre une pièce adverse.
    else:
        # On détermine aléatoirement la pièce qui sera déplacée et celle qui sera prise
        index2 = np.random.randint(0, possible_capture)

        #Si la pièce est un pion.
        if must_capture[index2][0] == player.number:
            Piece = Checker(must_capture[index2][1][0], must_capture[index2][1][1], must_capture[index2][3][0],
                            must_capture[index2][3][1], player.number)
            gameboard = Piece.move(gameboard)
            gameboard[must_capture[index2][2][0]][must_capture[index2][2][1]] = 0
            player.win_one_point()

        #Si la pièce est une dame.
        else:
            # nombre de position possibles pour la dame après la prise
            compt = must_capture[index2][3]
            # choisi une position aléatoire
            add = np.random.randint(1, compt + 1)
            sign_row = (must_capture[index2][1][0] - must_capture[index2][2][0]) / abs(
                must_capture[index2][1][0] - must_capture[index2][2][0])
            sign_column = (must_capture[index2][1][1] - must_capture[index2][2][1]) / abs(
                must_capture[index2][1][1] - must_capture[index2][2][1])

            Piece = King(must_capture[index2][1][0], must_capture[index2][1][1],
                         must_capture[index2][2][0] + sign_row * add,
                         must_capture[index2][2][1] + sign_column * add, player.number)
            gameboard = Piece.move(gameboard)
            gameboard[must_capture[index2][2][0]][must_capture[index2][2][1]] = 0
            player.win_one_point()

def play_turn_again(play_again, player_turn, player, s_row, s_column, gameboard):
    """
    Simule la suite du tour d'un joueur lorsque celui-ci peut continuer de jouer.

    Paramètres
    ----------
    play_again: dict
        Est déterminé par la méthode player.can_capture_with_checker
            ou player.can_capture_with_king.
        Contient l'emplacement de la pièce adverse à prendre.

    player_turn: dict
        Contient le numéro du joueur qui doit jouer.

    player: player.Human
        Caractérise le joueur entrain de jouer.

    s_row, s_column: int
        Caractérise les coordonées de la pièce qui peut rebouger.

    gameboard: array
        Définit le plateau de jeu en cours.
    """

    #Demande de rentrer des coordonnées pour la case ciblée.
    coords_pieces = player.where_piece(gameboard)[0]
    must_capture = player.must_capture(gameboard)
    coords_again = {"t_row": player.choose_t_row(gameboard), "t_column": player.choose_t_column(gameboard)}
    make_another_move = player.check_coords(s_row, s_column, coords_again["t_row"], coords_again["t_column"],
                                            gameboard, coords_pieces, must_capture)

    #Si les coordonnées ne remplissent pas les conditions du jeu ou bien que le joueur décide de ne pas jouer
    # le coup obligatoire alors il doit redonner des coordonnées.
    while make_another_move["message"] == PB or (\
            make_another_move["target"] != play_again["target_rd"] \
            and make_another_move["target"] != play_again["target_ld"] \
            and make_another_move["target"] != play_again["target_ru"] \
            and make_another_move["target"] != play_again["target_lu"]):
        display_message("Vous êtes obligé de manger une pièce adverse.")
        view(gameboard)
        coords_again = {"t_row": player.choose_t_row(gameboard), "t_column": player.choose_t_column(gameboard)}
        make_another_move = player.check_coords(s_row, s_column, coords_again["t_row"], coords_again["t_column"],
                                                gameboard, coords_pieces, must_capture)

    # Acceptation des coordonnées : la pièce est un pion ou une dame
    coords_again_all = {"s_row": s_row, "s_column": s_column, "t_row": coords_again["t_row"], "t_column": coords_again["t_column"]}
    Piece = choice_piece(coords_again_all, make_another_move, player)

    #Le joueur mange forcément l'adversaire.
    gameboard = Piece.move(gameboard)
    gameboard = Piece.capture(gameboard, make_another_move)
    player.win_one_point()

    #Le tour s'arrête si le joueur ne peut plus rejouer.
    #la pièce a rejouer est un pion
    if make_another_move["type"] == CHECKER:
        play_again = player.can_capture_with_checker(gameboard, coords_again["t_row"], coords_again["t_column"])
        if not play_again["bool"] == True:
            player_turn["status"] = END_OF_TURN
            display_message("Vous avez fini votre tour.")
            display_message("Joueur %d, votre score est de %d." % (player.number, player.score))
    #la piece à rejouer est une dame
    else:
        play_again = player.can_capture_with_king(gameboard, coords_again["t_row"], coords_again["t_column"])
        if not play_again["bool"] == True:
            player_turn["status"] = END_OF_TURN
            display_message("Vous avez fini votre tour.")
            display_message("Joueur %d, votre score est de %d." % (player.number, player.score))


    # Vérification si le pion ne devient pas une dame
    if make_another_move["type"] == CHECKER and Piece.check_king():
        gameboard = Piece.become_king(gameboard)

    #rejouer si l'on peut
    while player_turn["status"] == STILL_PLAYING:
        display_message("Vous pouvez rejouer avec le même pion uniquement pour manger.")
        view(gameboard)
        play_turn_again(play_again, player_turn, player, coords_again["t_row"], coords_again["t_column"], gameboard)

