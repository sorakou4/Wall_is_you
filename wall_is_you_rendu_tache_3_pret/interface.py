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

import os
import moteur
import fltk
import chargement_donjon

# Variables globales
nb_lignes = 6
nb_colonnes = 8
nb_dragons = 5
nb_bonus = 1
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
bonus = None
intention = []



def obtenir_texture_etat(etat):
    """
    Retourne le fichier texture correspondant à l'état d'une salle.
    Paramètres : haut, droite, bas, gauche (booléens)
    """
    haut, droite, bas, gauche = etat

    # --- Couloirs ---
    if haut and not droite and bas and not gauche:
        return 'texture/nord-sud.png'
    if not haut and droite and not bas and gauche:
        return 'texture/ouest-est.png'

    # --- Coins ---
    if haut and droite and not bas and not gauche:
        return 'texture/nord-est.png'
    if not haut and droite and bas and not gauche:
        return 'texture/sud-est.png'
    if not haut and not droite and bas and gauche:
        return 'texture/ouest-sud.png'
    if haut and not droite and not bas and gauche:
        return 'texture/nord-ouest.png'

    # --- Culs-de-sac ---
    if haut and not droite and not bas and not gauche:
        return 'texture/nord.png'
    if not haut and droite and not bas and not gauche:
        return 'texture/est.png'
    if not haut and not droite and bas and not gauche:
        return 'texture/sud.png'
    if not haut and not droite and not bas and gauche:
        return 'texture/ouest.png'

    # --- Trois ouvertures ---
    if haut and droite and bas and not gauche:
        return 'texture/nord-est-sud.png'
    if not haut and droite and bas and gauche:
        return 'texture/est-sud-ouest.png'
    if haut and not droite and bas and gauche:
        return 'texture/nord-sud-ouest.png'
    if haut and droite and not bas and gauche:
        return 'texture/nord-est-ouest.png'
    # --- Quatre ouvertures ---
    if haut and droite and bas and gauche:
        return 'texture/nord-est-sud-ouest.png'
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
            nom_image = obtenir_texture_etat(etat_salle)

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
    
    # Bonus
    global bonus
    if bonus:
        for pos in bonus:
            cx, cy = centre_de_case(pos)
            fltk.image(cx, cy, "texture/bonus.png",
                       largeur=int(taille_case * 0.3),
                       hauteur=int(taille_case * 0.3),
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
    Gère le clic droit sur une case pour l'intention :
    1. Si la case est déjà dans l'intention, coupe l'intention après cette case.
    2. Si la case est nouvelle, elle est ajoutée UNIQUEMENT si elle est connectée par une porte ouverte à la dernière case du chemin.
    """
    global intention, donjon, aventurier

    case_list = list(case)

    if case_list in intention:
        try:
            index = intention.index(case_list)
            # Coupe la liste d'intention après cette position
            intention = intention[:index + 1]
            rafraichir_affichage()
            return # Sortir après la coupure
        except ValueError:
            pass
            
    # Gère l'ajout d'une nouvelle case (avec validation)

    if not intention:
        # Si l'intention est vide, le départ est la position actuelle de l'aventurier
        pos_depart = aventurier[0]
    else:
        # Sinon, le départ est la dernière case de l'intention
        pos_depart = intention[-1]

    if moteur.sont_salles_connectees(donjon, pos_depart, case_list):
        # Si le mouvement est valide (adjacent et porte ouverte), on ajoute
        intention.append(case_list)
        rafraichir_affichage()
        # Pour pas avoir de spam comme au dernier test xd
    else:
        pass 

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

def nouvelle_partie(fichier="donjons/donjon_niv1.txt"):
    """
    Démarre une nouvelle partie en chargeant un fichier de donjon.
    """
    global donjon, aventurier, dragons, bonus, intention, nb_lignes, nb_colonnes

    # Charger les données
    donjon, aventurier, dragons, bonus = chargement_donjon.charger_donjon(fichier)
    # Propager le bonus au moteur afin que la logique de jeu y ait accès
    try:
        moteur.bonus = bonus
    except Exception:
        pass

    # Réinitialiser le chemin
    intention = []

    # Adapter l’affichage
    nb_lignes = len(donjon)
    nb_colonnes = len(donjon[0])
    mettre_a_jour_taille_case()
    rafraichir_affichage()

def programme_principal(fichier="donjons/donjon_niv1.txt"):
    """
    Boucle principale de l'interface graphique :
    - Crée la fenêtre
    - Lance une nouvelle partie
    - Gère les événements (clics, touches, redimensionnement, fermeture)
    """
    global largeur_fenetre, hauteur_fenetre

    fltk.cree_fenetre(largeur_fenetre, hauteur_fenetre)
    nouvelle_partie(fichier)

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
            
            elif touche in ("s", "S"):
                save_donjon()

            elif touche in ("l", "L"):
                chargement_donjon.load_donjon()
                
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

def save_donjon(fichier="sauvegarde.txt"):
    """
    Sauvegarde le donjon en texte EXACTEMENT comme un fichier de donjon.
    Très simple et lisible pour débutants.
    """
    global donjon, aventurier, dragons

    f = open(fichier, "w", encoding="utf-8")

    # --- 1) Grille en box drawing ---
    for ligne in donjon:
        ligne_txt = "".join(chargement_donjon.salle_to_char(s) for s in ligne)
        f.write(ligne_txt + "\n")

    # --- 2) Aventurier ---
    coord,niv = aventurier[0], aventurier[1]
    i,j = coord[0], coord[1]
    f.write("A")
    f.write(" ")
    f.write(str(i))
    f.write(" ")
    f.write(str(j))
    f.write(" ")
    f.write(str(niv))
    f.write("\n")

    # --- 3) Dragons ---
    for pos, niv in dragons:
        f.write("D")
        f.write(" ")
        f.write(str(pos[0]))
        f.write(" ")
        f.write(str(pos[1]))
        f.write(" ")
        f.write(str(niv))
        f.write("\n")

    print("Donjon sauvegardé sous forme box-drawing.")

if __name__ == '__main__':
    programme_principal()
