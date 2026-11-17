###########
# Imports #
from tkinter import *
import bloc
from file import File
from bloc import *
from jeu import Jeu
from bouton import nouvellePartie, relancer, appliquerPouvoir
###########


# Pour la musique de fond (boucle infinie)
import winsound
winsound.PlaySound(
    "musique.wav",
    winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP
)




###################
# Setup des class #
listeProba = [2, 2, 2, 2, 2, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32]   # Creations de
listeprochain = File(listeProba)                                # la file

jeu = Jeu() # Mise en place de la classe Jeu
colonneSelectionnee = 0 # Choix de la colone dans laquelle apparait le 1e bloc dans la zone de lacher
casesHaut = [] # Liste des cases de la zone de lacher
###################


####################
# Variables utiles #
backgroundColor = "#151923"
elementColor = "#252D3D"

# Pouvoirs : nombre d'utilisations au depart et nombre restant
usagesInitiaux = {"supprimer": 3, 
                  "fusionner": 3, 
                  "relancer": 5, 
                  "bombe": 2}

usagesRestants = {"supprimer": 3, 
                  "fusionner": 3, 
                  "relancer": 5, 
                  "bombe": 2}
pouvoirActif = None     # None si aucun pouvoir n'est selectionne sinon, le nom du pouvoir
partieTerminee = False  # False sauf si la partie est terminee
####################

# Textes d'indication dans la l'info bulle du jeu (=regle du jeu/description des pouvoir)
texteRegles = ("Regle du jeu : cliquer sur une des colonne du haut pour lâcher le bloc. S'il tombe a côte de blocs de même valeur, il les absorbe (priorite : bas, gauche, droite) et sa valeur double. (Les pouvoirs sont en utilisation limitee)")
messagesPouvoirs = {
    "supprimer": "Supprimer : cliquer sur le bloc a supprimer.",
    "fusionner": "Fusionner : cliquer sur un bloc qui a un voisin identique pour les fusionner.",
    "bombe": "Bombe : cliquer sur un bloc, il explose avec les 4 blocs qui l'entourent."
}
nomsPouvoirs = {"supprimer": "Supprimer", "fusionner": "Fusionner", "relancer": "Relancer", "bombe": "Bombe"}
####################


####################
### Fonctions du jeu ###
def lireMeilleurScore(): # Meilleur score (sauvegarde dans un fichier texte)
    # Fonction qui lit le meilleur score et le renvoie (si ne trouve rien renvoie 0
    try:
        fichier = open("meilleur_score.txt", "r")
        valeur = int(fichier.read())
        fichier.close()
        return valeur
    except (FileNotFoundError, ValueError):
        return 0

def sauvegarderMeilleurScore(valeur):              
    #Fonction qui sauvegarde le meilleur score du joueur dans un fichier nomme "meilleur_score.txt"
    fichier = open("meilleur_score.txt", "w")
    fichier.write(str(valeur))
    fichier.close()

meilleurScoreVariable = lireMeilleurScore()     #On charge le meilleur score au debut

def actualiser(x, y, elementGraphique, elementTableau):
    # Fonction pour actualiser la grille du jeu
    for widget in elementGraphique.winfo_children():    # On detruit tt
        widget.destroy()

    for i in range(x):
        for j in range(y):
            # On initioalise les cases comme si elles etaient vides
            couleurFond = backgroundColor
            couleurTexte = "white"

            if elementTableau[i][j] != "": # Et si elle n'est pas vide on lui applique sa couleur de fond
                blocJeu = Bloc(elementTableau[i][j])
                couleurFond = blocJeu.couleurBg()   # Grace a la class Bloc
                couleurTexte = blocJeu.couleurFg()

            bloc = Canvas(elementGraphique, width=75, height=75, bg=couleurFond, highlightthickness=1, highlightbackground=elementColor) # On applique le style

            if elementTableau[i][j] != "":
                bloc.create_text(37.5, 37.5, text=str(elementTableau[i][j]), font=("Inter", 25), fill=couleurTexte) # Pareil mais on definit couleur de texte + sa taille

            bloc.bind("<Button-1>", lambda event, l=i, c=j: cliquerGrille(l, c))  # Detecte la colonne dans laquelle on veut deposer le bloc en recuperant ses coordonnees
            bloc.grid(row=i, column=j)  # Positionne la case dans la grille


def actualiserHaut():
    # Actualise la zone de lâcher de blocs en haut du jeu
    valeurBloc = listeprochain.file[0] # Recupere le prochain bloc a jouer
    for j in range(7): # Parcourt les 7 colonnes
        case = casesHaut[j] # Recupere la case correspondante
        case.delete("all") # Efface le contenu precedent
        case.configure(bg=backgroundColor) # Remet la couleur de fond par defaut

        if j == colonneSelectionnee: # Verifie si cette colonne est selectionnee
            bloc = Bloc(valeurBloc) # Cree le bloc a afficher
            case.configure(bg=bloc.couleurBg()) # Applique sa couleur
            case.create_text(37.5, 37.5, text=str(valeurBloc), font=("Inter", 25), fill=bloc.couleurFg()) # Affiche sa valeur


def choisirColonne(colonne):
    # Choisit la colonne dans laquelle le bloc va tomber
    global colonneSelectionnee
    colonneSelectionnee = colonne # On sauvegarde la colonne selectionne
    actualiserHaut()

def actualiserProchains():
    # Actualise l'affichage des trois prochains blocs
    for label, index in [(prochain1Label, 1), (prochain2Label, 2), (prochain3Label, 3)]: # Parcourt les trois prochains blocs
        valeur = listeprochain.file[index] # Recupere la valeur du bloc
        bloc = Bloc(valeur) # Cree le bloc correspondant
        label.configure(text=str(valeur), bg=bloc.couleurBg(), fg=bloc.couleurFg()) # Actualise sa valeur et ses couleurs


def actualiserScore():
    # Actualise le score et aussi le meilleur score si necessaire
    global meilleurScoreVariable
    scoreValeur.configure(text=str(jeu.score)) # Actualise le score

    if jeu.score > meilleurScoreVariable: # Verifie si le meilleur score est depasse
        meilleurScoreVariable = jeu.score # si oui met a jour le meilleur score
        meilleurScoreValeur.configure(text=str(meilleurScoreVariable)) # Actualise l affichage
        sauvegarderMeilleurScore(meilleurScoreVariable) # Sauvegarde le nouveau record


def afficherInfo(texte):
    # Change le texte d'indication affiche au joueur
    texteInfo.configure(text=texte) # Remplace le texte actuel par celui qui est en parametre


def actualiserPouvoirs():
    # Actualise les boutons des pouvoirs (nbr utilisations)
    for cle in boutonsPouvoirs: # Parcourt tous les pouvoirs
        reste = usagesRestants[cle] # Recupere le nombre d'utilisations
        bouton = boutonsPouvoirs[cle] # Recupere le bouton correspondant
        bouton.configure(text=nomsPouvoirs[cle] + " \n " + str(reste) + "x") # Actualise son texte + nbr utilisations

        if reste == 0: # Verifie si le pouvoir est epuise
            bouton.configure(state=DISABLED) # Desactive le bouton
        else:
            bouton.configure(state=NORMAL) # Active le bouton

        if cle == pouvoirActif: # Verifie si le pouvoir est selectionne
            bouton.configure(relief=SUNKEN, bd=4) # Met le bouton en relief
        else:
            bouton.configure(relief=FLAT, bd=0) # Remet le bouton normal


def deposerBloc(colonne):
    # Depose un bloc dans la colonne choisie
    if partieTerminee or pouvoirActif is not None: # Si un pouvoir est selctionner ou on ne peux plus jouer, arrete la fonction
        return

    valeur = listeprochain.file[0] # Recupere la valeur du prochain bloc dans la file
    ligneFinale = jeu.trouverPosition(colonne) # Recherche la position ou le bloc doit tomber

    if ligneFinale is None: # Verifie si la colonne est pleine
        afficherGameOver() # Affiche l'ecran de fin de partie
        return

    # Anime la chute du bloc
    def animation(ligne):
        jeu.grille[ligne][colonne] = valeur # Affiche temporairement le bloc dans la grille
        actualiser(9, 7, grille, jeu.DonnerGrille()) # Actualise la grille
        jeu.grille[ligne][colonne] = "" # Efface sa position temporaire

        if ligne < ligneFinale: # Verifie si le bloc a atteint sa position finale
            fenetre.after(60, lambda: animation(ligne + 1)) # Passe a la ligne suivante apres un court delai
        else:
            # Depose definitivement le bloc
            jeu.deposerBloc(colonne, valeur) # Ajoute le bloc dans la grille du jeu
            listeprochain.defiler() # Retire le bloc joue de la file
            listeprochain.filer(listeProba) # Ajoute un nouveau bloc dans la file
            actualiserScore() # Actualise le score
            actualiser(9, 7, grille, jeu.DonnerGrille()) # Actualise la grille
            actualiserHaut() # Actualise la zone de lâcher
            actualiserProchains() # Actualise les prochains blocs

            if jeu.estTerminee(): # Verifie si la partie est terminee
                afficherGameOver() # Affiche l'ecran de fin de partie

    animation(0) # Lance l'animation depuis le haut de la grille
    return


def choisirPouvoir(nom):
    # Selectionne ou deselectionne un pouvoir
    global pouvoirActif

    if partieTerminee: # Verifie si la partie est terminee, si oui termoine la fonction
        return

    if usagesRestants[nom] == 0: # Verifie si le pouvoir est encore disponible, si oui termoine la fonction
        return

    # Le pouvoir Relancer s'applique immediatement
    if nom == "relancer":
        relancer(listeprochain, listeProba) # Relance les prochains blocs
        usagesRestants[nom] -= 1 # Retire une utilisation
        actualiserHaut() # Actualise la zone de lâcher
        actualiserProchains() # Actualise les prochains blocs
        actualiserPouvoirs() # Actualise les boutons
        return

    # Un second clic sur le même pouvoir annule sa selection
    if pouvoirActif == nom:
        pouvoirActif = None # Desactive le pouvoir
        afficherInfo(texteRegles) # Reaffiche les regles
    else:
        pouvoirActif = nom # Active le pouvoir selectionne
        afficherInfo(messagesPouvoirs[nom]) # Affiche ses instructions

    actualiserPouvoirs() # Actualise l'apparence des boutons


def cliquerGrille(ligne, colonne):
    # Gere le clic sur une case de la grille pour utiliser un pouvoir
    global pouvoirActif

    if pouvoirActif is None: # Verifie si aucun pouvoir n'est selectionne
        return

    # Applique le pouvoir sur la case selectionnee
    reussi = appliquerPouvoir(pouvoirActif, jeu, ligne, colonne) # Recupere le resultat de l'action

    # Verifie si le pouvoir a pu être applique
    if not reussi:
        afficherInfo("Impossible ici ! " + messagesPouvoirs[pouvoirActif]) # Informe le joueur
        return

    # Met a jour les utilisations restantes
    usagesRestants[pouvoirActif] -= 1 # Retire une utilisation
    pouvoirActif = None # Desactive le pouvoir
    afficherInfo(texteRegles) # Reaffiche les regles

    # Actualise les informations du jeu
    actualiserScore() # Actualise le score
    actualiser(9, 7, grille, jeu.DonnerGrille()) # Actualise la grille
    actualiserPouvoirs() # Actualise les boutons


def recommencer():
    # Reinitialise la grille et le score
    global pouvoirActif, partieTerminee
    partieTerminee = False # Reactive la partie

    nouvellePartie(jeu, listeprochain, listeProba) # Reinitialise les donnees du jeu
    pouvoirActif = None # Desactive tout pouvoir selectionne

    for cle in usagesRestants: # Parcourt les differents pouvoirs
        usagesRestants[cle] = usagesInitiaux[cle] # Reinitialise leurs utilisations

    afficherInfo(texteRegles) # Reaffiche les regles
    actualiserScore() # Actualise le score
    actualiser(9, 7, grille, jeu.DonnerGrille()) # Actualise la grille
    actualiserHaut() # Actualise la zone de lâcher
    actualiserProchains() # Actualise les prochains blocs
    actualiserPouvoirs() # Actualise les boutons


def quitter():
    # Ferme la fenêtre
    fenetre.destroy() # Ferme la fenêtre
    winsound.PlaySound(None, winsound.SND_ASYNC) # Arrête la musique


def quitter_menu():
    # Ferme la fenêtre du menu
    menu.destroy() # Detruit la fenêtre du menu


def LancerJeu():
    # Lance la fenêtre du jeu
    menu.destroy() # Ferme le menu
    fenetre.mainloop() # Lance la boucle principale du jeu


def afficherGameOver():
    # Affiche le message de fin de partie
    global partieTerminee
    partieTerminee = True # Empêche de continuer a jouer
    Label(
        grille,
        text="GAME OVER",
        font=("Verdana", 28, "bold"),
        bg="#151923",
        fg="white"
    ).place(relx=0.5, rely=0.5, anchor="center") # Affiche le message au centre de la grille
####################



################################
# Parametrage de la fenêtre menu
menu = Tk()
menu.title("Suika 2048")
menu.geometry("450x425")
menu.configure(bg=backgroundColor)
menu.resizable(0, 0)  # Empeche le redimensionnement de la fenetre

# Bouton quitter le menu
quitterMenu = Button(menu, text="Quitter", bg="#da7037", font=("Verdana", 13, "bold"), fg="#FFFFFF", height=2, bd=0, relief=FLAT, command=quitter_menu)
quitterMenu.place(x=150, y=150, width=150, height=45)
# Bouton jouer
jouer = Button(menu, text="Jouer", bg="#da7037", font=("Verdana", 13, "bold"), fg="#FFFFFF", height=2, bd=0, relief=FLAT, command=LancerJeu)
jouer.place(x=150, y=200, width=150, height=45)
################################



###########################
# Parametrage de la fenêtre de jeu
fenetre = Tk()
fenetre.title("Suika 2048")
fenetre.geometry("950x925")
fenetre.configure(bg=backgroundColor)
fenetre.resizable(0, 0)  # Empeche le redimensionnement de la fenetre


# Elements de la fenetre
FrameGlobal = Frame(fenetre, bg=backgroundColor) # Global frame (contient tout le reste)
FrameGlobal.pack(padx=10, pady=10, fill=BOTH, expand=True)

# Frame de gauche (zone de lacher de bloc + grille du jeu)
partieJeu = Frame(FrameGlobal, width=545, bg=backgroundColor) # Frame de gauche
partieJeu.pack(padx=10, side=LEFT, fill=Y)

# Zone du haut de la frame de gauche (zone de lacher de bloc + grille du jeu)
hautJeu = Frame(partieJeu, bg=backgroundColor, height=550) # Frame du haut de la frame "partieJeu"
hautJeu.pack(side=TOP)

# Zone de lacher de bloc
lacherBloc = Frame(hautJeu, bg=elementColor, height=65) # Zone/grille de lacher de bloc
lacherBloc.pack(pady=10, side=TOP, fill=X)

# Creation de la grille du jeu (9 par 7)
grille = Frame(hautJeu, bg=backgroundColor) # Grille du jeu
grille.pack(pady=10, side=BOTTOM, fill=BOTH, expand=True)

# Compartiment des pouvoirs
pouvoirs = Frame(partieJeu, bg=backgroundColor, height=200)
pouvoirs.pack(pady=10, side=TOP, fill=X)
Supprimer = Button(pouvoirs, text="Supprimer", bg="#E74C3C", font=("Verdana", 10, "bold"), fg="#FFFFFF", height=3, bd=0, relief=FLAT, command=lambda: choisirPouvoir("supprimer")) # Bouton pouvoir 2
Supprimer.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)
Fusionner = Button(pouvoirs, text="Fusionner", bg="#E67E22", font=("Verdana", 10, "bold"), fg="#FFFFFF", height=3, bd=0, relief=FLAT, command=lambda: choisirPouvoir("fusionner")) # Bouton pouvoir 3
Fusionner.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)
Relancer = Button(pouvoirs, text="Relancer", bg="#8E44AD", font=("Verdana", 10, "bold"), fg="#FFFFFF", height=3, bd=0, relief=FLAT, command=lambda: choisirPouvoir("relancer")) # Bouton
Relancer.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)
Bombe = Button(pouvoirs, text="Bombe", bg="#27AE60", font=("Verdana", 10, "bold"), fg="#FFFFFF", height=3, bd=0, relief=FLAT, command=lambda: choisirPouvoir("bombe")) # Bouton pouvoir 5
Bombe.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)

# Pour retrouver un bouton a partir du nom du pouvoir
boutonsPouvoirs = {"supprimer": Supprimer, "fusionner": Fusionner, "relancer": Relancer, "bombe": Bombe}


####### Frame de droite #######
partieAffichage = Frame(FrameGlobal, bg=backgroundColor) # Frame de droite
partieAffichage.pack(padx=10, side=RIGHT, fill=BOTH, expand=True)

# Creation de la zone du titre et des prochains blocs
titreEtProchain = Frame(partieAffichage, bg=backgroundColor, height=500) # Frame du haut de la frame de droite
titreEtProchain.pack(side=TOP, fill=X)

# Creation de la zone du titre (en haut de la frame de droite)
titre = Frame(titreEtProchain, bg=elementColor, height=65) # Frame qui contient le titre
titre.pack(pady=10, side=TOP, fill=X)
titreLabel = Label(titre, text="SuikaGame / 2048", font=("Verdana", 22, "bold"), bg=elementColor, fg="#FFFFFF") # Titre en lui meme
titreLabel.pack(pady=10)

# Zone avec les prochains blocs de la file
prochain = Frame(titreEtProchain, bg=backgroundColor, height=660)
prochain.pack(pady=10, side=BOTTOM, fill=BOTH, expand=True)
prochainTxt = Label(prochain, text="Prochains blocs :", font=("Arial", 14, "bold"), bg=backgroundColor, fg="#FFFFFF") # Texte pour expliquer la zone
prochainTxt.pack(side=TOP, expand=True, anchor="w")

# Premier prochain bloc (couleur et texte changent selon la valeur du bloc)
prochain1 = Frame(prochain, bg=elementColor, height=100, width=100) # Premier prochain bloc
prochain1.pack(pady=15)
prochain1.pack_propagate(False)
prochain1Label = Label(prochain1, text=listeprochain.file[1], font=("Verdana", 18, "bold"), bg=Bloc(listeprochain.file[1]).couleurBg(), fg=Bloc(listeprochain.file[1]).couleurFg()) # Texte de ce prochain bloc
prochain1Label.pack(expand=True, fill=BOTH)

# Deuxieme prochain bloc (couleur et texte changent selon la valeur du bloc)
prochain2 = Frame(prochain, bg=elementColor, height=100, width=100) # Second prochain bloc
prochain2.pack(pady=15)
prochain2.pack_propagate(False)
prochain2Label = Label(prochain2, text=listeprochain.file[2], font=("Verdana", 18, "bold"), bg=Bloc(listeprochain.file[2]).couleurBg(), fg=Bloc(listeprochain.file[2]).couleurFg())
prochain2Label.pack(expand=True, fill=BOTH)

# Troisieme prochain bloc (couleur et texte changent selon la valeur du bloc)
prochain3 = Frame(prochain, bg=elementColor, height=100, width=100) # Troisieme prochain bloc
prochain3.pack(pady=15)
prochain3.pack_propagate(False)
prochain3Label = Label(prochain3, text=listeprochain.file[3], font=("Verdana", 18, "bold"), bg=Bloc(listeprochain.file[3]).couleurBg(), fg=Bloc(listeprochain.file[3]).couleurFg())
prochain3Label.pack(expand=True, fill=BOTH)

# Zone parametres : texte d'indication (regle du jeu ou aide du pouvoir selectionne)
parametre = Frame(partieAffichage, bg=backgroundColor)
parametre.pack(pady=10, fill=BOTH, expand=True)
texteInfo = Label(parametre, text=texteRegles, font=("Verdana", 10), bg=elementColor, fg="#FFFFFF", wraplength=300, justify=LEFT, anchor="nw", padx=10, pady=10)
texteInfo.pack(fill=BOTH, expand=True)

hautPara = Frame(partieAffichage, bg=backgroundColor)
hautPara.pack(fill=X, side=TOP)
restart = Button(hautPara, text=f"Restart", bg="#da7037", font=("Verdana", 13, "bold"), fg="#FFFFFF", height=2, bd=0, relief=FLAT, command=recommencer) # Bouton recommencer
restart.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)
quitter = Button(hautPara, text=f"Quitter", bg="#da7037", font=("Verdana", 13, "bold"), fg="#FFFFFF", height=2, bd=0, relief=FLAT, command=quitter) # Bouton quitter
quitter.pack(padx=5, pady=10, side=RIGHT, fill=X, expand=True)

# Affichage du score actuel et du meilleur score
scoreGlobal = Frame(partieAffichage, bg=backgroundColor, height=150)
scoreGlobal.pack(side=BOTTOM, fill=X)

# score actuel
score = Frame(scoreGlobal, bg="#2B6FF6", height=65) # Score actuel
score.pack(pady=10, side=TOP, fill=X)
scoreLabel = Label(score, text="Score :", font=("Verdana", 18, "bold"), bg="#2B6FF6", fg="#FFFFFF") # Texte gauche
scoreLabel.pack(side=LEFT, pady=10, padx=10)
scoreValeur = Label(score, text=str(jeu.score), font=("Verdana", 18, "bold"), bg="#2B6FF6", fg="#FFFFFF") # Texte droite
scoreValeur.pack(side=RIGHT, pady=10, padx=10)
# Meilleur score
meilleurScore = Frame(scoreGlobal, bg="#2B6FF6", height=65)
meilleurScore.pack(pady=10, side=TOP, fill=X)
meilleurScoreLabel = Label(meilleurScore, text="Best score :", font=("Verdana", 18, "bold"), bg="#2B6FF6", fg="#FFFFFF") # Texte gauche
meilleurScoreLabel.pack(side=LEFT, pady=10, padx=10)
meilleurScoreValeur = Label(meilleurScore, text=str(meilleurScoreVariable), font=("Verdana", 18, "bold"), bg="#2B6FF6", fg="#FFFFFF") # Texte droite
meilleurScoreValeur.pack(side=RIGHT, pady=10, padx=10)

# Creation de la zone de lacher de bloc (haut du jeu)
for j in range(7):
    case = Canvas(lacherBloc,width=75,height=75,bg=backgroundColor,highlightthickness=1, highlightbackground=elementColor)

    case.grid(row=0, column=j)

    case.bind("<Enter>", lambda event, col=j: choisirColonne(col))
    case.bind("<Button-1>", lambda event, col=j: deposerBloc(col))

    casesHaut.append(case)

# Actualise le jeu et la grille, ainsi que le score et les pouvoirs
actualiserHaut()
actualiser(9, 7, grille, jeu.DonnerGrille())
actualiserPouvoirs()

# Lancer la fenetre
menu.mainloop()
