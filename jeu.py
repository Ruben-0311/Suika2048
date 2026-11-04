### Création du jeu (grillage, dépot de blocs, etc...)

from bloc import *
from file import *

listeProba = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32]

class Jeu:
    def __init__(self):
        # Grille du jeu 9 par 7
        self.grille = [["" for i in range(7)] for j in range(9)]

        # Grille du haut 1 par 7
        self.grilleHaut = ["" for i in range(7)]
        self.grilleHaut[3] = random.choice(listeProba)

        # Score de la partie
        self.score = 0


    def DonnerGrille(self):
        return self.grille

    def DonnerGrilleHaut(self):
        return self.grilleHaut

    def trouverPosition(self, colonne):
        for ligne in range(8, -1, -1):
            if self.grille[ligne][colonne] == "":
                return ligne

        return None

    def deposerBloc(self, colonne, valeur):
        ligne = self.trouverPosition(colonne)

        if ligne is None:
            return False

        self.grille[ligne][colonne] = valeur

        # Fusion du bloc qui vient d'être lâché avec ses voisins
        self.score += self.fusionnerBloc(ligne, colonne)

        return True


    ### Fusion des blocs ###

    # Cherche un voisin de même valeur : bas, puis gauche, puis droite
    # Renvoie sa position (ligne, colonne) ou None s'il n'y en a pas
    def trouverVoisinIdentique(self, ligne, colonne):
        valeur = self.grille[ligne][colonne]

        # (décalage de ligne, décalage de colonne) dans l'ordre de priorité
        for (decalageLigne, decalageColonne) in [(1, 0), (0, -1), (0, 1)]:
            l = ligne + decalageLigne
            c = colonne + decalageColonne

            # On vérifie qu'on ne sort pas de la grille
            if 0 <= l < 9 and 0 <= c < 7:
                if self.grille[l][c] == valeur:
                    return (l, c)

        return None

    # Fait retomber les blocs d'une colonne pour boucher les trous
    def appliquerGravite(self, colonne):
        # On récupère les valeurs de la colonne, du bas vers le haut
        valeurs = []
        for ligne in range(8, -1, -1):
            if self.grille[ligne][colonne] != "":
                valeurs.append(self.grille[ligne][colonne])

        # On réécrit la colonne en partant du bas
        for ligne in range(8, -1, -1):
            indice = 8 - ligne
            if indice < len(valeurs):
                self.grille[ligne][colonne] = valeurs[indice]
            else:
                self.grille[ligne][colonne] = ""

    # Fusionne le bloc en (ligne, colonne) avec ses voisins identiques
    # Le bloc absorbe les autres. Renvoie les points gagnés
    def fusionnerBloc(self, ligne, colonne):
        points = 0
        voisin = self.trouverVoisinIdentique(ligne, colonne)

        while voisin is not None:
            ligneVoisin, colonneVoisin = voisin
            nouvelleValeur = self.grille[ligne][colonne] * 2
            points += nouvelleValeur

            if ligneVoisin > ligne:
                # Voisin du bas : le bloc fusionné prend sa place
                self.grille[ligne][colonne] = ""
                self.grille[ligneVoisin][colonneVoisin] = nouvelleValeur
                ligne = ligneVoisin
            else:
                # Voisin de gauche ou de droite : le bloc reste où il est
                self.grille[ligne][colonne] = nouvelleValeur
                self.grille[ligneVoisin][colonneVoisin] = ""
                self.appliquerGravite(colonneVoisin)

            # On regarde si le nouveau bloc peut encore fusionner
            voisin = self.trouverVoisinIdentique(ligne, colonne)

        return points




        ### Pouvoirs ###

    # Remet la grille et le score à zéro
    def reinitialiser(self):
        self.grille = [["" for i in range(7)] for j in range(9)]
        self.score = 0

    # Pouvoir "Supprimer" : retire un bloc
    def supprimerBloc(self, ligne, colonne):
        if self.grille[ligne][colonne] == "":
            return False

        self.grille[ligne][colonne] = ""
        self.appliquerGravite(colonne)
        return True

    # Pouvoir "Fusionner" : fusionne le bloc cliqué avec ses voisins identiques
    # (même priorité que pour un bloc lâché : bas, gauche, droite)
    def fusionnerPouvoir(self, ligne, colonne):
        if self.grille[ligne][colonne] == "":
            return False

        if self.trouverVoisinIdentique(ligne, colonne) is None:
            return False

        self.score += self.fusionnerBloc(ligne, colonne)
        return True

    # Pouvoir "Bombe" : supprime le bloc cliqué et les 4 blocs qui l'entourent
    def exploser(self, ligne, colonne):
        if self.grille[ligne][colonne] == "":
            return False

        for (decalageLigne, decalageColonne) in [(0, 0), (1, 0), (-1, 0), (0, -1), (0, 1)]:
            l = ligne + decalageLigne
            c = colonne + decalageColonne
            if 0 <= l < 9 and 0 <= c < 7:
                self.grille[l][c] = ""

        # Tous les blocs retombent
        for c in range(7):
            self.appliquerGravite(c)
        return True