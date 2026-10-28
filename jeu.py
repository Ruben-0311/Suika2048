from bloc import Bloc
from file import File


class Jeu:
    def __init__(self):
        self.lignes = 9
        self.colonnes = 7

        # Grille de jeu
        self.grille = [
            ["" for i in range(self.colonnes)] for j in range(self.lignes)]

        # Score actuel
        self.score = 0

        # File des prochains blocs
        self.file = File()