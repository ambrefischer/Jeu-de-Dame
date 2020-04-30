# -*- coding: utf-8 -*-
"""
Project : Jeu de Dames

@authors: Ambre Fischer & Charles Fortier (groupe TD 2)
"""

#"w" écrase l'ancienne sauvegarde
#"a" garde l'ancienne sauvegarde

from utils import *


def add_player(nickname, score):
    """
    Ajoute le joueur dans le fichier texte des meilleurs scores.

    Paramètres
    ----------
    nickname: str
        Contient le nom qui apparaîtra sur le classement.

    score: int
        Contient le score qui apparaîtra sur le classement.
    """

    file = open("classement.txt", "a")
    file.write(nickname)
    file.write(" : ")
    file.write(str(score))
    file.write("\n")
    file.close()
    
    
def view_highscore(appli):
    """
    Permet de visualiser les meilleurs scores.

    Paramètres
    ----------
    Aucun
    """

    display_message("Voici les meilleurs classements sur ce jeu :")
    with open("classement.txt", "r") as file:
        for line in file:
            tot_line = line
    appli.textBrowser.setText("Voici les meilleurs classements sur ce jeu : \n" + tot_line)
            
            
            
            
       


