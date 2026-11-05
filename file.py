import random

# Classe représentant la file des prochains blocs à déposer
class File:
    ### Construction de la file ###
    def __init__(self,liste):
        self.file=[random.choice(liste) for i in range(4)]

    # Créer un nouveau bloc aléatoire et l'ajoute à la file
    def filer(self, liste):
            self.file.append(random.choice(liste))

    # Renvoie le bloc en tête de file et le supprime de la file
    def defiler(self):
        self.file.pop(0)

    # Renvoie la liste des blocs dans la file
    def relancer(self, liste):
        self.file=[random.choice(liste) for i in range(4)]