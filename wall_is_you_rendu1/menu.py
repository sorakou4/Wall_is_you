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
logo_emplacement = "texture/logo.png"

# Boutons: chaque bouton est une liste [x, y, w, h, texte]
def creer_boutons():
    w_btn = 220
    h_btn = 50
    gap = 20
    cx = LARGEUR // 2
    top_y = 220

    btn_charger = [cx - w_btn // 2, top_y, w_btn, h_btn, "Charger un donjon"]
    btn_quitter = [cx - w_btn // 2, top_y + (h_btn + gap), w_btn, h_btn, "Quitter"]
    btn_retour = [20, HAUTEUR - 20 - 40, 120, 40, "Retour"]
    
    sb_w = 120
    sb_h = 40
    sb_x = cx - sb_w // 2
    sb_y0 = top_y + h_btn - 30
    sb1 = [sb_x, sb_y0, sb_w, sb_h, "Facile"]
    sb2 = [sb_x, sb_y0 + sb_h + 8, sb_w, sb_h, "Moyen"]
    sb3 = [sb_x, sb_y0 + 2*(sb_h + 8), sb_w, sb_h, "Difficile"]

    return btn_charger, btn_quitter, btn_retour, [sb1, sb2, sb3]

btn_charger, btn_quitter, btn_retour, sous_boutons = creer_boutons()

def bouton_contient(bouton, px, py):
    x = bouton[0]
    y = bouton[1]
    w = bouton[2]
    h = bouton[3]
    return x <= px <= x + w and y <= py <= y + h

def bouton_souris_hover(bouton, mx, my):
    if mx is None or my is None:
        return False
    return bouton_contient(bouton, mx, my)

def dessiner_bouton(bouton, mx=None, my=None):
    x = bouton[0]
    y = bouton[1]
    w = bouton[2]
    h = bouton[3]
    texte = bouton[4]
    
    hover = bouton_souris_hover(bouton, mx, my)
    couleur = COULEUR_BOUTON_HOVER if hover else COULEUR_BOUTON
    fltk.rectangle(x, y, x + w, y + h, remplissage=couleur, couleur="black")
    fltk.texte(x + w // 2, y + h // 2, texte, ancrage="center", couleur=COULEUR_TEXTE, taille=14)

def dessiner_menu(mx=None, my=None):
    fltk.rectangle(0, 0, LARGEUR, HAUTEUR, remplissage=COULEUR_FOND, couleur=COULEUR_FOND)

    if afficher_sous_boutons:
        zone_w = 360
        zone_h = 220
        zone_x = (LARGEUR - zone_w) // 2
        zone_y = 180
        fltk.rectangle(zone_x, zone_y, zone_x + zone_w, zone_y + zone_h, remplissage="darkgrey", couleur="black")
        fltk.texte(LARGEUR // 2, zone_y + 20, "Choisir un donjon", ancrage="center", taille=16, couleur="black")

        for sb in sous_boutons:
            dessiner_bouton(sb, mx, my)
        dessiner_bouton(btn_retour, mx, my)

        fltk.mise_a_jour()
        return

    logo_w = 360
    logo_h = 140
    logo_x = (LARGEUR - logo_w) // 2
    logo_y = 60
    fltk.rectangle(logo_x, logo_y, logo_x + logo_w, logo_y + logo_h, remplissage="white", couleur="black")
    fltk.texte(LARGEUR // 2, logo_y + logo_h // 2, "LOGO ICI", ancrage="center", taille=18, couleur="black")
    if logo_emplacement:
        try:
            fltk.image(LARGEUR // 2, logo_y + logo_h // 2, logo_emplacement, largeur=logo_w, hauteur=logo_h, ancrage="center")
        except Exception:
            pass

    dessiner_bouton(btn_charger, mx, my)
    dessiner_bouton(btn_quitter, mx, my)

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
            dessiner_menu()
        elif t == "ClicGauche":
            x = fltk.abscisse(ev)
            y = fltk.ordonnee(ev)
            if x is None or y is None:
                continue

            if afficher_sous_boutons:
                idx = 0
                while idx < len(sous_boutons):
                    sb = sous_boutons[idx]
                    if bouton_contient(sb, x, y):
                        fltk.ferme_fenetre()
                        if idx == 0:
                            interface.nb_dragons = 3
                            interface.graine_donjon = 42
                        elif idx == 1:
                            interface.nb_dragons = 4
                            interface.graine_donjon = 123
                        elif idx == 2:
                            interface.nb_dragons = 5
                            interface.graine_donjon = 456
                        interface.programme_principal()
                        break
                    idx = idx + 1
                if bouton_contient(btn_retour, x, y):
                    afficher_sous_boutons = False
                dessiner_menu(x, y)
                continue

            if bouton_contient(btn_charger, x, y):
                afficher_sous_boutons = True
                dessiner_menu(x, y)
                continue
            if bouton_contient(btn_quitter, x, y):
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
    programme_menu()
