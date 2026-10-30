class Bloc:
    def __init__(self, valeur):
        self.valeur = valeur
        self.saCouleur = self.couleurBg()

    def couleurBg(self):
        if self.valeur == "":
            return "#151923"
        elif self.valeur == 2:
            return "#e5dbd1"
        elif self.valeur == 4:
            return "#e3d7c0"
        elif self.valeur == 8:
            return "#e9a974"
        elif self.valeur == 16:
            return "#ec8e5f"
        elif self.valeur == 32:
            return "#eb775b"
        elif self.valeur == 64:
            return "#f56046"
        elif self.valeur == 128:
            return "#ebcc72"
        elif self.valeur == 256:
            return "#eac95f"
        elif self.valeur == 512:
            return "#e9c44d"
        elif self.valeur == 1024:
            return "#eac140"
        elif self.valeur >= 2048:
            return "#eac02e"

    def couleurFg(self):
        if self.valeur == "":
            return "#FFFFFF"
        elif self.valeur in (2, 4, 128, 256, 512, 1024, 2048):
            return "#51483F"
        elif self.valeur in (8, 16, 32, 64):
            return "#FFFFFF"
        elif self.valeur > 2048:
            return "#51483F"

    def fusionner(self, bloc2):
        if self.valeur == bloc2.valeur:
            self.valeur *= 2
            self.saCouleur = self.couleurBg()
            bloc2.suprrimer()
        else:
            return False

    def suprrimer(self):
        self.valeur = ""
        self.saCouleur = self.couleurBg()        