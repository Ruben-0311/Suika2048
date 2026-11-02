### Classe représentant un bloc du jeu (couleur en fonction de sa valeur)
class Bloc:
    def __init__(self, valeur):
        self.valeur = valeur
        self.saCouleur = self.couleurBg()

# Couleur en fonction de la valeur du bloc
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

# Couleur du texte en fonction de la valeur du bloc
    def couleurFg(self):
        if self.valeur == "":
            return "#FFFFFF"
        elif self.valeur in (2, 4, 128, 256, 512, 1024, 2048):
            return "#51483F"
        elif self.valeur in (8, 16, 32, 64):
            return "#FFFFFF"
        elif self.valeur > 2048:
            return "#51483F"

# Fonction pour fusionner deux blocs et mettre à jour la couleur du bloc résultant
    def fusionner(self, bloc2):
        if self.valeur == bloc2.valeur:
            self.valeur *= 2
            self.saCouleur = self.couleurBg()
            bloc2.suprrimer()
        else:
            return False

### Vraiment nécessaire cette fonction ? (celle du dessous) ###

# Fonction pour supprimer un bloc et mettre à jour la couleur du bloc
    def suprrimer(self):
        self.valeur = ""
        self.saCouleur = self.couleurBg()        