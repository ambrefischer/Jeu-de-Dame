# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:50:37 2020

@author: Ambre

suggestion d'idées :
    on peut suggérer au joueur quels mouvement il peut faire
    créer un fichier avec les dix meilleurs joueurs
    musique
    feu d'artifice de fin
    demander d'obtenir les règles du jeu
    si le joueur ne peut plus bouger mais il lui reste des pions, il perd la partie.
    
    
ne pas oublier :
    faire les figures demandés
    obliger à manger si possible
    pouvoir manger une dame int --> float ?
"""

from piece import Checker, King
from player import Human  # , IA
from utils import *
from gameboard import *
from constants import *


def play_with():
    choice = input("Voulez-vous jouer contre un 'joueur' ou un 'ordi' ? ")

    # Selection de l'adversaire
    if choice == "joueur":
        return Human(1, 0)
    else:
        display_message("Les autres modes ne sont pas encore disponibles...")
        return Human(1, 0)


def initialisation():
    display_message("Let's the game begin !")

    # Création du plateau
    gameboard = create_gameboard()
    view(gameboard)
    
    # Définition du tour du joueur
    player_turn = {"player_number": 1.0, "status": "still playing"}
    
    return {"player_turn": player_turn, "gameboard": gameboard}


def who_plays(player_turn, j1, j2):
    # Tour du joueur 1
    if player_turn["player_number"] % 2 == 1.0:
        return j1
    # Tour du joueur 2
    else:
        return j2
    
    
def choice_piece(game, make_a_move, player):
    if make_a_move["type"] == CHECKER:
        piece = Checker(game["s_row"], game["s_column"],
                        game["t_row"], game["t_column"], player.number)
    else:
        piece = King(game["s_row"], game["s_column"],
                     game["t_row"], game["t_column"], player.number)
    return piece

    
def play_turn(player_turn, j1, j2, gameboard):
        # Détermination de à qui le tour
        player = who_plays(player_turn, j1, j2)

        # Le joueur peut rejouer s'il mange un pion adverse.
        while player_turn["status"] == STILL_PLAYING:
            display_message(
                "Joueur %d, à vous de jouer. Votre score est de %d."
                % (player.number, player.score)
            )

            # Choix du déplacement
            game = player.play(gameboard)
            make_a_move = player.one_turn(game["s_row"], game["s_column"],
                                          game["t_row"], game["t_column"], gameboard)

            # Problème dans les coordonnées
            while make_a_move["message"] == PB:
                view(gameboard)
                game = player.play(gameboard)
                make_a_move = player.one_turn(game["s_row"], game["s_column"],
                                              game["t_row"], game["t_column"], gameboard)

            # Acceptation des coordonnées : la pièce est un pion ou une dame
            piece = choice_piece(game, make_a_move, player)

            # Si le joueur désire se déplacer.
            if make_a_move["message"] == I_M_ON_MY_WAY:
                gameboard = piece.move(gameboard)
                player_turn["status"] = END_OF_TURN

            # Ou le joueur désire manger un pion adverse.
            else:
                gameboard = piece.move(gameboard)
                gameboard = piece.capture(gameboard, make_a_move)
                player.win_one_point()

            # Vérification si le pion ne devient pas une dame
            if make_a_move["type"] == CHECKER and piece.check_king():
                gameboard = piece.become_king(gameboard)

            view(gameboard)
        player_turn["player_number"] += 1
        player_turn["status"] = STILL_PLAYING

    
        

    