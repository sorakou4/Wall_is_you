"""
# Projet Wall Is You - Tâche 1
# Interface graphique pour Wall Is You (utilise `fltk.py` existant).
# Auteur : Lohan, Daniel
# Date : 21 novembre 2025

Ce fichier affiche une grille carrée centrée, dessine des murs et des
ouvertures pour chaque salle (visible lors des rotations), et place
l'aventurier et les dragons au centre des cases.

Contrôles :
- Clic gauche = pivoter la salle
- Clic droit = ajouter à l'intention
- Espace = appliquer l'intention
- R = recommencer
- Échap = quitter
"""

import moteur
import fltk

# Variables globales
nb_lignes = 6
nb_colonnes = 8
nb_dragons = 5
graine_donjon = None
largeur_fenetre = 1000
hauteur_fenetre = 700
marge = 40
marge_droite = 200
taille_case = 0
grille_x0 = 0
grille_y0 = 0
donjon = None
aventurier = None
dragons = None
intention = []

# Dictionnaire qui associe un état de salle (tuple) à un nom de fichier image
ETATS_TEXTURE = {
    # --- Couloirs ---
    # (haut, droite, bas, gauche)
    (True, False, True, False): 'texture/nord-sud.png',
    (False, True, False, True): 'texture/ouest-est.png',

    # --- Coins ---
    (True, True, False, False): 'texture/nord-est.png',
    (False, True, True, False): 'texture/sud-est.png',
    (False, False, True, True): 'texture/ouest-sud.png',
    (True, False, False, True): 'texture/nord-ouest.png',

    # --- Culs-de-sac ---
    (True, False, False, False): 'texture/nord.png',
    (False, True, False, False): 'texture/est.png',
    (False, False, True, False): 'texture/sud.png',
    (False, False, False, True): 'texture/ouest.png',

    # --- autres passages ( 3 ou 4 passages) ---
    # (True, True, True, False): 'salle_T_bas.png',
    # (True, True, True, True): 'salle_croix.png',
}

def obtenir_texture_etat(etat_salle):
    """
    Retourne le fichier texture correspondant à l'état d'une salle.
    - etat_salle : tuple (N,E,S,O) indiquant les ouvertures
    """
    for etat, texture in ETATS_TEXTURE.items():
        if etat == etat_salle:
            return texture
    return None

def mettre_a_jour_taille_case():
    """
    Calcule la taille des cases et la position de la grille
    en fonction de la taille de la fenêtre.
    """
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

def obtenir_case_de_xy(x, y):
    """
    Convertit des coordonnées (x,y) en indices de case (i,j).
    Retourne la case correspondante dans la grille.
    """
    j = (x - grille_x0) // taille_case
    i = (y - grille_y0) // taille_case
    i = int(max(0, min(nb_lignes - 1, i)))
    j = int(max(0, min(nb_colonnes - 1, j)))
    return (i, j)

def centre_de_case(case):
    """
    Retourne les coordonnées du centre d'une case (i,j).
    """
    i, j = case
    cx = grille_x0 + j * taille_case + taille_case // 2
    cy = grille_y0 + i * taille_case + taille_case // 2
    return cx, cy

def afficher_commandes():
    """
    Affiche la liste des commandes disponibles sur le côté droit de l'écran.
    """
    x = largeur_fenetre - marge_droite + 20
    y = 60
    espacement = 30

    commandes = [
        ("Commandes:", "black", 14),
        ("", "black", 12),
        ("Clic gauche", "blue", 12),
        ("→ Pivoter une salle", "black", 12),
        ("", "black", 12),
        ("Clic droit", "blue", 12),
        ("→ Ajouter intention", "black", 12),
        ("", "black", 12),
        ("Espace", "blue", 12),
        ("→ Valider intention", "black", 12),
        ("", "black", 12),
        ("R", "blue", 12),
        ("→ Nouvelle partie", "black", 12),
        ("", "black", 12),
        ("Échap", "blue", 12),
        ("→ Quitter", "black", 12),
        ("", "black", 12),
    ]

    for texte, couleur, taille in commandes:
        fltk.texte(x, y, texte, couleur=couleur, ancrage='w', taille=taille)
        y += espacement

def rafraichir_affichage():
    """
    Redessine l'intégralité de l'interface :
    - Donjon (salles avec textures)
    - Aventurier et dragons
    - Intention (chemin en rouge)
    - Commandes et niveau du héros
    """
    fltk.efface_tout()
    niveau_aventurier = aventurier[1]
    fltk.texte(largeur_fenetre // 2, hauteur_fenetre - 30,
               "Niveau de l'aventurier : " + str(niveau_aventurier),ancrage="center", taille=18, couleur="blue")

    afficher_commandes()

    # Bordure du donjon
    largeur_donjon = taille_case * nb_colonnes
    hauteur_donjon = taille_case * nb_lignes
    epaisseur_bordure = 6
    x0 = grille_x0 - epaisseur_bordure
    y0 = grille_y0 - epaisseur_bordure
    x1 = grille_x0 + largeur_donjon + epaisseur_bordure
    y1 = grille_y0 + hauteur_donjon + epaisseur_bordure
    fltk.rectangle(x0, y0, x1, y1, remplissage="black", couleur="black")

    # Salles
    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            x0 = grille_x0 + j * taille_case
            y0 = grille_y0 + i * taille_case
            x1 = grille_x0 + (j + 1) * taille_case
            y1 = grille_y0 + (i + 1) * taille_case
            cx = (x0 + x1) // 2
            cy = (y0 + y1) // 2

            etat_salle = donjon[i][j]
            nom_image = obtenir_texture_etat(etat_salle)

            # Test de sécurité si le donjon n'est pas encore initialisé (ne devrait pas arriver ici)
            if donjon is None: 
                 fltk.rectangle(x0, y0, x1, y1, remplissage='red', couleur='black')
                 continue

            # Récupérer l'état de la salle (ex: (True, True, False, False))
            etat_salle = donjon[i][j]

            # Choisir le bon fichier image grâce au dictionnaire
            nom_image = ETATS_TEXTURE.get(etat_salle)

            # Si on a trouvé une image pour cet état, on l'affiche
            if nom_image:
                try:
                    fltk.image(cx, cy,nom_image,largeur=(x1 - x0), hauteur=(y1 - y0), ancrage='center')
                except Exception as e:
                    # En cas d'erreur (ex: image manquante ou format illisible), dessiner un carré ROSE
                    print(f"Erreur image {nom_image}: {e}")
                    fltk.rectangle(x0, y0, x1, y1, remplissage='pink', couleur='pink')
            else:
                # Si l'état n'est pas dans le dico

                # CAS 1: L'état est une salle fermée (0 passage)
                if etat_salle == (False, False, False, False):
                    # Dessiner un mur plein de couleur jaune
                    fltk.rectangle(x0, y0, x1, y1, remplissage='yellow', couleur='black')
                
                # CAS 2: L'état est un type de salle inconnu (ex: 3 ou 4 passages)
                else:
                    # Afficher en gris pour signaler un état non répertorié
                    print(f"DEBUG: État de salle inconnu en ({i}, {j}): {etat_salle}. Affiché en gris.")
                    fltk.rectangle(x0, y0, x1, y1, remplissage='grey', couleur='black')

    # Dragons
    for pos, niveau in dragons:
        cx, cy = centre_de_case(pos)
        fltk.image(cx, cy, "texture/dragon.png",
                   largeur=int(taille_case*0.6),
                   hauteur=int(taille_case*0.6),
                   ancrage="center")
        fltk.texte(cx, cy, str(niveau), couleur="red",
                   ancrage="center", taille=12)

    # Aventurier
    pos_x, pos_y = centre_de_case(aventurier[0])
    fltk.image(pos_x, pos_y, "texture/aventurier.png",
               largeur=int(taille_case * 0.6),
               hauteur=int(taille_case * 0.6),
               ancrage='center')

    # Intention (chemin en rouge)
    if intention:
        points = [centre_de_case(intention[0])]
        for case in intention[1:]:
            points.append(centre_de_case(case))
        for i in range(len(points) - 1):
            fltk.ligne(points[i][0], points[i][1],
                       points[i+1][0], points[i+1][1],
                       couleur="red", epaisseur=3)

    fltk.mise_a_jour()

def pivoter_case(case):
    """
    Fait pivoter la salle sélectionnée et rafraîchit l'affichage.
    """
    i, j = case
    moteur.faire_pivoter_donjon(donjon, i, j)
    rafraichir_affichage()

def ajouter_a_intention(case):
    """
    Ajoute une case au chemin d'intention de l'aventurier.
    - case : tuple (i,j) représentant une salle
    La case est ajoutée seulement si elle n'est pas déjà la dernière de la liste.
    """
    global intention
    if not intention or intention[-1] != case:
        intention.append(case)
        rafraichir_affichage()

def effacer_intention():
    """
    Réinitialise le chemin d'intention (liste vide).
    Rafraîchit l'affichage pour supprimer le tracé rouge.
    """
    global intention
    intention = []
    rafraichir_affichage()

def appliquer_intention():
    """
    Applique le chemin d'intention de l'aventurier :
    - Vérifie la validité du chemin
    - Déplace l'aventurier case par case
    - Gère les combats contre les dragons
    - Déplace les dragons après le tour du héros
    - Affiche victoire ou défaite si nécessaire
    """
    global aventurier, dragons

    if not intention:
        return

    chemin = list(intention)
    if chemin[0] != aventurier[0]:
        chemin = [aventurier[0]] + chemin

    # APPEL AU MOTEUR : vérification du chemin et combats
    resultat = moteur.appliquer_tour_aventurier(donjon, aventurier, dragons, chemin)
    statut, message, msg_combat = resultat[0], resultat[1], resultat[4]

    # Vérifier immédiatement la défaite
    if statut == "defaite":
        print("Défaite !", message)
        fltk.texte(largeur_fenetre // 2, 20, message,couleur="red", ancrage="center", taille=20)
        fltk.mise_a_jour()
        fltk.attente(2)
        fltk.ferme_fenetre()
        effacer_intention()
        return

    # Animation si l’aventurier est vivant
    if statut in ("en_cours", "victoire"):
        chemin_restant = chemin[1:]
        for position in chemin_restant:
            aventurier[0] = list(position)
            if msg_combat:
                print(msg_combat)
            rafraichir_affichage()
            fltk.attente(0.3)

        # Déplacer les dragons après le tour du héros
        fltk.attente(0.5)
        moteur.deplacer_dragons(donjon, aventurier, dragons)
        rafraichir_affichage()
        fltk.attente(0.3)

    # Vérifier la victoire
    if statut == "victoire":
        fltk.texte(largeur_fenetre // 2, 20, "Victoire !",couleur="green", ancrage="center", taille=20)
        fltk.mise_a_jour()
        fltk.attente(2)
        fltk.ferme_fenetre()
        effacer_intention()
        return

    effacer_intention()

def nouvelle_partie():
    """
    Initialise une nouvelle partie :
    - Génère un nouveau donjon avec aventurier et dragons
    - Réinitialise l'intention
    - Met à jour la taille des cases
    - Rafraîchit l'affichage
    """
    global donjon, aventurier, dragons, intention
    donjon, aventurier, dragons = moteur.creer_donjon(
        nb_lignes, nb_colonnes, nb_dragons, graine_donjon)
    intention = []
    mettre_a_jour_taille_case()
    rafraichir_affichage()

def programme_principal():
    """
    Boucle principale de l'interface graphique :
    - Crée la fenêtre
    - Lance une nouvelle partie
    - Gère les événements (clics, touches, redimensionnement, fermeture)
    """
    global largeur_fenetre, hauteur_fenetre

    fltk.cree_fenetre(largeur_fenetre, hauteur_fenetre)
    nouvelle_partie()

    partie_en_cours = True
    while partie_en_cours:
        evenement = fltk.donne_ev()
        if evenement is None:
            fltk.mise_a_jour()
            continue

        type_ev = fltk.type_ev(evenement)
        
        # Gestion des événements de fermeture
        if type_ev == "Quitte":
            partie_en_cours = False
            fltk.ferme_fenetre()
            break
        elif type_ev == "Touche":
            touche = fltk.touche(evenement)
            if touche == "Escape":
                partie_en_cours = False
                fltk.ferme_fenetre()
                break
            
            elif touche in ("r", "R"):
                nouvelle_partie()
                
            elif touche == "space":
                # Appel de la fonction pour appliquer le tour et obtenir le statut
                statut_fin = appliquer_intention() 
                
                # Vérification de la fin de partie
                if statut_fin is not None and (statut_fin[0] == "victoire" or statut_fin[0] == "defaite"):
                    partie_en_cours = False
                    fltk.mise_a_jour()
                    fltk.ferme_fenetre()
                    break
        
        # Gestion des autres événements
        elif type_ev == "Redimension":
            largeur_fenetre = fltk.largeur_fenetre()
            hauteur_fenetre = fltk.hauteur_fenetre()
            mettre_a_jour_taille_case()
            rafraichir_affichage()
        elif type_ev == "ClicGauche":
            x, y = fltk.abscisse(evenement), fltk.ordonnee(evenement)
            if x is not None and y is not None:
                case = obtenir_case_de_xy(int(x), int(y))
                pivoter_case(case)
        elif type_ev == "ClicDroit":
            x, y = fltk.abscisse(evenement), fltk.ordonnee(evenement)
            if x is not None and y is not None:
                case = obtenir_case_de_xy(int(x), int(y))
                ajouter_a_intention(case)


if __name__ == '__main__':
    nb_dragons = 3
    programme_principal()
