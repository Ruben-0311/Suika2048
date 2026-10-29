import random
from tkinter import *
from file import File
from bloc import *

# Variables utiles
backgroundColor = "#151923"
elementColor = "#252D3D"
#la liste des cubes est cubes=[2,4,8,16,32,64,128,256,512,1024,2048,4096]

grille = [[],[],[],[],[],[],[],
          [],[],[],[],[],[],[],
          [],[],[],[],[],[],[],
          [],[],[],[],[],[],[],
          [],[],[],[],[],[],[],
          [],[],[],[],[],[],[],
          [],[],[],[],[],[],[],
          [],[],[],[],[],[],[],
          [],[],[],[],[],[],[],
          [],[],[],[],[],[],[],
          ]

listeProba = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32]


# Setup des class 
listeprochain = File(listeProba)


# Parametrage de la fenêtre
fenetre = Tk()
fenetre.title("Suika 2048")
fenetre.geometry("950x900")
fenetre.configure(bg=backgroundColor)
fenetre.resizable(0, 0)  # Empeche le redimensionnement de la fenetre


##############
# Global frame (contient tout le reste)
##############
FrameGlobal = Frame(fenetre, bg=backgroundColor)
FrameGlobal.pack(padx=10, pady=10, fill=BOTH, expand=True)


##################
## Frame de gauche
##################
partieJeu = Frame(FrameGlobal, width=545, bg=backgroundColor)
partieJeu.pack(padx=10, side=LEFT, fill=Y)

# Frame du haut de la frame de gauche
jeu = Frame(partieJeu, bg=backgroundColor, height=550)
jeu.pack(side=TOP)

# Zone de lacher de bloc
lacherBloc = Frame(jeu, bg=elementColor, height=65)
lacherBloc.pack(pady=10, side=TOP, fill=X)

# Grille du jeu
grille = Frame(jeu, bg=backgroundColor)
grille.pack(pady=10, side=BOTTOM, fill=BOTH, expand=True)


# Compartiment des pouvoirs
pouvoirs = Frame(partieJeu, bg=backgroundColor, height=150)
pouvoirs.pack(pady=10, side=TOP, fill=X)

# Bouton 1
pouvoir1 = Button(pouvoirs, text="Annuler", bg="#2B6FF6", font=("Verdana", 10, "bold"), fg="#FFFFFF", height=3, bd=0, relief=FLAT)
pouvoir1.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)

# Bouton 2
pouvoir2 = Button(pouvoirs, text="Supprimer", bg="#E74C3C", font=("Verdana", 10, "bold"), fg="#FFFFFF", height=3, bd=0, relief=FLAT)
pouvoir2.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)

# Bouton 3
pouvoir3 = Button(pouvoirs, text="Fusionner", bg="#E67E22", font=("Verdana", 10, "bold"), fg="#FFFFFF", height=3, bd=0, relief=FLAT)
pouvoir3.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)

# Bouton 4
pouvoir4 = Button(pouvoirs, text="Relancer", bg="#8E44AD", font=("Verdana", 10, "bold"), fg="#FFFFFF", height=3, bd=0, relief=FLAT)
pouvoir4.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)

# Bouton 5
pouvoir5 = Button(pouvoirs, text="Bombe", bg="#27AE60", font=("Verdana", 10, "bold"), fg="#FFFFFF", height=3, bd=0, relief=FLAT)
pouvoir5.pack(padx=5, pady=10, side=LEFT, fill=X, expand=True)


##################
## Frame de droite
##################
partieAffichage = Frame(FrameGlobal, bg=backgroundColor)
partieAffichage.pack(padx=10, side=RIGHT, fill=BOTH, expand=True)

# Frame du haut de la frame de droite
titreEtProchain = Frame(partieAffichage, bg=backgroundColor, height=500)
titreEtProchain.pack(side=TOP, fill=X)


# Frame qui contient le titre
titre = Frame(titreEtProchain, bg=elementColor, height=65)
titre.pack(pady=10, side=TOP, fill=X)

titreLabel = Label(titre, text="SuikaGame / 2048", font=("Verdana", 22, "bold"), bg=elementColor, fg="#FFFFFF")
titreLabel.pack(pady=10)


############################################
# Zone avec les prochains blocs de la file #
############################################


prochain = Frame(titreEtProchain, bg=backgroundColor, height=660)
prochain.pack(pady=10, side=BOTTOM, fill=BOTH, expand=True)

prochainTxt = Label(prochain, text="Prochain blocs :", font=("Arial", 14, "bold"), bg=backgroundColor, fg="#FFFFFF")
prochainTxt.pack(side=TOP, expand=True, anchor="w")

# Premier bloc
prochain1 = Frame(prochain, bg=elementColor, height=100, width=100)
prochain1.pack(pady=15)
prochain1.pack_propagate(False)

prochain1Label = Label(prochain1, text=listeprochain.file[0], font=("Verdana", 18, "bold"), bg=Bloc(listeprochain.file[0]).couleurBg(), fg=Bloc(listeprochain.file[0]).couleurFg())
prochain1Label.pack(expand=True, fill=BOTH)

# Deuxième bloc
prochain2 = Frame(prochain, bg=elementColor, height=100, width=100)
prochain2.pack(pady=15)
prochain2.pack_propagate(False)

prochain2Label = Label(prochain2, text=listeprochain.file[1], font=("Verdana", 18, "bold"), bg=Bloc(listeprochain.file[1]).couleurBg(), fg=Bloc(listeprochain.file[1]).couleurFg())
prochain2Label.pack(expand=True, fill=BOTH)

# Troisième bloc
prochain3 = Frame(prochain, bg=elementColor, height=100, width=100)
prochain3.pack(pady=15)
prochain3.pack_propagate(False)

prochain3Label = Label(prochain3, text=listeprochain.file[2], font=("Verdana", 18, "bold"), bg=Bloc(listeprochain.file[2]).couleurBg(), fg=Bloc(listeprochain.file[2]).couleurFg())
prochain3Label.pack(expand=True, fill=BOTH)


# Affichage du score actuel et du meilleur score
scoreGlobal = Frame(partieAffichage, bg=backgroundColor, height=150)
scoreGlobal.pack(side=BOTTOM, fill=X)

# Score actuel
score = Frame(scoreGlobal, bg="#2B6FF6", height=65)
score.pack(pady=10, side=TOP, fill=X)

scoreLabel = Label(score, text="Score :", font=("Verdana", 18, "bold"), bg="#2B6FF6", fg="#FFFFFF")
scoreLabel.pack(side=LEFT, pady=10, padx=10)

scroreValeur = Label(score, text="8496", font=("Verdana", 18, "bold"), bg="#2B6FF6", fg="#FFFFFF")
scroreValeur.pack(side=RIGHT, pady=10, padx=10)


# Meilleur score
meilleurScore = Frame(scoreGlobal, bg="#2B6FF6", height=65)
meilleurScore.pack(pady=10, side=TOP, fill=X)

meilleurScoreLabel = Label(meilleurScore, text="Best score :", font=("Verdana", 18, "bold"), bg="#2B6FF6", fg="#FFFFFF")
meilleurScoreLabel.pack(side=LEFT, pady=10, padx=10)

meilleurScoreValeur = Label(meilleurScore, text="16542", font=("Verdana", 18, "bold"), bg="#2B6FF6", fg="#FFFFFF")
meilleurScoreValeur.pack(side=RIGHT, pady=10, padx=10)


# Fonction pour creer une grille
def faireUneGrille(x, y, element):
    for i in range(x):
        for j in range(y):
            bloc = Canvas(
                element,
                width=75,
                height=75,
                bg=backgroundColor,
                highlightthickness=1,
                highlightbackground=elementColor
            )
            bloc.grid(row=i, column=j)


faireUneGrille(1, 7, lacherBloc)
faireUneGrille(9, 7, grille)



# Lancer la fenetre
fenetre.mainloop()
