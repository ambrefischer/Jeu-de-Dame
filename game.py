# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:50:37 2020

@author: Ambre

suggestion d'idées :
    on peut suggérer au joueur quels mouvement il peut faire
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


if __name__ == "__main__":
    display_beginning()
    display_message("Bienvenue sur le meilleur jeu qui existe.")
    choice = input("Voulez-vous jouer contre un 'joueur' ou un 'ordi' ? ")

    # Selection de l'adversaire
    if choice == "joueur":
        j1 = Human(1, 0)
    else:
        display_message("Les autres modes ne sont pas encore disponibles...")
        j1 = Human(1.0, 0)
    j2 = Human(2.0, 0)

    display_message("Let's the game begin !")

    # Création du plateau
    gameboard = create_gameboard()
    view(gameboard)

    # Définition du tour du joueur
    player_turn = {"player_number": 1.0, "status": "still playing"}
    # Début du jeu
    while j1.score < 20 or j2.score < 20:
        # Tour du joueur 1
        if player_turn["player_number"] % 2 == 1.0:
            player = j1
        # Tour du joueur 2
        else:
            player = j2

        # Le joueur peut rejouer si il mange un pion adverse.
        while player_turn["status"] == "still playing":
            display_message(
                "Joueur %d, à vous de jouer. Votre score est de %d."
                % (player.number, player.score)
            )

            # Choix du déplacement
            game = player.play(gameboard)
            make_a_move = player.one_turn(game["s_row"], game["s_column"],
                                          game["t_row"], game["t_column"], gameboard)

            # Problème dans les coordonnées
            while make_a_move["message"] == "pb":
                game = player.play(gameboard)
                view(gameboard)
                make_a_move = player.one_turn(game["s_row"], game["s_column"],
                                              game["t_row"], game["t_column"], gameboard)

            # Acceptation des coordonnées : la pièce est un pion ou une dame
            if make_a_move["type"] == "Checker":
                piece = Checker(game["s_row"], game["s_column"],
                                game["t_row"], game["t_column"], player.number)
            else:
                piece = King(game["s_row"], game["s_column"],
                             game["t_row"], game["t_column"], player.number)

            # Si le joueur désire se déplacer.
            if make_a_move["message"] == "I'm on my way":
                gameboard = piece.move(gameboard)
                player_turn["status"] = "end of play"

            # Ou le joueur désire manger un pion adverse.
            else:
                gameboard = piece.move(gameboard)
                gameboard = piece.capture(gameboard, make_a_move)
                player.win_one_point()

            # Vérification si le pion ne devient pas une dame
            if make_a_move["type"] == "Checker" and piece.check_king():
                gameboard = piece.become_king(gameboard)

            view(gameboard)
        player_turn["player_number"] += 1
        player_turn["status"] = "still playing"

    # Comdition de gagne
    if j1.score < j2.score:
        display_message("Le joueur 2 a gagné.", "green")
    else:
        display_message("Le joueur 1 a gagné.", "blue")
