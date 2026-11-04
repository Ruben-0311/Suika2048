###########
# Imports #
import random
from tkinter import *
from file import File
from bloc import *
from jeu import Jeu
###########


###################
# Setup des class #
listeProba = [2, 2, 2, 2, 2, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32] # Creations de
listeprochain = File(listeProba)                                                # la file

jeu = Jeu()                             # Mise en place de la classe Jeu
colonneSelectionnee = 0 # Choix de la colone dans laquelle apparait le 1e bloc dans la zone de lacher
valeurBloc = jeu.DonnerGrilleHaut()[0] # Recupere la valeur du prochain bloc qui va tomber
casesHaut = []
###################


####################
# Variables utiles #
backgroundColor = "#151923"
elementColor = "#252D3D"

scoreVariable = 0
meilleurScoreVariable = 12354
####################

####################
# Fonctions du jeu #
def actualiser(x, y, elementGraphique, elementTableau):
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


def deposerBloc(colonne):
    valeur = listeprochain.file[0]

    succes = jeu.deposerBloc(colonne, valeur)

    if not succes:
        return

    listeprochain.defiler()
    listeprochain.filer(listeProba)

    actualiser(9, 7, grille, jeu.DonnerGrille())
    actualiserHaut()
    actualiserProchains()


def actualiserProchains():
    for label, index in [(prochain1Label, 1), (prochain2Label, 2), (prochain3Label, 3)]:
        valeur = listeprochain.file[index]
        bloc = Bloc(valeur)

        label.configure(text=str(valeur), bg=bloc.couleurBg(), fg=bloc.couleurFg())

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
Supprimer = Button(pouvoirs, text=f"Supprimer \n {3}x", bg="#E74C3C", font=("Verdana", 10, "bold"), fg="#FFFFFF", height=3, bd=0, relief=FLAT) # Bouton pouvoir 2
Supprimer.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)
Fusionner = Button(pouvoirs, text=f"Fusionner \n {3}x", bg="#E67E22", font=("Verdana", 10, "bold"), fg="#FFFFFF", height=3, bd=0, relief=FLAT) # Bouton pouvoir 3
Fusionner.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)
Relancer = Button(pouvoirs, text=f"Relancer \n {5}x", bg="#8E44AD", font=("Verdana", 10, "bold"), fg="#FFFFFF", height=3, bd=0, relief=FLAT) # Bouton
Relancer.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)
Bombe = Button(pouvoirs, text=f"Bombe \n {2}x", bg="#27AE60", font=("Verdana", 10, "bold"), fg="#FFFFFF", height=3, bd=0, relief=FLAT) # Bouton pouvoir 5
Bombe.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)


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

# Zone parametres
parametre = Frame(partieAffichage, bg=backgroundColor)
parametre.pack(pady=10, fill=BOTH, expand=True)

hautPara = Frame(partieAffichage, bg=backgroundColor)
hautPara.pack(fill=X, side=TOP)
restart = Button(hautPara, text=f"Restart", bg="#da7037", font=("Verdana", 13, "bold"), fg="#FFFFFF", height=2, bd=0, relief=FLAT) # Bouton recommencer
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
scoreValeur = Label(score, text=scoreVariable, font=("Verdana", 18, "bold"), bg="#2B6FF6", fg="#FFFFFF") # Texte droite
scoreValeur.pack(side=RIGHT, pady=10, padx=10)
# Meilleur score
meilleurScore = Frame(scoreGlobal, bg="#2B6FF6", height=65)
meilleurScore.pack(pady=10, side=TOP, fill=X)
meilleurScoreLabel = Label(meilleurScore, text="Best score :", font=("Verdana", 18, "bold"), bg="#2B6FF6", fg="#FFFFFF") # Texte gauche
meilleurScoreLabel.pack(side=LEFT, pady=10, padx=10)
meilleurScoreValeur = Label(meilleurScore, text="16542", font=("Verdana", 18, "bold"), bg="#2B6FF6", fg="#FFFFFF") # Texte droite
meilleurScoreValeur.pack(side=RIGHT, pady=10, padx=10)

if scoreVariable>meilleurScoreVariable:
    meilleurScoreVariable=scoreVariable

else:
    pass




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
# Lancer la fenetre
fenetre.mainloop()