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
import moteur
import fltk

# Variables globales
nb_lignes = 6
nb_colonnes = 8
nb_dragons = 5
largeur_fenetre = 1000  # Augmenté pour avoir de l'espace pour les commandes
hauteur_fenetre = 700   # Augmenté pour avoir plus d'espace vertical
marge = 40
marge_droite = 200  # Espace pour les commandes à droite
taille_case = 0
grille_x0 = 0
grille_y0 = 0
donjon = None
aventurier = None
dragons = None
intention = []

def nouvelle_partie():
    global donjon, aventurier, dragons, intention
    donjon, aventurier, dragons = moteur.creer_donjon(nb_lignes, nb_colonnes, nb_dragons)
    intention = []
    mettre_a_jour_taille_case()
    rafraichir_affichage()

def mettre_a_jour_taille_case():
    global taille_case, grille_x0, grille_y0
    largeur_grille = largeur_fenetre - 2 * marge - marge_droite
    hauteur_grille = hauteur_fenetre - 2 * marge
    largeur_case = largeur_grille // nb_colonnes
    hauteur_case = hauteur_grille // nb_lignes
    taille_case = max(8, min(largeur_case, hauteur_case))
    largeur_totale = taille_case * nb_colonnes
    hauteur_totale = taille_case * nb_lignes
    grille_x0 = marge + (largeur_grille - largeur_totale) // 2
    grille_y0 = marge + (hauteur_grille - hauteur_totale) // 2

def obtenir_case_de_xy(x: int, y: int) -> Tuple[int, int]:
    j = (x - grille_x0) // taille_case
    i = (y - grille_y0) // taille_case
    i = int(max(0, min(nb_lignes - 1, i)))
    j = int(max(0, min(nb_colonnes - 1, j)))
    return (i, j)

def centre_de_case(case: Tuple[int, int]) -> Tuple[int, int]:
    i, j = case
    cx = grille_x0 + j * taille_case + taille_case // 2
    cy = grille_y0 + i * taille_case + taille_case // 2
    return cx, cy

def afficher_commandes():
    """Affiche la liste des commandes du jeu"""
    x = largeur_fenetre - marge_droite + 20
    y = 60
    espacement = 30

    commandes = [
        ("Commandes:", "black", 14),
        ("", "black", 12),  # Espace
        ("Clic gauche", "blue", 12),
        ("→ Pivoter une salle", "black", 12),
        ("", "black", 12),  # Espace
        ("'i' + Clic gauche", "blue", 12),
        ("→ Ajouter à l'intention", "black", 12),
        ("", "black", 12),  # Espace
        ("Espace", "blue", 12),
        ("→ Valider l'intention", "black", 12),
        ("", "black", 12),  # Espace
        ("R", "blue", 12),
        ("→ Nouvelle partie", "black", 12),
        ("", "black", 12),  # Espace
        ("Échap", "blue", 12),
        ("→ Quitter", "black", 12),
        ("", "black", 12),  # Espace
    ]

    for texte, couleur, taille in commandes:
        fltk.texte(x, y, texte, couleur=couleur, ancrage='w', taille=taille)
        y += espacement

def rafraichir_affichage():
    fltk.efface_tout()
    
    # Afficher les commandes
    afficher_commandes()
    
    # Dessiner la grille
    marge_case = 2  # Espace entre les cases en pixels
    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            # Calculer les coordonnées avec la marge
            x0 = grille_x0 + j * taille_case + marge_case
            y0 = grille_y0 + i * taille_case + marge_case
            x1 = grille_x0 + (j + 1) * taille_case - marge_case
            y1 = grille_y0 + (i + 1) * taille_case - marge_case
            cx = (x0 + x1) // 2
            cy = (y0 + y1) // 2

            haut, droite, bas, gauche = donjon[i][j]
            gap = (x1 - x0) // 3  # Ajuster la taille du passage en fonction de la nouvelle taille

            # Les murs sont dessinés avec un espace au milieu si le passage est ouvert

            # Dessin du mur du haut
            if haut:  # Si le passage est ouvert
                fltk.ligne(x0, y0, cx - gap//2, y0, couleur="black", epaisseur=2)
                fltk.ligne(cx + gap//2, y0, x1, y0, couleur="black", epaisseur=2)
            else:  # Si le mur est fermé
                fltk.ligne(x0, y0, x1, y0, couleur="black", epaisseur=2)

            # Dessin du mur du bas
            if bas:  # Si le passage est ouvert
                fltk.ligne(x0, y1, cx - gap//2, y1, couleur="black", epaisseur=2)
                fltk.ligne(cx + gap//2, y1, x1, y1, couleur="black", epaisseur=2)
            else:  # Si le mur est fermé
                fltk.ligne(x0, y1, x1, y1, couleur="black", epaisseur=2)

            # Dessin du mur de gauche
            if gauche:  # Si le passage est ouvert
                fltk.ligne(x0, y0, x0, cy - gap//2, couleur="black", epaisseur=2)
                fltk.ligne(x0, cy + gap//2, x0, y1, couleur="black", epaisseur=2)
            else:  # Si le mur est fermé
                fltk.ligne(x0, y0, x0, y1, couleur="black", epaisseur=2)

            # Dessin du mur de droite
            if droite:  # Si le passage est ouvert
                fltk.ligne(x1, y0, x1, cy - gap//2, couleur="black", epaisseur=2)
                fltk.ligne(x1, cy + gap//2, x1, y1, couleur="black", epaisseur=2)
            else:  # Si le mur est fermé
                fltk.ligne(x1, y0, x1, y1, couleur="black", epaisseur=2)

    # Dessiner les dragons
    for dragon in dragons:
        position, niveau = dragon
        cx, cy = centre_de_case(position)
        rayon = int((taille_case - 4) * 0.15)  # Ajuster la taille en fonction de la case réduite
        fltk.cercle(cx, cy, rayon, couleur="red", remplissage="red")
        fltk.texte(cx, cy, str(niveau), couleur="white", ancrage="center", taille=max(8, rayon // 2))

    # Dessiner l'aventurier
    pos_x, pos_y = centre_de_case(aventurier[0])
    rayon = int((taille_case - 4) * 0.15)  # Ajuster la taille en fonction de la case réduite
    fltk.cercle(pos_x, pos_y, rayon, couleur="blue", remplissage="blue")
    fltk.texte(pos_x, pos_y, str(aventurier[1]), couleur="white", ancrage="center", taille=max(8, rayon // 2))

    # Dessiner l'intention
    if intention:
        points = [centre_de_case(intention[0])]
        for case in intention[1:]:
            points.append(centre_de_case(case))
        for point1, point2 in zip(points, points[1:]):
            fltk.ligne(point1[0], point1[1], point2[0], point2[1], couleur="red", epaisseur=3)

    fltk.mise_a_jour()

def pivoter_case(case: Tuple[int, int]):
    i, j = case
    moteur.faire_pivoter_donjon(donjon, i, j)
    rafraichir_affichage()

def ajouter_a_intention(case: Tuple[int, int]):
    global intention
    if not intention or intention[-1] != case:
        intention.append(case)
        rafraichir_affichage()

def effacer_intention():
    global intention
    intention = []
    rafraichir_affichage()

def appliquer_intention():
    global aventurier
    if not intention:
        return
    chemin = list(intention)
    if chemin[0] != aventurier[0]:
        chemin = [aventurier[0]] + chemin

    resultat = moteur.appliquer_tour_aventurier(donjon, aventurier, dragons, chemin)
    statut = resultat.get("statut")

    if statut in ("en_cours", "victoire"):
        chemin_restant = chemin[1:]
        for position in chemin_restant:
            aventurier[0] = position
            if resultat.get("combat_message"):
                print(resultat["combat_message"])  # Afficher le message de combat en console
            rafraichir_affichage()
            fltk.attente(0.18)

    if statut == "victoire":
        message = "Victoire ! Tous les dragons sont morts."
        print(message)
        fltk.texte(largeur_fenetre // 2, 20, message, couleur="green", ancrage="center", taille=20)
        # Mettre à jour l'affichage, laisser le message visible puis fermer la fenêtre
        fltk.mise_a_jour()
        fltk.attente(2)  # Attendre 2 secondes pour que le message soit visible
        fltk.ferme_fenetre()
        return
    elif statut == "defaite":
        message = f"Défaite ! {resultat.get('message', 'L''aventurier est mort.')}"
        print(message)
        fltk.texte(largeur_fenetre // 2, 20, message, couleur="red", ancrage="center", taille=20)
        fltk.mise_a_jour()
        fltk.attente(2)  # Attendre 2 secondes pour que le message soit visible
        fltk.ferme_fenetre()
        return

    effacer_intention()

def programme_principal():
    global largeur_fenetre, hauteur_fenetre
    # Création de la fenêtre
    fltk.cree_fenetre(largeur_fenetre, hauteur_fenetre)
    nouvelle_partie()

    while True:
        evenement = fltk.donne_ev()
        if evenement is None:
            fltk.mise_a_jour()
            continue

        type_ev = fltk.type_ev(evenement)
        if type_ev == "Quitte":
            fltk.ferme_fenetre()
            break
        elif type_ev == "Redimension":
            largeur_fenetre = fltk.largeur_fenetre()
            hauteur_fenetre = fltk.hauteur_fenetre()
            mettre_a_jour_taille_case()
            rafraichir_affichage()
        elif type_ev == "ClicGauche":
            x = fltk.abscisse(evenement)
            y = fltk.ordonnee(evenement)
            if x is None or y is None:
                continue
            case = obtenir_case_de_xy(int(x), int(y))
            if fltk.touche_pressee('i'):
                ajouter_a_intention(case)
            else:
                pivoter_case(case)
        elif type_ev == "Touche":
            touche = fltk.touche(evenement)
            if touche == "Escape":
                fltk.ferme_fenetre()
                break
            elif touche in ("r", "R"):
                nouvelle_partie()
            elif touche == "space":
                appliquer_intention()

if __name__ == '__main__':
    programme_principal()