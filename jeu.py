from bloc import *
from file import *

listeProba = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32]

class Jeu:
    def __init__(self):
        # Grille du jeu 9 par 7
        self.grille = [["" for i in range(7)] for j in range(9)]

        # Grille du haut 1 par 7
        self.grilleHaut = ["" for i in range(7)]
        self.grilleHaut[0] = random.choice(listeProba)

    def get_grille(self):
        return self.grille

    def get_grille_haut(self):
        return self.grilleHaut