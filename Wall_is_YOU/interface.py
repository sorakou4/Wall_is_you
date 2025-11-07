"""
Interface graphique pour Wall Is You (utilise `fltk.py` existant).

Ce fichier affiche une grille carrée centrée, dessine des murs et des
ouvertures pour chaque salle (visible lors des rotations), et place
l'aventurier et les dragons au centre des cases.

Contrôles : clic gauche = pivoter la salle ; maintenir 'i' + clic =
ajouter à l'intention ; Espace = appliquer l'intention ; R =
recommencer ; Échap = quitter.
"""

from typing import List, Tuple
import Donjon_version_corrigee as base
import moteur
import fltk

Cell = Tuple[int, int]


class Interface:
    def __init__(self, nb_lignes=6, nb_colonnes=8, nb_dragons=5):
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.nb_dragons = nb_dragons

        self.window_w = 800
        self.window_h = 600
        fltk.cree_fenetre(self.window_w, self.window_h)

        self.margin = 40
        self.nouvelle_partie()

    def nouvelle_partie(self):
        self.donjon, self.aventurier, self.dragons = base.creer_donjon(
            self.nb_lignes, self.nb_colonnes, self.nb_dragons
        )
        self.intention: List[Cell] = []
        self.update_cell_size()
        self.redessiner()

    def update_cell_size(self):
        grid_w = self.window_w - 2 * self.margin
        grid_h = self.window_h - 2 * self.margin
        cw = grid_w // self.nb_colonnes
        ch = grid_h // self.nb_lignes
        self.cell_size = max(8, min(cw, ch))
        total_w = self.cell_size * self.nb_colonnes
        total_h = self.cell_size * self.nb_lignes
        self.grid_x0 = self.margin + (grid_w - total_w) // 2
        self.grid_y0 = self.margin + (grid_h - total_h) // 2

    def cell_from_xy(self, x: int, y: int) -> Cell:
        j = (x - self.grid_x0) // self.cell_size
        i = (y - self.grid_y0) // self.cell_size
        i = int(max(0, min(self.nb_lignes - 1, i)))
        j = int(max(0, min(self.nb_colonnes - 1, j)))
        return (i, j)

    def center_of_cell(self, cell: Cell) -> Tuple[int, int]:
        i, j = cell
        cx = self.grid_x0 + j * self.cell_size + self.cell_size // 2
        cy = self.grid_y0 + i * self.cell_size + self.cell_size // 2
        return cx, cy

    def redessiner(self):
        fltk.efface_tout()
        
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                x0 = self.grid_x0 + j * self.cell_size
                y0 = self.grid_y0 + i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                cx = (x0 + x1) // 2
                cy = (y0 + y1) // 2

                haut, droite, bas, gauche = self.donjon[i][j]
                gap = self.cell_size // 3

                # haut
                if not haut:
                    fltk.ligne(x0, y0, x1, y0, couleur="black", epaisseur=2)
                else:
                    fltk.ligne(x0, y0, cx - gap//2, y0, couleur="black", epaisseur=2)
                    fltk.ligne(cx + gap//2, y0, x1, y0, couleur="black", epaisseur=2)

                # bas
                if not bas:
                    fltk.ligne(x0, y1, x1, y1, couleur="black", epaisseur=2)
                else:
                    fltk.ligne(x0, y1, cx - gap//2, y1, couleur="black", epaisseur=2)
                    fltk.ligne(cx + gap//2, y1, x1, y1, couleur="black", epaisseur=2)

                # gauche
                if not gauche:
                    fltk.ligne(x0, y0, x0, y1, couleur="black", epaisseur=2)
                else:
                    fltk.ligne(x0, y0, x0, cy - gap//2, couleur="black", epaisseur=2)
                    fltk.ligne(x0, cy + gap//2, x0, y1, couleur="black", epaisseur=2)

                # droite
                if not droite:
                    fltk.ligne(x1, y0, x1, y1, couleur="black", epaisseur=2)
                else:
                    fltk.ligne(x1, y0, x1, cy - gap//2, couleur="black", epaisseur=2)
                    fltk.ligne(x1, cy + gap//2, x1, y1, couleur="black", epaisseur=2)

        # dragons
        for d in self.dragons:
            pos, niveau = d
            cx, cy = self.center_of_cell(pos)
            r = int(self.cell_size * 0.15)
            fltk.cercle(cx, cy, r, couleur="red", remplissage="red")
            fltk.texte(cx, cy, str(niveau), couleur="white", ancrage="center", taille=max(8, r // 2))

        # aventurier
        ax, ay = self.center_of_cell(self.aventurier[0])
        r = int(self.cell_size * 0.15)
        fltk.cercle(ax, ay, r, couleur="blue", remplissage="blue")
        fltk.texte(ax, ay, str(self.aventurier[1]), couleur="white", ancrage="center", taille=max(8, r // 2))

        # intention
        if self.intention:
            pts = [self.center_of_cell(self.intention[0])]
            for c in self.intention[1:]:
                pts.append(self.center_of_cell(c))
            for a, b in zip(pts, pts[1:]):
                fltk.ligne(a[0], a[1], b[0], b[1], couleur="red", epaisseur=3)

        fltk.mise_a_jour()

    def toggle_rotate_cell(self, cell: Cell):
        i, j = cell
        base.pivot_donjon(self.donjon, i, j)
        self.redessiner()

    def add_to_intention(self, cell: Cell):
        if not self.intention or self.intention[-1] != cell:
            self.intention.append(cell)
            self.redessiner()

    def clear_intention(self):
        self.intention = []
        self.redessiner()

    def appliquer_intention(self):
        if not self.intention:
            return
        chemin = list(self.intention)
        if chemin[0] != self.aventurier[0]:
            chemin = [self.aventurier[0]] + chemin

        res = moteur.appliquer_tour_aventurier(self.donjon, self.aventurier, self.dragons, chemin)
        status = res.get("status")

        if status in ("ongoing", "win"):
            path = chemin[1:]
            for p in path:
                self.aventurier[0] = p
                self.redessiner()
                fltk.attente(0.18)

        if status == "win":
            fltk.texte(self.window_w // 2, 20, "Victoire ! Tous les dragons sont morts.", couleur="green", ancrage="center", taille=20)
        elif status == "lose":
            fltk.texte(self.window_w // 2, 20, "Défaite ! L'aventurier est mort.", couleur="red", ancrage="center", taille=20)

        self.intention = []
        self.redessiner()

    def run(self):
        while True:
            ev = fltk.donne_ev()
            if ev is None:
                fltk.mise_a_jour()
                continue

            t = fltk.type_ev(ev)
            if t == "Quitte":
                fltk.ferme_fenetre()
                break
            elif t == "Redimension":
                self.window_w = fltk.largeur_fenetre()
                self.window_h = fltk.hauteur_fenetre()
                self.update_cell_size()
                self.redessiner()
            elif t == "ClicGauche":
                x = fltk.abscisse(ev)
                y = fltk.ordonnee(ev)
                if x is None or y is None:
                    continue
                cell = self.cell_from_xy(int(x), int(y))
                if fltk.touche_pressee('i'):
                    self.add_to_intention(cell)
                else:
                    self.toggle_rotate_cell(cell)
            elif t == "Touche":
                key = fltk.touche(ev)
                if key == "Escape":
                    fltk.ferme_fenetre()
                    break
                elif key in ("r", "R"):
                    self.nouvelle_partie()
                elif key == "space":
                    self.appliquer_intention()


def main():
    ui = Interface()
    ui.run()


if __name__ == '__main__':
    main()