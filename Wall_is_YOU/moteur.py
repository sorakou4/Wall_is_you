"""Moteur du jeu Wall Is You"""
from random import randrange as rnd, seed

def creer_donjon(nl, nc, nd, graine=None):
    """Crée un donjon avec aventurier et dragons"""
    if graine is not None:
        seed(graine)
    
    # Créer le donjon et la liste des salles (serpentin)
    donjon = [[(False, False, False, False) for _ in range(nc)] for _ in range(nl)]
    salles = [(i, j) if i % 2 == 0 else (i, nc - 1 - j) for i in range(nl) for j in range(nc)]
    
    # États valides du TEXTURE_MAP
    # Couloirs: (T, F, T, F), (F, T, F, T)
    # Coins: (T, T, F, F), (F, T, T, F), (F, F, T, T), (T, F, F, T)
    # Culs-de-sac: (T, F, F, F), (F, T, F, F), (F, F, T, F), (F, F, F, T)
    
    k = 0
    while k < len(salles) - 1:
        i1, j1 = salles[k]
        i2, j2 = salles[k + 1]
        s1, s2 = list(donjon[i1][j1]), list(donjon[i2][j2])
        
        if i1 == i2:
            if j2 > j1:
                s1[1], s2[3] = True, True
            else:
                s1[3], s2[1] = True, True
        else:
            if i2 > i1:
                s1[2], s2[0] = True, True
            else:
                s1[0], s2[2] = True, True
        
        donjon[i1][j1], donjon[i2][j2] = tuple(s1), tuple(s2)
        k = k + 1

    # Mélanger l'orientation des salles
    for i in range(nl):
        for j in range(nc):
            rotations = rnd(4)
            s = donjon[i][j]
            for _ in range(rotations):
                s = (s[3], s[0], s[1], s[2])
            donjon[i][j] = s

    aventurier = [[rnd(nl), rnd(nc)], 1]
    dragons = []
    occ = [aventurier[0][:]]
    for n in range(1, 1 + nd):
        while True:
            p = [rnd(nl), rnd(nc)]
            found = False
            for occ_p in occ:
                if occ_p == p:
                    found = True
                    break
            if not found:
                occ.append(p)
                dragons.append([p, n])
                break
    
    return donjon, aventurier, dragons

def creer_donjon_niveau1():
    """Crée un donjon de niveau 1 (3 dragons, graine 42)"""
    return creer_donjon(6, 8, 3, 42)

def creer_donjon_niveau2():
    """Crée un donjon de niveau 2 (4 dragons, graine 123)"""
    return creer_donjon(6, 8, 4, 123)

def creer_donjon_niveau3():
    """Crée un donjon de niveau 3 (5 dragons, graine 456)"""
    return creer_donjon(6, 8, 5, 456)

def faire_pivoter_salle(s):
    return (s[3], s[0], s[1], s[2])

def faire_pivoter_donjon(d, i, j):
    d[i][j] = faire_pivoter_salle(d[i][j])

def sont_salles_connectees(d, p1, p2):
    i1, j1 = p1
    i2, j2 = p2
    s1, s2 = d[i1][j1], d[i2][j2]
    if i1 == i2:
        return (j1 + 1 == j2 and s1[1] and s2[3]) or (j1 - 1 == j2 and s1[3] and s2[1])
    if j1 == j2:
        return (i1 + 1 == i2 and s1[2] and s2[0]) or (i1 - 1 == i2 and s1[0] and s2[2])
    return False

def verifier_chemin(d, c):
    if not c:
        return False
    i = 0
    while i < len(c) - 1:
        if not sont_salles_connectees(d, c[i], c[i+1]):
            return False
        i = i + 1
    return True

def trouver_dragon(dg, p):
    p = tuple(p)
    for i, d in enumerate(dg):
        if tuple(d[0]) == p:
            return i
    return None

def deplacer_dragons(d, a, dg):
    """Déplace chaque dragon d'une case si possible vers l'aventurier"""
    occ = [dragon[0][:] for dragon in dg]

    nl = len(d)
    nc = len(d[0]) if nl > 0 else 0
    nouveau = []

    for dragon_idx in range(len(dg)):
        pos = dg[dragon_idx][0]
        niveau = dg[dragon_idx][1]
        voisins = []
        x, y = pos[0], pos[1]
        if x > 0 and sont_salles_connectees(d, [x, y], [x-1, y]):
            voisins.append([x-1, y])
        if x < nl-1 and sont_salles_connectees(d, [x, y], [x+1, y]):
            voisins.append([x+1, y])
        if y > 0 and sont_salles_connectees(d, [x, y], [x, y-1]):
            voisins.append([x, y-1])
        if y < nc-1 and sont_salles_connectees(d, [x, y], [x, y+1]):
            voisins.append([x, y+1])

        dist_act = abs(pos[0] - a[0][0]) + abs(pos[1] - a[0][1])
        candidates = []
        for v in voisins:
            taken = any(occ_p == v for occ_p in occ)
            if not taken:
                dist_v = abs(v[0] - a[0][0]) + abs(v[1] - a[0][1])
                if dist_v < dist_act:
                    candidates.append(v)

        if candidates:
            choix = candidates[rnd(len(candidates))]
            occ = [p for p in occ if p != pos]
            occ.append(choix)
            if tuple(choix) == tuple(a[0]):
                if niveau <= a[1]:
                    a[1] += 1
                    continue
                else:
                    return ["defaite", "Dragon " + str(niveau) + " trop fort!", a, dg, None]
            else:
                nouveau.append([[choix[0], choix[1]], niveau])
        else:
            nouveau.append([[pos[0], pos[1]], niveau])

    dg[:] = nouveau
    return None

def appliquer_tour_aventurier(d, a, dg, c):
    """Retourne [statut, message, aventurier, dragons, combat_message]"""
    if not c:
        return ["chemin_invalide", "Le chemin est vide.", a, dg, None]
    if c[0] != a[0]:
        c = [a[0]] + c
    if not verifier_chemin(d, c):
        return ["chemin_invalide", "Chemin invalide.", a, dg, None]
    
    msg_combat = None
    pos_idx = 1
    while pos_idx < len(c):
        pos = c[pos_idx]
        a[0] = list(pos)
        idx = trouver_dragon(dg, list(pos))
        if idx is not None:
            dr = dg[idx]
            if dr[1] <= a[1]:
                msg_combat = "Dragon " + str(dr[1]) + " vaincu !"
                dg.pop(idx)
                a[1] += 1
            else:
                return ["defaite", "Dragon " + str(dr[1]) + " trop fort!", a, dg, None]
        pos_idx = pos_idx + 1
    
    if not dg:
        return ["victoire", "Victoire!", a, dg, msg_combat]
    
    # Après le déplacement de l'aventurier, déplacer les dragons d'une case
    res = deplacer_dragons(d, a, dg)
    if res is not None:
        return res

    if not dg:
        return ["victoire", "Victoire!", a, dg, msg_combat]
    return ["en_cours", "Continuer.", a, dg, msg_combat]