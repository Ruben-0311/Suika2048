
### Différents boutons pour l'interface graphique

# Imports #
from tkinter import *
from random import choice
from bloc import Bloc
from file import File
from jeu import Jeu


# Fonction pour créer une nouvelle partie #
def nouvellePartie(jeu, listeprochain, grille, actualiser, actualiserHaut, actualiserProchains, scoreValeur, meilleurScoreValeur):  # Le meilleur score pourrait être utile pour la suite

    # Vidage la grille du jeu #
    for i in range(9):
        for j in range(7):
            jeu.grille[i][j] = ""

    # Réinitialisation la grille du haut #
    for j in range(7):
        jeu.grilleHaut[j] = ""
    jeu.grilleHaut[3] = choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32])
    # Réinitialisation la file
    listeprochain.file = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32]
    # Actualisation les affichages
    actualiser(9, 7, grille, jeu.DonnerGrille())
    actualiserHaut()
    actualiserProchains()
    scoreValeur.configure(text="0")

# Fonction pour poser une bombe #
def bombe(jeu, actualiser, actualiserHaut, actualiserProchains, grille, compteurBombes):
    blocsPresents = []

    # La bombe ne peut être posée que sur un bloc présent dans la grille #
    for i in range(9):
        for j in range(7):
            if jeu.grille[i][j] != "":
                blocsPresents.append((i, j))
    # Impossible de poser une bombe si la grille est vide
    if len(blocsPresents) == 0:
        return
    # Vérification du nombre de bombes restantes
    if bombesRestantes == 0:
        return
    # Explosion et suppression des blocs adjacents
    jeu.grille[i+1][j] = ""
    jeu.grille[i-1][j] = ""
    jeu.grille[i][j+1] = ""
    jeu.grille[i][j-1] = ""
    # On retire une bombe du stock
    bombesRestantes -= 1
    compteurBombes.configure(text="Bombes restantes : " + str(bombesRestantes[0]))
    # Actualisation
    actualiser(9, 7, grille, jeu.DonnerGrille())
    actualiserHaut()
    actualiserProchains()


# Fonction pour relancer les prochains blocs #
def relancer(listeprochain, historique, actualiserProchains, relancementsRestants, compteurRelancements):
    # Vérification du nombre de relancements restants
    if relancementsRestants[0] <= 0:
        return
    # Sauvegarde de la file
    historique.append(([ligne[:] for ligne in Jeu.grille],listeprochain.file[:]))
    # On mélange les prochains blocs
    listeprochain.file[0] = choice.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32])
    listeprochain.file[1] = choice.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32])
    listeprochain.file[2] = choice.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32])
    # On retire un relancement
    relancementsRestants[0] -= 1
    compteurRelancements.configure(text="Relancements restants : " + str(relancementsRestants[0]))
    actualiserProchains()

#### EN COURT

    