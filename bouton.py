
### Différents boutons pour l'interface graphique

# Imports #
from tkinter import *
from random import choice
from bloc import Bloc
from file import File
from jeu import Jeu


### Fonctions appelées par les boutons de l'interface (logique du jeu uniquement)

# Fonction pour créer une nouvelle partie #
def nouvellePartie(jeu, listeprochain, listeProba):
    jeu.reinitialiser()
    listeprochain.relancer(listeProba)

# Fonction pour relancer les prochains blocs #
def relancer(listeprochain, listeProba):
    listeprochain.relancer(listeProba)

# Fonction qui applique un pouvoir sur le bloc cliqué #
# Renvoie True si le pouvoir a fonctionné, False sinon
def appliquerPouvoir(nom, jeu, ligne, colonne):
    if nom == "supprimer":
        return jeu.supprimerBloc(ligne, colonne)
    elif nom == "fusionner":
        return jeu.fusionnerPouvoir(ligne, colonne)
    elif nom == "bombe":
        return jeu.exploser(ligne, colonne)
    return False