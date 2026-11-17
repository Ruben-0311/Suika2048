### Differents boutons pour l'interface graphique

from tkinter import *
from random import choice
from bloc import Bloc
from file import File
from jeu import Jeu


### Fonctions appelees par les boutons de l'interface

def nouvellePartie(jeu, listeprochain, listeProba):
    # Fonction pour creer une nouvelle partie
    jeu.reinitialiser() # Reinitialise la grille et le score de la partie
    listeprochain.relancer(listeProba) # Remplit a nouveau la file avec les prochains blocs possibles

def relancer(listeprochain, listeProba):
    # Fonction pour relancer les prochains blocs
    listeprochain.relancer(listeProba) # Remplace le contenu actuel de la file par une nouvelle selection de blocs


# Renvoie True si le pouvoir a fonctionne, False sinon
def appliquerPouvoir(nom, jeu, ligne, colonne):
    # Fonction qui applique un pouvoir sur le bloc clique, et qui transmet a la class jeu pour s'occuper d appliquer l'effet sur les blocs

    if nom == "supprimer": # Verifie si le pouvoir est suppression
        return jeu.supprimerBloc(ligne, colonne) # Supprime aux coordonnées

    elif nom == "fusionner": # Verifie si le pouvoir est fusion
        return jeu.fusionnerPouvoir(ligne, colonne) # Fusionne si possible en fonction des coordonnees


    elif nom == "bombe": # Verifie si le pouvoir est bombe
        return jeu.exploser(ligne, colonne) # Detruit le bloc selectionne et ses 4 voisins 


    else:
        assert False, "Nom de pouvoir inconnu" # Si le nom ne correspond pas a un pouvooir, renvoie l'erreur
