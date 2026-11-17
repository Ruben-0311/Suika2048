import random#

class File:
    # Classe représentant la file des prochains blocs à déposer

    def __init__(self,liste): ### Construction de l'objet file
        self.file=[random.choice(liste) for i in range(4)]

    def filer(self, liste): # Rajoute un bloc a la file (a la fin)
            self.file.append(random.choice(liste))

    def defiler(self): # Supprime le 1er element de la file
        self.file.pop(0)

    def relancer(self, liste): # Reinitialise tt le contenu de la file
        self.file=[random.choice(liste) for i in range(4)]