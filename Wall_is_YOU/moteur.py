"""
Moteur du jeu "Wall Is You"

Ce fichier contient toutes les fonctionnalités nécessaires pour le jeu:
- Création et gestion du donjon
- Gestion des salles et leurs rotations
- Création et gestion de l'aventurier et des dragons
- Vérification des chemins et déplacements
- Gestion des combats
"""

from random import randrange

def creer_salle():
    """Crée une salle avec tous les murs fermés"""
    return (False, False, False, False)

def creer_donjon(nb_lignes, nb_colonnes, nb_dragons):
    """
    Crée un donjon avec:
    - Des salles ayant deux passages ouverts
    - Un aventurier de niveau 1 placé aléatoirement
    - Des dragons placés aléatoirement avec des niveaux croissants
    """
    # Création du donjon avec toutes les salles fermées
    donjon = [[creer_salle() for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
    
    def trouver_voisins(ligne, colonne):
        """Retourne les positions des salles voisines possibles"""
        salles_voisines = []
        if ligne > 0:
            salles_voisines.append((ligne-1, colonne))
        if ligne < nb_lignes - 1:
            salles_voisines.append((ligne+1, colonne))
        if colonne > 0:
            salles_voisines.append((ligne, colonne-1))
        if colonne < nb_colonnes - 1:
            salles_voisines.append((ligne, colonne+1))
        return salles_voisines

    # Création du chemin en serpentin pour garantir deux passages par salle
    toutes_salles = [(i, j) for i in range(nb_lignes) for j in range(nb_colonnes)]
    for k in range(len(toutes_salles)-1):
        salle1 = toutes_salles[k]
        salle2 = toutes_salles[k+1]
        i1, j1 = salle1
        i2, j2 = salle2
        
        # Ouvrir les passages entre les salles
        salle_actuelle = list(donjon[i1][j1])
        salle_suivante = list(donjon[i2][j2])
        
        if i1 == i2:  # Même ligne
            if j2 > j1:  # Salle2 à droite
                salle_actuelle[1] = True  # Ouvrir à droite
                salle_suivante[3] = True  # Ouvrir à gauche
            else:  # Salle2 à gauche
                salle_actuelle[3] = True  # Ouvrir à gauche
                salle_suivante[1] = True  # Ouvrir à droite
        else:  # Même colonne
            if i2 > i1:  # Salle2 en bas
                salle_actuelle[2] = True  # Ouvrir en bas
                salle_suivante[0] = True  # Ouvrir en haut
            else:  # Salle2 en haut
                salle_actuelle[0] = True  # Ouvrir en haut
                salle_suivante[2] = True  # Ouvrir en bas
        
        donjon[i1][j1] = tuple(salle_actuelle)
        donjon[i2][j2] = tuple(salle_suivante)

    # Création de l'aventurier : [position, niveau]
    aventurier = [(randrange(nb_lignes), randrange(nb_colonnes)), 1]

    # Création des dragons : liste de [position, niveau]
    dragons = []
    for niveau in range(2, 2 + nb_dragons):
        position = (randrange(nb_lignes), randrange(nb_colonnes))
        dragons.append([position, niveau])

    return donjon, aventurier, dragons

def faire_pivoter_salle(salle):
    """Fait pivoter une salle de 90° vers la droite (sens horaire)"""
    mur_haut, mur_droite, mur_bas, mur_gauche = salle
    # Pour une rotation de 90° vers la droite (sens horaire) :
    # - le mur du haut devient le mur de droite
    # - le mur de droite devient le mur du bas
    # - le mur du bas devient le mur de gauche
    # - le mur de gauche devient le mur du haut
    # Dans le tuple (haut, droite, bas, gauche), chaque élément se déplace
    # d'une position vers la droite
    return (mur_gauche, mur_haut, mur_droite, mur_bas)

def faire_pivoter_donjon(donjon, ligne, colonne):
    """Fait pivoter la salle en position (ligne,colonne) du donjon"""
    donjon[ligne][colonne] = faire_pivoter_salle(donjon[ligne][colonne])

def sont_salles_connectees(donjon, position1, position2):
    """Vérifie si deux salles adjacentes sont connectées par un passage"""
    ligne1, colonne1 = position1
    ligne2, colonne2 = position2
    salle1 = donjon[ligne1][colonne1]
    salle2 = donjon[ligne2][colonne2]

    # Vérification des connexions selon la position relative
    if ligne1 == ligne2:  # Même ligne
        if colonne1 + 1 == colonne2:  # Salle2 à droite
            return salle1[1] and salle2[3]
        elif colonne1 - 1 == colonne2:  # Salle2 à gauche
            return salle1[3] and salle2[1]
    elif colonne1 == colonne2:  # Même colonne
        if ligne1 + 1 == ligne2:  # Salle2 en bas
            return salle1[2] and salle2[0]
        elif ligne1 - 1 == ligne2:  # Salle2 en haut
            return salle1[0] and salle2[2]
    return False

def verifier_chemin(donjon, chemin):
    """Vérifie si le chemin est valide (salles connectées)"""
    if not chemin:
        return False
    for index in range(len(chemin) - 1):
        if not sont_salles_connectees(donjon, chemin[index], chemin[index + 1]):
            return False
    return True

def trouver_dragon(dragons, position):
    """Trouve un dragon à une position donnée"""
    for index, dragon in enumerate(dragons):
        if dragon[0] == position:
            return index
    return None

def partie_gagnee(dragons):
    """Vérifie si la partie est gagnée (tous les dragons éliminés)"""
    return len(dragons) == 0

def appliquer_tour_aventurier(donjon, aventurier, dragons, chemin):
    """
    Applique le déplacement de l'aventurier et gère les combats
    Retourne un dictionnaire avec le statut et les mises à jour
    """
    if not chemin:
        return {
            "statut": "chemin_invalide",
            "message": "Le chemin est vide.",
            "aventurier": aventurier,
            "dragons": dragons,
        }

    # Ajouter la position de départ si nécessaire
    if chemin[0] != aventurier[0]:
        chemin = [aventurier[0]] + chemin

    # Vérifier la validité du chemin
    if not verifier_chemin(donjon, chemin):
        return {
            "statut": "chemin_invalide",
            "message": "Le chemin n'est pas valide (salles non connectées).",
            "aventurier": aventurier,
            "dragons": dragons,
        }

    # Déplacer l'aventurier et gérer les combats
    for position_courante in chemin[1:]:
        aventurier[0] = position_courante
        indice_dragon = trouver_dragon(dragons, position_courante)
        
        if indice_dragon is not None:
            dragon = dragons[indice_dragon]
            if dragon[1] <= aventurier[1] + 1:
                # L'aventurier gagne le combat
                message_combat = f"Dragon niveau {dragon[1]} vaincu ! L'aventurier gagne 1 niveau."
                del dragons[indice_dragon]
                aventurier[1] += 1
            else:
                # L'aventurier perd le combat
                return {
                    "statut": "defaite",
                    "message": f"L'aventurier (niveau {aventurier[1]}) a été vaincu par un dragon de niveau {dragon[1]} !",
                    "aventurier": aventurier,
                    "dragons": dragons,
                }

    # Vérifier la victoire
    if partie_gagnee(dragons):
        return {
            "statut": "victoire",
            "message": "Victoire ! Tous les dragons ont été vaincus !",
            "aventurier": aventurier,
            "dragons": dragons,
        }

    return {
        "statut": "en_cours",
        "message": "Tour terminé.",
        "combat_message": message_combat if 'message_combat' in locals() else None,
        "aventurier": aventurier,
        "dragons": dragons,
    }

def afficher_etat_jeu(donjon, aventurier, dragons):
    """Affiche l'état du jeu (pour le débogage)"""
    print("=== État du jeu ===")
    print(f"Aventurier : position {aventurier[0]}, niveau {aventurier[1]}")
    print("Dragons :")
    for dragon in dragons:
        print(f" - Dragon niveau {dragon[1]} en position {dragon[0]}")
    print("===================")
