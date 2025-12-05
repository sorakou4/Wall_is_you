# Projet Wall Is You - Tâche 1
# Moteur de jeu (logique interne)
# Auteur : Lohan, Daniel
# Date : 21 novembre 2025

import random

def creer_donjon(nl, nc, nd, graine=None):
    """
    Crée un donjon rectangulaire de dimensions (nl x nc) avec un aventurier et nd dragons.
    Génère un chemin en serpentin pour garantir que les salles sont connectées.
    """
    if graine is not None:
        random.seed(graine)

    # Initialisation des salles (tout fermé au départ)
    donjon = [[[False, False, False, False] for _ in range(nc)] for _ in range(nl)]

    # Cela garantit que la salle k et k+1 sont toujours voisines
    salles = []
    for i in range(nl):
        if i % 2 == 0:
            # Lignes paires : de Gauche à Droite
            for j in range(nc):
                salles.append((i, j))
        else:
            # Lignes impaires : de Droite à Gauche
            for j in range(nc - 1, -1, -1):
                salles.append((i, j))

    # Relier les salles (plus de random.shuffle ici pour garder l'ordre du serpentin)
    k = 0
    while k < len(salles) - 1:
        i1, j1 = salles[k]
        i2, j2 = salles[k + 1]
        
        s1 = donjon[i1][j1]
        s2 = donjon[i2][j2]

        if i1 == i2:  # connexion horizontale (même ligne)
            if j2 > j1: # s2 est à droite
                s1[1] = True # Ouvre Est de s1
                s2[3] = True # Ouvre Ouest de s2
            else:       # s2 est à gauche
                s1[3] = True # Ouvre Ouest de s1
                s2[1] = True # Ouvre Est de s2
        elif j1 == j2:  # connexion verticale (même colonne)
            if i2 > i1: # s2 est en bas
                s1[2] = True # Ouvre Sud de s1
                s2[0] = True # Ouvre Nord de s2
            else:       # s2 est en haut
                s1[0] = True # Ouvre Nord de s1
                s2[2] = True # Ouvre Sud de s2

        k += 1

    # Mélanger l’orientation des salles (rotation aléatoire)
    for i in range(nl):
        for j in range(nc):
            rotations = random.randrange(4)
            s = donjon[i][j]
            for _ in range(rotations):
                s = (s[3], s[0], s[1], s[2])
            donjon[i][j] = s

    # Position initiale de l’aventurier
    aventurier = [[random.randrange(nl), random.randrange(nc)], 1]
    dragons = []

    occ = [aventurier[0]] # Positions occupées

    # Placement des dragons en évitant les collisions
    for n in range(1, 1 + nd):
        while True:
            p = [random.randrange(nl), random.randrange(nc)]
            if p not in occ:
                occ.append(p)
                dragons.append([p, n])
                break

    return donjon, aventurier, dragons

def creer_donjon_niveau1():
    """Crée un donjon de niveau 1 (6x8, 3 dragons, graine 42)."""
    return creer_donjon(6, 8, 3, 42)

def creer_donjon_niveau2():
    """Crée un donjon de niveau 2 (6x8, 4 dragons, graine 123)."""
    return creer_donjon(6, 8, 4, 123)

def creer_donjon_niveau3():
    """Crée un donjon de niveau 3 (6x8, 5 dragons, graine 456)."""
    return creer_donjon(6, 8, 5, 456)

def faire_pivoter_salle(s):
    """
    Fait pivoter une salle de 90° vers la droite.
    - s : tuple (N,E,S,O) des ouvertures
    Retourne : nouvelle orientation
    """
    return (s[3], s[0], s[1], s[2])

def faire_pivoter_donjon(d, i, j):
    """
    Fait pivoter la salle (i,j) du donjon.
    - d : donjon
    - i,j : coordonnées de la salle
    """
    d[i][j] = faire_pivoter_salle(d[i][j])

def sont_salles_connectees(d, p1, p2):
    """
    Vérifie si deux salles adjacentes sont connectées par un couloir.
    - d : donjon
    - p1, p2 : positions (i,j)
    Retourne : True si connectées, False sinon
    """
    i1, j1 = p1
    i2, j2 = p2
    s1, s2 = d[i1][j1], d[i2][j2]
    if i1 == i2:  # même ligne
        return (j1 + 1 == j2 and s1[1] and s2[3]) or (j1 - 1 == j2 and s1[3] and s2[1])
    if j1 == j2:  # même colonne
        return (i1 + 1 == i2 and s1[2] and s2[0]) or (i1 - 1 == i2 and s1[0] and s2[2])
    return False

def verifier_chemin(d, c):
    """
    Vérifie si une séquence de salles forme un chemin valide.
    - d : donjon
    - c : liste de positions [(i,j), ...]
    Retourne : True si valide, False sinon
    """
    if not c:
        return False
    i = 0
    while i < len(c) - 1:
        if not sont_salles_connectees(d, c[i], c[i+1]):
            return False
        i = i + 1
    return True

def trouver_dragon(dg, p):
    """
    Cherche si un dragon est présent à la position p.
    - dg : liste des dragons
    - p : position [i,j]
    Retourne : index du dragon ou None
    """
    for i, d in enumerate(dg):
        if d[0] == p:
            return i
    return None

def deplacer_dragons(d, a, dg):
    """
    Déplace chaque dragon d'une case vers l’aventurier si possible.
    - d : donjon
    - a : aventurier [position, niveau]
    - dg : liste des dragons
    Retourne :
      - None si tout va bien
      - ["defaite", ...] si un dragon trop fort atteint l’aventurier
      
    """
    occ = [dragon[0][:] for dragon in dg]
    nl = len(d)
    nc = len(d[0]) if nl > 0 else 0
    nouveau = []

    for dragon_idx in range(len(dg)):
        pos = dg[dragon_idx][0]
        niveau = dg[dragon_idx][1]
        voisins = []
        x, y = pos[0], pos[1]
        # Cherche les voisins accessibles
        if x > 0 and sont_salles_connectees(d, [x, y], [x-1, y]):
            voisins.append([x-1, y])
        if x < nl-1 and sont_salles_connectees(d, [x, y], [x+1, y]):
            voisins.append([x+1, y])
        if y > 0 and sont_salles_connectees(d, [x, y], [x, y-1]):
            voisins.append([x, y-1])
        if y < nc-1 and sont_salles_connectees(d, [x, y], [x, y+1]):
            voisins.append([x, y+1])

        # Choisir un voisin qui rapproche du héros
        dist_act = abs(pos[0] - a[0][0]) + abs(pos[1] - a[0][1])
        candidates = []
        for v in voisins:
            if v not in occ:
                dist_v = abs(v[0] - a[0][0]) + abs(v[1] - a[0][1])
                if dist_v < dist_act:
                    candidates.append(v)

        if candidates:
            choix = candidates[random.randrange(len(candidates))]
            occ = [p for p in occ if p != pos]
            occ.append(choix)
            # Combat si le dragon atteint l’aventurier
            if tuple(choix) == tuple(a[0]):
                if niveau <= a[1]:
                    a[1] += 1  # victoire du héros
                    continue
                else:
                    return ["defaite", f"Dragon {niveau} trop fort!", a, dg, None]
            else:
                nouveau.append([choix, niveau])
        else:
            nouveau.append([pos, niveau])

    dg[:] = nouveau
    return None

def appliquer_tour_aventurier(donjon, aventurier, dragons, chemin):
    """
    Retourne [statut, message, aventurier, dragons, combat_messages]
    """
    if not chemin:
        return ["chemin_invalide", "Le chemin est vide.", aventurier, dragons, None]

    if chemin[0] != aventurier[0]:
        chemin = [aventurier[0]] + chemin

    if not verifier_chemin(donjon, chemin):
        return ["chemin_invalide", "Chemin invalide.", aventurier, dragons, None]

    combats = []
    for pos in chemin[1:]:
        aventurier[0] = list(pos)
        idx = trouver_dragon(dragons, list(pos))
        if idx is not None:
            dragon = dragons[idx]
            if dragon[1] <= aventurier[1]:
                combats.append(f"Dragon {dragon[1]} vaincu !")
                dragons.pop(idx)
                aventurier[1] += 1
            else:
                return ["defaite", f"Dragon {dragon[1]} trop fort!", aventurier, dragons, None]

        if not dragons:
            return ["victoire", "Victoire!", aventurier, dragons, combats]

    res = deplacer_dragons(donjon, aventurier, dragons)
    if res is not None:
        return res

    if not dragons:
        return ["victoire", "Victoire!", aventurier, dragons, combats]

    return ["en_cours", "Continuer.", aventurier, dragons, combats]

