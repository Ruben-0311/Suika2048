import random

class File:
    def __init__(self,liste):
        self.file=[random.choice(liste) for i in range(4)]

    def filer(self, liste):
            self.file.append(random.choice(liste))

    def defiler(self):
        self.file.pop(0)