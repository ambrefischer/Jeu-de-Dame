# -*- coding: utf-8 -*-
"""
Project : Jeu de Dames

@authors: Ambre Fischer & Charles Fortier (groupe TD 2)
"""

def display_message(message, color="black"):
    """
    Affiche le message via la fonction print.

    Paramètres
    ----------
    message: str
        Définit le message que l'on veut afficher.

    color: str
        Définit la couleur du message à afficher
    """

    print(" ")
    print(" ")
    print("\033[1;" + select_color(color) + ";48m " + message + "  \n")
    print(" ")


def select_color(color):
    """
    Détermine la couleur voulue

    Paramètres
    ----------
    color: str
        Définit la couleur du message que l'on veut afficher.
    """

    colors = {
        "grey": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "purple": "35",
        "cyan": "36",
        "white": "37",
        "black": "0",
    }
    return colors[color]


def display_beginning():
    """
    Affiche le message du début.

    Paramètres
    ----------
    Aucun
    """

    print(''' 
                     _                          _____ _                _               
     /\             | |                ___     / ____| |              | |            _ 
    /  \   _ __ ___ | |__  _ __ ___   ( _ )   | |    | |__   __ _ _ __| | ___  ___  (_)
   / /\ \ | '_ ` _ \| '_ \| '__/ _ \  / _ \/\ | |    | '_ \ / _` | '__| |/ _ \/ __|    
  / ____ \| | | | | | |_) | | |  __/ | (_>  < | |____| | | | (_| | |  | |  __/\__ \  _ 
 /_/   _\_\_| |_| |_|_.__/|_|  \___|__\___/\/  \_____|_| |_|\__,_|_|  |_|\___||___/ (_)
      | |                | |      |  __ \                                              
      | | ___ _   _    __| | ___  | |  | | __ _ _ __ ___   ___  ___                    
  _   | |/ _ \ | | |  / _` |/ _ \ | |  | |/ _` | '_ ` _ \ / _ \/ __|                   
 | |__| |  __/ |_| | | (_| |  __/ | |__| | (_| | | | | | |  __/\__ \                   
  \____/ \___|\__,_|  \__,_|\___| |_____/ \__,_|_| |_| |_|\___||___/                   
  ______ _   _  _____ _______         ____           _                                 
 |  ____| \ | |/ ____|__   __|/\     |  _ \         | |                                
 | |__  |  \| | (___    | |  /  \    | |_) |_ __ ___| |_ __ _  __ _ _ __   ___         
 |  __| | . ` |\___ \   | | / /\ \   |  _ <| '__/ _ \ __/ _` |/ _` | '_ \ / _ \        
 | |____| |\  |____) |  | |/ ____ \  | |_) | | |  __/ || (_| | (_| | | | |  __/        
 |______|_| \_|_____/   |_/_/  __\_\ |____/|_|  \___|\__\__,_|\__, |_| |_|\___|        
 |  __ \         (_)    | |   |_   _|      / _|      /_ |   /\ __/ |                   
 | |__) | __ ___  _  ___| |_    | |  _ __ | |_ ___    | |  /  \___/                    
 |  ___/ '__/ _ \| |/ _ \ __|   | | | '_ \|  _/ _ \   | | / /\ \                       
 | |   | | | (_) | |  __/ |_   _| |_| | | | || (_) |  | |/ ____ \                      
 |_|   |_|  \___/| |\___|\__| |_____|_| |_|_| \___/   |_/_/    \_\                     
                _/ |                                                                   
               |__/                                                                                                   
    
Bienvenue sur le meilleur jeu qui existe.    
    ''')
