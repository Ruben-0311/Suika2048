# Différents boutons pour l'interface graphique
from tkinter import *
from random import choice
from bloc import Bloc


# Fonction pour créer une nouvelle partie
def nouvellePartie(jeu, listeprochain, casesHaut, grille,
                   prochain1Label, prochain2Label, prochain3Label,
                   actualiser, actualiserHaut, actualiserProchains,
                   scoreValeur, meilleurScoreValeur):

    # Vidage la grille du jeu
    for i in range(9):
        for j in range(7):
            jeu.grille[i][j] = ""

    # Réinitialisation la grille du haut
    for j in range(7):
        jeu.grilleHaut[j] = ""
    jeu.grilleHaut[3] = choice([2, 2, 2, 2, 2, 2, 2, 2, 2,4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32])
    # Réinitialisation la file
    listeprochain.file = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32]
    # Actualisation les affichages
    actualiser(9, 7, grille, jeu.DonnerGrille())
    actualiserHaut()
    actualiserProchains()
    scoreValeur.configure(text="0")

# Fonction pour poser une bombe
def bombe(jeu, historique, actualiser, actualiserHaut,
          actualiserProchains, grille, bombesRestantes,
          compteurBombes):
    blocsPresents = []

    # La bombe ne peut être posée que sur un bloc présent dans la grille
    for i in range(9):
        for j in range(7):
            if jeu.grille[i][j] != "":
                blocsPresents.append((i, j))
    # Impossible de poser une bombe si la grille est vide
    if len(blocsPresents) == 0:
        return
    # Vérification du nombre de bombes restantes
    if bombesRestantes[0] <= 0:
        return
    # Choix aléatoire d'un bloc
    ligne, colonne = choice(blocsPresents)
    # On récupère la valeur du bloc choisi
    valeur = jeu.grille[ligne][colonne]
    # Le bloc régresse d'un niveau
    if valeur > 2:
        jeu.grille[ligne][colonne] = valeur // 2
    else:
        jeu.grille[ligne][colonne] = ""
    # On retire une bombe du stock
    bombesRestantes[0] -= 1
    compteurBombes.configure(text="Bombes restantes : " + str(bombesRestantes[0]))
    # Actualisation
    actualiser(9, 7, grille, jeu.DonnerGrille())
    actualiserHaut()
    actualiserProchains()


# Fonction pour relancer les prochains blocs
def relancer(listeprochain, historique, actualiserProchains, relancementsRestants, compteurRelancements):
    # Vérification du nombre de relancements restants
    if relancementsRestants[0] <= 0:
        return
    # Sauvegarde de la file
    historique.append(([ligne[:] for ligne in jeu.grille],listeprochain.file[:]))
    # On mélange les prochains blocs
    listeprochain.file[0] = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32])
    listeprochain.file[1] = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32])
    listeprochain.file[2] = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32])
    # On retire un relancement
    relancementsRestants[0] -= 1
    compteurRelancements.configure(text="Relancements restants : " + str(relancementsRestants[0]))
    actualiserProchains()


### Attention : les fonctions ci-dessous sont des fonctions à complettement réécrire
### Elles sont là pour l'instant pour éviter de réouvrir un autre fichier et de perdre du temps

import pygame

# Initialisation de Pygame
pygame.init()

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouton Pygame")

# Création de la classe Bouton
class Button:
    def __init__(self, x, y, width, height, color, text, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

# Fonction à exécuter lorsque le bouton est cliqué
def on_button_click():
    print("Bouton cliqué!")

# Création du bouton
button = Button(200, 250, 200, 100, GREEN, "Cliquez-moi", WHITE, on_button_click)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        button.handle_event(event)

    # Changement de couleur du bouton lorsque survolé
    if button.rect.collidepoint(pygame.mouse.get_pos()):
        button.color = RED
    else:
        button.color = GREEN

    screen.fill(WHITE)
    button.draw(screen)
    pygame.display.flip()

pygame.quit()