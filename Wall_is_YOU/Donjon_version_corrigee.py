# Projet Wall Is You - Tâche 1
# Moteur de jeu (logique interne)
# Auteur : Lohan, Daniel
# Date : 21 novembre 2025

from random import randrange

def creer_donjon(nb_lignes, nb_colonnes, nb_dragons):
    """
    Crée un donjon avec des salles initialisées et des dragons placés aléatoirement.
    Chaque salle n'a que deux passages ouverts, les autres murs sont fermés.
    Retourne (donjon, aventurier, dragons)
    """
    # Création du donjon : chaque salle = (haut, droite, bas, gauche)
    # On initialise tout fermé, puis on créera une (ou plusieurs)
    # cycles qui ouvrent exactement deux passages par salle.
    donjon = [[(False, False, False, False) for _ in range(nb_colonnes)] for _ in range(nb_lignes)]

    # Nous allons construire un graphe 2-régulier (chaque case a degré 2)
    # en ajoutant des arêtes entre cases voisines de manière aléatoire.
    # Algorithme : tentative gloutonne aléatoire avec restart si on bloque.
    import random

    def neighbors(i, j):
        res = []
        if i > 0:
            res.append((i - 1, j))
        if i < nb_lignes - 1:
            res.append((i + 1, j))
        if j > 0:
            res.append((i, j - 1))
        if j < nb_colonnes - 1:
            res.append((i, j + 1))
        return res

    max_attempts = 200
    attempt = 0
    success = False
    edges = set()
    cells_all = [(i, j) for i in range(nb_lignes) for j in range(nb_colonnes)]
    while attempt < max_attempts and not success:
        attempt += 1
        # reset
        donjon = [[(False, False, False, False) for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
        edges = set()
        deg = {(i, j): 0 for i in range(nb_lignes) for j in range(nb_colonnes)}

        # create stubs (each cell appears twice)
        stubs = []
        for c in cells_all:
            stubs.append(c)
            stubs.append(c)
        random.shuffle(stubs)

        failed = False
        while stubs:
            u = stubs.pop()  # take last stub
            # find a partner in stubs that is a neighbor and valid
            found = False
            for idx in range(len(stubs)-1, -1, -1):
                v = stubs[idx]
                if v == u:
                    continue
                if deg[v] >= 2 or deg[u] >= 2:
                    continue
                # must be neighbors
                if v in neighbors(*u):
                    # also avoid duplicating edge
                    if (u, v) in edges or (v, u) in edges:
                        continue
                    # pair them
                    edges.add((u, v))
                    deg[u] += 1
                    deg[v] += 1
                    stubs.pop(idx)
                    found = True
                    break
            if not found:
                failed = True
                break
        if not failed:
            # ensure all degrees are exactly 2
            if all(deg[c] == 2 for c in cells_all):
                success = True
                break
            else:
                # try again
                continue

    # Apply edges to donjon representation
    for (u, v) in edges:
        i1, j1 = u
        i2, j2 = v
        haut1, droite1, bas1, gauche1 = donjon[i1][j1]
        haut2, droite2, bas2, gauche2 = donjon[i2][j2]
        if i1 == i2 and j1 + 1 == j2:
            droite1 = True
            gauche2 = True
        elif i1 == i2 and j1 - 1 == j2:
            gauche1 = True
            droite2 = True
        elif j1 == j2 and i1 + 1 == i2:
            bas1 = True
            haut2 = True
        elif j1 == j2 and i1 - 1 == i2:
            haut1 = True
            bas2 = True
        donjon[i1][j1] = (haut1, droite1, bas1, gauche1)
        donjon[i2][j2] = (haut2, droite2, bas2, gauche2)

    # If generation failed after many attempts, fall back to snake cycle (deterministic)
    if not success:
        cells = []
        for i in range(nb_lignes):
            row = list(range(nb_colonnes))
            if i % 2 == 1:
                row = list(reversed(row))
            for j in row:
                cells.append((i, j))
        def open_between(a, b):
            (i1, j1) = a
            (i2, j2) = b
            haut1, droite1, bas1, gauche1 = donjon[i1][j1]
            haut2, droite2, bas2, gauche2 = donjon[i2][j2]
            if i1 == i2 and j1 + 1 == j2:
                droite1 = True
                gauche2 = True
            elif i1 == i2 and j1 - 1 == j2:
                gauche1 = True
                droite2 = True
            elif j1 == j2 and i1 + 1 == i2:
                bas1 = True
                haut2 = True
            elif j1 == j2 and i1 - 1 == i2:
                haut1 = True
                bas2 = True
            donjon[i1][j1] = (haut1, droite1, bas1, gauche1)
            donjon[i2][j2] = (haut2, droite2, bas2, gauche2)
        N = len(cells)
        for k in range(N):
            a = cells[k]
            b = cells[(k + 1) % N]
            open_between(a, b)

    # Création de l'aventurier (niveau 1, position aléatoire)
    aventurier = [(randrange(nb_lignes), randrange(nb_colonnes)), 1]

    # Création des dragons
    dragons = []
    niveaux = list(range(2, 2 + nb_dragons))
    for niveau in niveaux:
        position = (randrange(nb_lignes), randrange(nb_colonnes))
        dragon = [position, niveau]
        dragons.append(dragon)

    return donjon, aventurier, dragons


def pivot_salle(salle):
    """
    Fait pivoter une salle de 90° vers la droite.
    Les deux passages ouverts tournent avec la salle.
    """
    haut, droite, bas, gauche = salle
    return (gauche, haut, droite, bas)


def pivot_donjon(donjon, i, j):
    """
    Pivote la salle en (i, j)
    Fonctrionne de paire avec la fonction pivot_salle.
    """
    donjon[i][j] = pivot_salle(donjon[i][j])


def sont_connectees(donjon, pos1, pos2):
    """
    Retourne True si les salles pos1 et pos2 sont adjacentes ET ouvertes dans les bonnes directions.
    False sinon.
    """
    i1, j1 = pos1
    i2, j2 = pos2

    salle1 = donjon[i1][j1]
    salle2 = donjon[i2][j2]

    # même ligne
    if i1 == i2:
        if j1 + 1 == j2:   # salle2 est à droite
            return salle1[1] and salle2[3]
        elif j1 - 1 == j2: # salle2 est à gauche
            return salle1[3] and salle2[1]

    # même colonne
    if j1 == j2:
        if i1 + 1 == i2:   # salle2 est en dessous
            return salle1[2] and salle2[0]
        elif i1 - 1 == i2: # salle2 est au-dessus
            return salle1[0] and salle2[2]

    return False


def deplacer_aventurier(aventurier, chemin, donjon):
    """
    Déplace l'aventurier si le chemin est valide.
    """
    if verifier_chemin(donjon, chemin):
        aventurier[0] = chemin[-1]
        print("L'aventurier arrive en", aventurier[0])
    else:
        print("Chemin invalide.")


def verifier_chemin(donjon, chemin):
    """
    Vérifie que le chemin est formé de salles connectées.
    """
    for i in range(len(chemin) - 1):
        if not sont_connectees(donjon, chemin[i], chemin[i + 1]):
            return False
    return True


def afficher_etat(donjon, aventurier, dragons):
    """
    Affiche un résumé textuel du jeu (pour debug sans interface graphique).
    """
    print("=== État du jeu ===")
    print("Aventurier : position", aventurier[0], "niveau", aventurier[1])
    print("Dragons :")
    for d in dragons:
        print(" - Dragon niv", d[1], "en", d[0])
    print("===================")