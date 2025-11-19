from typing import Tuple
import fltk
import moteur
import interface

# Taille fenêtre
LARGEUR = 400
HAUTEUR = 500
MARGE = 40

# Couleurs
COULEUR_FOND = "darkslategray"
COULEUR_BOUTON = "darkgrey"
COULEUR_BOUTON_HOVER = "grey"
COULEUR_TEXTE = "black"

# Etat de l'UI
afficher_sous_boutons = False
logo_emplacement = None  # mettre "chemin/vers/logo.png" dans le main pour avoir le logo

# Définition simple d'un bouton rectangulaire
class Bouton:
    def __init__(self, x, y, w, h, texte):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.texte = texte

    def dessiner(self, souris_pos: Tuple[int,int] = (None, None)):
        mx, my = souris_pos
        hover = False
        if mx is not None and my is not None:
            hover = (self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h)
        couleur = COULEUR_BOUTON_HOVER if hover else COULEUR_BOUTON
        fltk.rectangle(self.x, self.y, self.x + self.w, self.y + self.h, remplissage=couleur, couleur="black")
        fltk.texte(self.x + self.w // 2, self.y + self.h // 2, self.texte, ancrage="center", couleur=COULEUR_TEXTE, taille=14)

    def contient(self, px, py):
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h

# Créer les boutons principaux
def creer_boutons():
    w_btn = 220
    h_btn = 50
    gap = 20
    cx = LARGEUR // 2
    top_y = 220

    btn_charger = Bouton(cx - w_btn // 2, top_y, w_btn, h_btn, "Charger un donjon")
    btn_quitter = Bouton(cx - w_btn // 2, top_y + (h_btn + gap), w_btn, h_btn, "Quitter")
    # bouton retour en bas gauche (pour les sous-menus)
    btn_retour = Bouton(20, HAUTEUR - 20 - 40, 120, 40, "Retour")
    # sous-boutons (invisibles tant que afficher_sous_boutons == False)
    sb_w = 120
    sb_h = 40
    sb_x = cx - sb_w // 2
    sb_y0 = top_y + h_btn - 30
    sb1 = Bouton(sb_x, sb_y0, sb_w, sb_h, "Donjon 1")
    sb2 = Bouton(sb_x, sb_y0 + sb_h + 8, sb_w, sb_h, "Donjon 2")
    sb3 = Bouton(sb_x, sb_y0 + 2*(sb_h + 8), sb_w, sb_h, "Donjon 3")

    return btn_charger, btn_quitter, btn_retour, (sb1, sb2, sb3)

btn_charger, btn_quitter, btn_retour, sous_boutons = creer_boutons()

def dessiner_menu(mx=None, my=None):
    # fond
    fltk.rectangle(0, 0, LARGEUR, HAUTEUR, remplissage=COULEUR_FOND, couleur=COULEUR_FOND)

    # Si on affiche le sous-menu, on ne dessine que les sous-boutons et le bouton retour
    if afficher_sous_boutons:
        # zone de fond pour le sous-menu (centrée)
        zone_w = 360
        zone_h = 220
        zone_x = (LARGEUR - zone_w) // 2
        zone_y = 180
        fltk.rectangle(zone_x, zone_y, zone_x + zone_w, zone_y + zone_h, remplissage="darkgrey", couleur="black")
        fltk.texte(LARGEUR // 2, zone_y + 20, "Choisir un donjon", ancrage="center", taille=16, couleur="black")

        # dessiner uniquement les sous-boutons et le bouton retour
        for sb in sous_boutons:
            sb.dessiner((mx, my))
        btn_retour.dessiner((mx, my))

        fltk.mise_a_jour()
        return

    # emplacement logo (milieu haut)
    logo_w = 360
    logo_h = 140
    logo_x = (LARGEUR - logo_w) // 2
    logo_y = 60
    fltk.rectangle(logo_x, logo_y, logo_x + logo_w, logo_y + logo_h, remplissage="white", couleur="black")
    fltk.texte(LARGEUR // 2, logo_y + logo_h // 2, "LOGO ICI", ancrage="center", taille=18, couleur="black")
    # si logo_logo_emplacement défini, tentative d'afficher l'image 
    if logo_emplacement:
        try:
            fltk.image(LARGEUR // 2, logo_y + logo_h // 2, logo_emplacement, largeur=logo_w, hauteur=logo_h, ancrage="center")
        except Exception:
            pass

    # dessiner boutons principaux
    btn_charger.dessiner((mx, my))
    btn_quitter.dessiner((mx, my))

    # texte centré en bas
    texte_bas = "Wall Is You — Prototype de menu"
    fltk.texte(LARGEUR // 2, HAUTEUR - 18, texte_bas, ancrage="center", taille=12, couleur="black")

    fltk.mise_a_jour()

def programme_menu():
    global afficher_sous_boutons
    fltk.cree_fenetre(LARGEUR, HAUTEUR)
    dessiner_menu()

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
            # si tu veux gérer redimension, tu peux mettre à jour LARGEUR/HAUTEUR et recréer boutons
            dessiner_menu()
        elif t == "ClicGauche":
            x = fltk.abscisse(ev)
            y = fltk.ordonnee(ev)
            if x is None or y is None:
                continue

            if afficher_sous_boutons:
                # si on est dans le sous-menu, ne traiter que les sous-boutons et le retour
                for idx, sb in enumerate(sous_boutons, start=1):
                    if sb.contient(x, y):
                        fltk.ferme_fenetre()
                        if idx == 1:
                            interface.programme_principal(moteur.creer_donjon1)
                        elif idx == 2:
                            interface.programme_principal(moteur.creer_donjon2)
                        elif idx == 3:
                            interface.programme_principal(moteur.creer_donjon3)
                        break
                if btn_retour.contient(x, y):
                    afficher_sous_boutons = False
                dessiner_menu(x, y)
                continue

            # Si on n'est pas dans le sous-menu, traiter les boutons du menu principal
            if btn_charger.contient(x, y):
                afficher_sous_boutons = True
                dessiner_menu(x, y)
                continue
            if btn_quitter.contient(x, y):
                fltk.ferme_fenetre()
                break

            dessiner_menu(x, y)

        elif t == "SourisDeplace":
            mx = fltk.abscisse(ev)
            my = fltk.ordonnee(ev)
            dessiner_menu(mx, my)
        elif t == "Touche":
            key = fltk.touche(ev)
            if key == "Escape":
                fltk.ferme_fenetre()
                break

if __name__ == "__main__":
    logo_emplacement = "texture/logo.png"
    programme_menu()
