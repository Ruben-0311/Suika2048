### Creation du jeu (grille, depôt de blocs, etc...)

from bloc import *
from file import *

listeProba = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32] # Liste des proba des blocs


class Jeu:
    ''' Classe qui s'occupe du jeu, ses regles, la gestion de tous les elements y etant raccordes'''
    def __init__(self):
        self.grille = [["" for i in range(7)] for j in range(9)] # Creation de la grille principale de 9 lignes et 7 colonnes
        self.grilleHaut = ["" for i in range(7)] # Creation de la grille superieure qui contient le prochain bloc
        self.grilleHaut[3] = random.choice(listeProba) # Placement aleatoire du premier bloc au centre de la grille superieure
        self.score = 0 # score = 0

    #### Fonctions pour gerer la grille et le score ####
    def DonnerGrille(self):
        # Renvoie la grille principale du jeu
        return self.grille

    def DonnerGrilleHaut(self):
        # Renvoie la grille de depot des blocs
        return self.grilleHaut

    def trouverPosition(self, colonne):
        # Cherche la premiere case vide d'une colonne en partant du bas
        for ligne in range(8, -1, -1):
            if self.grille[ligne][colonne] == "":
                return ligne # Renvoie le numero de la ligne si une place est disponible

        return None # Renvoie None si la colonne est entierement remplie

    def estTerminee(self):
        # Verifie si toutes les colonnes sont pleines, si oui termine la partie
        return all(
            self.trouverPosition(colonne) is None
            for colonne in range(7)
        )

    
    def deposerBloc(self, colonne, valeur):
        # Cherche a deposer le bloc dans la colonne choisie
        ligne = self.trouverPosition(colonne) # Recherche la premiere case disponible dans la colonne


        # Si aucune case n'est disponible, le bloc ne peut pas être depose
        if ligne is None:
            return False

        # Place le bloc dans la case trouvee
        self.grille[ligne][colonne] = valeur

        # Cherche les fusions possibles et ajoute les points gagnes au score
        self.score += self.fusionnerBloc(ligne, colonne)

        return True


    ### Fusion des blocs ###
    def trouverVoisinIdentique(self, ligne, colonne):
        # On cherche si le bloc a un voisin identique, si oui renvoie ses coordonnees
        valeur = self.grille[ligne][colonne] # Recupere les coordonnees du bloc que l'on souhaite fusionner

        # Definit les deplacements possibles dans l'ordre de priorite
        # Chaque couple correspond a (decalage de ligne, decalage de colonne)
        for (decalageLigne, decalageColonne) in [(1, 0), (0, -1), (0, 1)]:
            l = ligne + decalageLigne
            c = colonne + decalageColonne

            # Verifie que les coordonnees du voisin restent dans la grille
            if 0 <= l < 9 and 0 <= c < 7:
                # Verifie si le voisin possede la même valeur
                if self.grille[l][c] == valeur:
                    return (l, c)

        return None

    def appliquerGravite(self, colonne):
        # But : faire tomber les blocs progrssivement

        # Recupere les valeurs presentes dans la colonne, en partant du bas
        valeurs = []
        for ligne in range(8, -1, -1):
            if self.grille[ligne][colonne] != "":
                valeurs.append(self.grille[ligne][colonne])

        # Reorganise la colonne en plaçant les blocs les uns sur les autres
        for ligne in range(8, -1, -1):
            # Calcule l'indice de la valeur a replacer
            indice = 8 - ligne

            # S'il reste des blocs a placer, on les remet dans la grille
            if indice < len(valeurs):
                self.grille[ligne][colonne] = valeurs[indice]
            else:
                # Les cases restantes sont laissees vides
                self.grille[ligne][colonne] = ""

    
    def fusionnerBloc(self, ligne, colonne):
        #Fait absorber le bloc voisin a celui qui vient d'etre laché par ce dernier
        points = 0 # nbr de points gagnes avec fusion

        voisin = self.trouverVoisinIdentique(ligne, colonne) # Recherche un premier voisin identique

        # Continue tant qu'un voisin identique peut être trouve
        while voisin is not None:
            ligneVoisin, colonneVoisin = voisin # Recupere les coordonnees du bloc voisin
            nouvelleValeur = self.grille[ligne][colonne] * 2 # Calcule la nouvelle valeur du bloc apres la fusion
            points += nouvelleValeur            # ajoute la nouvelle valeur au nombre de points gagnes

            if ligneVoisin > ligne:
                # Si le voisin est en dessous, le bloc fusionne prend sa place
                self.grille[ligne][colonne] = ""
                self.grille[ligneVoisin][colonneVoisin] = nouvelleValeur

                ligne = ligneVoisin # Met a jour la ligne du bloc fusionne.

            else:
                self.grille[ligne][colonne] = nouvelleValeur # Si le voisin est a gauche ou a droite, le bloc reste a sa place
                self.grille[ligneVoisin][colonneVoisin] = "" # Supprime le bloc voisin qui vient d'être absorbe
                self.appliquerGravite(colonneVoisin) # Fait retomber les blocs de la colonne ou le voisin a ete supprime

            voisin = self.trouverVoisinIdentique(ligne, colonne) # Verifie si le bloc fusionne peut encore fusionner avec un autre voisin

        return points # Renvoie le total des points gagnes

    

    def reinitialiser(self):
        # Remet la grille principale et le score a zero
        # Recree une grille vide de 9 lignes et 7 colonnes
        self.grille = [["" for i in range(7)] for j in range(9)]

        # Reinitialise le score
        self.score = 0
    
    
    ### Pouvoirs ###
    def supprimerBloc(self, ligne, colonne):
        # Supprimer = retire un bloc de la grille
        if self.grille[ligne][colonne] == "": # Verifie que la case selectionnee contient bien un bloc
            return False

        self.grille[ligne][colonne] = "" # Supprime le bloc selectionne
        self.appliquerGravite(colonne) # Fait retomber les blocs situes au-dessus pour combler le vide
        return True

    def fusionnerPouvoir(self, ligne, colonne):
        # Fusionner = fusionne le bloc selectionne avec un voisin identique
        if self.grille[ligne][colonne] == "": # Verifie que la case selectionnee n'est pas vide
            return False

        if self.trouverVoisinIdentique(ligne, colonne) is None: # Verifie qu'au moins un voisin identique existe
            return False

        self.score += self.fusionnerBloc(ligne, colonne) # Effectue les fusions et ajoute les points gagnes au score
        return True

    def exploser(self, ligne, colonne):
        # Bombe = detruit le bloc selectionne et les quatres blocs autour
        if self.grille[ligne][colonne] == "": # Verifie que la case selectionnee contient un bloc
            return False

        for (decalageLigne, decalageColonne) in [(0, 0), (1, 0), (-1, 0), (0, -1), (0, 1)]: # Definit les cinq positions a detruire :
            l = ligne + decalageLigne                   # le bloc selectionne, celui du haut, du bas, de gauche et de droite
            c = colonne + decalageColonne

            if 0 <= l < 9 and 0 <= c < 7: # Verifie que chaque position a detruire se trouve dans la grille
                self.grille[l][c] = "" # Supprime le bloc present a la position

        for c in range(7): # Re-applique la gravite pour combler les vides
            self.appliquerGravite(c)

        return True