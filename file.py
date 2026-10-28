import random
from tkinter import *
from bloc import Bloc
from main import*

liste = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 8, 8, 8, 16, 16, 32]

class File:
    def __init__(self,liste):
        self.file=[random.choice(liste),random.choice(liste),random.choice(liste)]

    def defiler(self):
        self.file.pop(0)

    def filer(self):
            assert not len(self.file)<=3
            self.file.append(random.choice(liste))

    def afficher(self):
        prochain = Frame(titreEtProchain, bg=backgroundColor, height=660)
        prochain.pack(pady=10, side=BOTTOM, fill=BOTH, expand=True)

        # Premier bloc
        prochain1 = Frame(prochain, bg=elementColor, height=100, width=100)
        prochain1.pack(pady=15)
        prochain1.pack_propagate(False)

        prochain1Label = Label(prochain1, text=str(self.file[0]), font=("Verdana", 18, "bold"), bg=Bloc(self.file), fg="#FFFFFF")
        prochain1Label.pack(expand=True, fill=BOTH)

        # Deuxième bloc
        prochain2 = Frame(prochain, bg=elementColor, height=100, width=100)
        prochain2.pack(pady=15)
        prochain2.pack_propagate(False)

        prochain2Label = Label(prochain2, text=str(self.file[1]), font=("Verdana", 18, "bold"), bg="#FDAB68", fg="#FFFFFF")
        prochain2Label.pack(expand=True, fill=BOTH)

        # Troisième bloc
        prochain3 = Frame(prochain, bg=elementColor, height=100, width=100)
        prochain3.pack(pady=15)
        prochain3.pack_propagate(False)

        prochain3Label = Label(prochain3, text=self.file[2], font=("Verdana", 18, "bold"), bg="#FE3939", fg="#FFFFFF")
        prochain3Label.pack(expand=True, fill=BOTH)
