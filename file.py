import random
from tkinter import *
from bloc import Bloc


class File:
    def __init__(self,liste):
        self.file=[random.choice(liste) for i in range(3)]

    def defiler(self):
        self.file.pop(0)

    def filer(self, liste):
            assert not len(self.file)<=3
            self.file.append(random.choice(liste))
