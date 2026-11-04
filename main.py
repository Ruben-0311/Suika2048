###########
# Imports #
import random
from tkinter import *
from file import File
from bloc import *
from jeu import Jeu
from bouton import nouvellePartie, relancer, appliquerPouvoir
###########


###################
# Setup des class #
listeProba = [2, 2, 2, 2, 2, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32] # Creations de
listeprochain = File(listeProba)                                                # la file

jeu = Jeu()                             # Mise en place de la classe Jeu
colonneSelectionnee = 0 # Choix de la colone dans laquelle apparait le 1e bloc dans la zone de lacher
casesHaut = []
###################


####################
# Variables utiles #
backgroundColor = "#151923"
elementColor = "#252D3D"

# Pouvoirs : nombre d'utilisations au départ et nombre restant
usagesInitiaux = {"supprimer": 3, "fusionner": 3, "relancer": 5, "bombe": 2}
usagesRestants = usagesInitiaux.copy()
pouvoirActif = None   # None si aucun pouvoir n'est sélectionné

# Textes d'indication
texteRegles = ("Règle du jeu : clique sur une colonne du haut pour lâcher le bloc. "
               "S'il tombe à côté de blocs de même valeur, il les absorbe (priorité : "
               "bas, gauche, droite) et sa valeur double. Utilise les pouvoirs "
               "avec parcimonie !")
messagesPouvoirs = {
    "supprimer": "Supprimer : clique sur le bloc de la grille que tu veux retirer.",
    "fusionner": "Fusionner : clique sur un bloc qui a un voisin identique (bas, gauche ou droite).",
    "bombe": "Bombe : clique sur un bloc, il explose avec les 4 blocs qui l'entourent."
}
nomsPouvoirs = {"supprimer": "Supprimer", "fusionner": "Fusionner", "relancer": "Relancer", "bombe": "Bombe"}
####################


#######################
# Meilleur score (sauvegardé dans un fichier texte)
def lireMeilleurScore():
    try:
        fichier = open("meilleur_score.txt", "r")
        valeur = int(fichier.read())
        fichier.close()
        return valeur
    except (FileNotFoundError, ValueError):
        return 0

def sauvegarderMeilleurScore(valeur):
    fichier = open("meilleur_score.txt", "w")
    fichier.write(str(valeur))
    fichier.close()

meilleurScoreVariable = lireMeilleurScore()
#######################


####################
# Fonctions du jeu #
def actualiser(x, y, elementGraphique, elementTableau):
    # On détruit les anciennes cases pour ne pas les empiler à chaque actualisation
    for widget in elementGraphique.winfo_children():
        widget.destroy()

    for i in range(x):
        for j in range(y):
            # Couleurs par défaut comme case vide a chaques debut de boucle
            couleurFond = backgroundColor
            couleurTexte = "white"

            if elementTableau[i][j] != "": # Si case pas vide on change ses couleurs
                blocJeu = Bloc(elementTableau[i][j])
                couleurFond = blocJeu.couleurBg()
                couleurTexte = blocJeu.couleurFg()

            bloc = Canvas(elementGraphique, width=75, height=75, bg=couleurFond, highlightthickness=1, highlightbackground=elementColor) # On applique le style

            if elementTableau[i][j] != "":
                bloc.create_text(37.5, 37.5, text=str(elementTableau[i][j]), font=("Inter", 25), fill=couleurTexte) #Pareil pour la couleur du texte

            # Clic sur la case : sert à utiliser un pouvoir
            bloc.bind("<Button-1>", lambda event, l=i, c=j: cliquerGrille(l, c))
            bloc.grid(row=i, column=j)

def actualiserHaut():
    valeurBloc = listeprochain.file[0]
    for j in range(7):
        case = casesHaut[j]
        case.delete("all")
        case.configure(bg=backgroundColor)

        if j == colonneSelectionnee:
            bloc = Bloc(valeurBloc)
            case.configure(bg=bloc.couleurBg())
            case.create_text(37.5, 37.5, text=str(valeurBloc), font=("Inter", 25), fill=bloc.couleurFg())

def choisirColonne(colonne):
    global colonneSelectionnee
    colonneSelectionnee = colonne
    actualiserHaut()

def actualiserProchains():
    for label, index in [(prochain1Label, 1), (prochain2Label, 2), (prochain3Label, 3)]:
        valeur = listeprochain.file[index]
        bloc = Bloc(valeur)

        label.configure(text=str(valeur), bg=bloc.couleurBg(), fg=bloc.couleurFg())

# Affiche le score et met à jour le meilleur score si besoin
def actualiserScore():
    global meilleurScoreVariable
    scoreValeur.configure(text=str(jeu.score))

    if jeu.score > meilleurScoreVariable:
        meilleurScoreVariable = jeu.score
        meilleurScoreValeur.configure(text=str(meilleurScoreVariable))
        sauvegarderMeilleurScore(meilleurScoreVariable)

# Change le texte d'indication
def afficherInfo(texte):
    texteInfo.configure(text=texte)

# Met à jour les boutons de pouvoirs (compteur, désactivation à 0, pouvoir sélectionné)
def actualiserPouvoirs():
    for cle in boutonsPouvoirs:
        reste = usagesRestants[cle]
        bouton = boutonsPouvoirs[cle]
        bouton.configure(text=nomsPouvoirs[cle] + " \n " + str(reste) + "x")

        if reste == 0:
            bouton.configure(state=DISABLED)
        else:
            bouton.configure(state=NORMAL)

        if cle == pouvoirActif:
            bouton.configure(relief=SUNKEN, bd=4)
        else:
            bouton.configure(relief=FLAT, bd=0)

def deposerBloc(colonne):
    # On ne lâche pas de bloc pendant qu'un pouvoir est sélectionné
    if pouvoirActif is not None:
        afficherInfo("Un pouvoir est sélectionné. " + messagesPouvoirs[pouvoirActif] + " (re-clique sur le bouton pour annuler)")
        return

    valeur = listeprochain.file[0]

    succes = jeu.deposerBloc(colonne, valeur)

    if not succes:
        return

    listeprochain.defiler()
    listeprochain.filer(listeProba)

    actualiserScore()
    actualiser(9, 7, grille, jeu.DonnerGrille())
    actualiserHaut()
    actualiserProchains()

# Clic sur un bouton de pouvoir
def choisirPouvoir(nom):
    global pouvoirActif

    if usagesRestants[nom] == 0:
        return

    # Relancer s'applique tout de suite, pas besoin de cliquer sur la grille
    if nom == "relancer":
        relancer(listeprochain, listeProba)
        usagesRestants[nom] -= 1
        afficherInfo("Les prochains blocs ont été relancés !")
        actualiserHaut()
        actualiserProchains()
        actualiserPouvoirs()
        return

    # Re-clic sur le même pouvoir : on annule la sélection
    if pouvoirActif == nom:
        pouvoirActif = None
        afficherInfo(texteRegles)
    else:
        pouvoirActif = nom
        afficherInfo(messagesPouvoirs[nom])
    actualiserPouvoirs()

# Clic sur une case de la grille (utile seulement si un pouvoir est sélectionné)
def cliquerGrille(ligne, colonne):
    global pouvoirActif

    if pouvoirActif is None:
        return

    reussi = appliquerPouvoir(pouvoirActif, jeu, ligne, colonne)

    if not reussi:
        afficherInfo("Impossible ici ! " + messagesPouvoirs[pouvoirActif])
        return

    usagesRestants[pouvoirActif] -= 1
    pouvoirActif = None
    afficherInfo(texteRegles)

    actualiserScore()
    actualiser(9, 7, grille, jeu.DonnerGrille())
    actualiserPouvoirs()

# Bouton Restart
def recommencer():
    global pouvoirActif

    nouvellePartie(jeu, listeprochain, listeProba)
    pouvoirActif = None
    for cle in usagesRestants:
        usagesRestants[cle] = usagesInitiaux[cle]

    afficherInfo(texteRegles)
    actualiserScore()
    actualiser(9, 7, grille, jeu.DonnerGrille())
    actualiserHaut()
    actualiserProchains()
    actualiserPouvoirs()

def quitter():
    fenetre.destroy()

####################



# Parametrage de la fenêtre
fenetre = Tk()
fenetre.title("Suika 2048")
fenetre.geometry("950x925")
fenetre.configure(bg=backgroundColor)
fenetre.resizable(0, 0)  # Empeche le redimensionnement de la fenetre

##############
# Elements de la fenetre
FrameGlobal = Frame(fenetre, bg=backgroundColor) # Global frame (contient tout le reste)
FrameGlobal.pack(padx=10, pady=10, fill=BOTH, expand=True)

partieJeu = Frame(FrameGlobal, width=545, bg=backgroundColor) # Frame de gauche
partieJeu.pack(padx=10, side=LEFT, fill=Y)

hautJeu = Frame(partieJeu, bg=backgroundColor, height=550) # Frame du haut de la frame "partieJeu"
hautJeu.pack(side=TOP)

lacherBloc = Frame(hautJeu, bg=elementColor, height=65) # Zone/grille de lacher de bloc
lacherBloc.pack(pady=10, side=TOP, fill=X)

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

# Pour retrouver un bouton à partir du nom du pouvoir
boutonsPouvoirs = {"supprimer": Supprimer, "fusionner": Fusionner, "relancer": Relancer, "bombe": Bombe}


####### Frame de droite #######
partieAffichage = Frame(FrameGlobal, bg=backgroundColor) # Frame de droite
partieAffichage.pack(padx=10, side=RIGHT, fill=BOTH, expand=True)

titreEtProchain = Frame(partieAffichage, bg=backgroundColor, height=500) # Frame du haut de la frame de droite
titreEtProchain.pack(side=TOP, fill=X)

titre = Frame(titreEtProchain, bg=elementColor, height=65) # Frame qui contient le titre
titre.pack(pady=10, side=TOP, fill=X)
titreLabel = Label(titre, text="SuikaGame / 2048", font=("Verdana", 22, "bold"), bg=elementColor, fg="#FFFFFF") # Titre en lui meme
titreLabel.pack(pady=10)

# Zone avec les prochains blocs de la file
prochain = Frame(titreEtProchain, bg=backgroundColor, height=660)
prochain.pack(pady=10, side=BOTTOM, fill=BOTH, expand=True)
prochainTxt = Label(prochain, text="Prochains blocs :", font=("Arial", 14, "bold"), bg=backgroundColor, fg="#FFFFFF") # Texte pour expliquer la zone
prochainTxt.pack(side=TOP, expand=True, anchor="w")

prochain1 = Frame(prochain, bg=elementColor, height=100, width=100) # Premier prochain bloc
prochain1.pack(pady=15)
prochain1.pack_propagate(False)
prochain1Label = Label(prochain1, text=listeprochain.file[1], font=("Verdana", 18, "bold"), bg=Bloc(listeprochain.file[1]).couleurBg(), fg=Bloc(listeprochain.file[1]).couleurFg()) # Texte de ce prochain bloc
prochain1Label.pack(expand=True, fill=BOTH)

prochain2 = Frame(prochain, bg=elementColor, height=100, width=100) # Second prochain bloc
prochain2.pack(pady=15)
prochain2.pack_propagate(False)
prochain2Label = Label(prochain2, text=listeprochain.file[2], font=("Verdana", 18, "bold"), bg=Bloc(listeprochain.file[2]).couleurBg(), fg=Bloc(listeprochain.file[2]).couleurFg())
prochain2Label.pack(expand=True, fill=BOTH)

prochain3 = Frame(prochain, bg=elementColor, height=100, width=100) # Troisieme prochain bloc
prochain3.pack(pady=15)
prochain3.pack_propagate(False)
prochain3Label = Label(prochain3, text=listeprochain.file[3], font=("Verdana", 18, "bold"), bg=Bloc(listeprochain.file[3]).couleurBg(), fg=Bloc(listeprochain.file[3]).couleurFg())
prochain3Label.pack(expand=True, fill=BOTH)

# Zone parametres : texte d'indication (règle du jeu ou aide du pouvoir sélectionné)
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


for j in range(7):
    case = Canvas(
        lacherBloc,
        width=75,
        height=75,
        bg=backgroundColor,
        highlightthickness=1,
        highlightbackground=elementColor
    )

    case.grid(row=0, column=j)

    case.bind("<Enter>", lambda event, col=j: choisirColonne(col))
    case.bind("<Button-1>", lambda event, col=j: deposerBloc(col))

    casesHaut.append(case)


actualiserHaut()
actualiser(9, 7, grille, jeu.DonnerGrille())
actualiserPouvoirs()
# Lancer la fenetre
fenetre.mainloop()