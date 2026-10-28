class Bloc:
    def __init__(self, valeur):
        self.valeur = valeur
        self.saCouleur = self.couleur()

    def couleur(self):
        if self.valeur == "":
            return "#151923"
        elif self.valeur == 2:
            return "#EEE4DA"
        elif self.valeur == 4:
            return "#EDE0C8"
        elif self.valeur == 8:
            return "#F2B179"
        elif self.valeur == 16:
            return "#F59563"
        elif self.valeur == 32:
            return "#F67C5F"
        elif self.valeur == 64:
            return "#F65E3B"
        elif self.valeur == 128:
            return "#EDCF72"
        elif self.valeur == 256:
            return "#EDCC61"
        elif self.valeur == 512:
            return "#EDC850"
        elif self.valeur == 1024:
            return "#EDC53F"
        elif self.valeur >= 2048:
            return "#EDC22E"

    def fusionner(self, bloc2):
        if self.valeur == bloc2.valeur:
            self.valeur *= 2
            self.saCouleur = self.couleur()
            bloc2.suprrimer()
        else:
            return False

    def suprrimer(self):
        self.valeur = ""
        self.saCouleur = self.couleur()
        