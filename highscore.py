# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:11:46 2020

@author: Ambre
"""
#"w" écrase l'ancienne sauvegarde
#"a" garde l'ancienne sauvegarde

from utils import *
import numpy as np


def add_player(nickname, score):
    file = open("classement.txt", "a")
    file.write(nickname)
    file.write(" : ")
    file.write(score)
    file.write("\n")
    file.close()
    
    
def view_highscore():
    display_message("Voici les meilleurs classements sur ce jeu :")
    with open("classement.txt", "r") as file:
        for line in file:
            print(line)
            
            
            
            
       


