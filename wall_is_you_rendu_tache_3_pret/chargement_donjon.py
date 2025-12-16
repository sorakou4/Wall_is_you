# Programme de conversion des caractères box-drawing en salles de donjon, pour la tache 3 du projet.

import interface

def char_to_salle(c):
    """
    Convertit un caractère box-drawing en liste [H,D,B,G].
    Retourne une copie indépendante.
    """
    mapping = {
        '╬': [True, True, True, True],
        '╠': [True, True, True, False],
        '╣': [True, False, True, True],
        '╦': [False, True, True, True],
        '╩': [True, True, False, True],
        '╔': [False, True, True, False],
        '╗': [False, False, True, True],
        '╚': [True, True, False, False],
        '╝': [True, False, False, True],
        '═': [False, True, False, True],
        '║': [True, False, True, False],
        '╥': [True, False, False, False],
        '╨': [False, False, True, False],
        '╡': [False, True, False, False],
        '╞': [False, False, False, True],
    }
    return mapping[c]

def salle_to_char(s):
    """
    Convertit une salle [H, D, B, G] en caractère box-drawing.
    Les tuples sont obligatoires dans un dictionnaire.
    Mais prend bien en compte les listes en entrée.
    """
    mapping_inv = {
        (True, True, True, True): "╬",

        (True, True, True, False): "╠",
        (True, False, True, True): "╣",
        (False, True, True, True): "╦",
        (True, True, False, True): "╩",

        (False, True, True, False): "╔",
        (False, False, True, True): "╗",
        (True, True, False, False): "╚",
        (True, False, False, True): "╝",

        (False, True, False, True): "═",
        (True, False, True, False): "║",

        (True, False, False, False): "╥",
        (False, False, True, False): "╨",
        (False, True, False, False): "╡",
        (False, False, False, True): "╞",
    }

    return mapping_inv[tuple(s)]


def charger_donjon(fichier):
    """
    Lit un fichier .txt contenant un donjon Wall Is You.
    Retourne :
      - donjon (liste de listes de liste (H,D,B,G))
      - aventurier ([pos])
      - dragons (liste [[pos, niveau], ...])
    """
    f = open(fichier, "r", encoding="utf-8")
    lignes = []
    for ligne in f:
        lignes.append(ligne.strip())
    f.close()

    # La 2ème partie commence quand une ligne débute par A ou D ou B
    indice = 0
    while indice < len(lignes) and not (lignes[indice].startswith("A") or lignes[indice].startswith("D") or lignes[indice].startswith("B")):
        indice += 1

    grille = lignes[:indice]
    persos = lignes[indice:]

    # Construction du donjon
    donjon = []
    for ligne in grille:
        ligne_salles = [char_to_salle(c) for c in ligne]
        donjon.append(ligne_salles)

    aventurier = None
    dragons = []
    bonus = []

    for l in persos:
        t = l.split()
        if not t:
            continue
        if t[0] == "A":
            # Format attendu : A ligne colonne niv
            # Si le niveau n'est pas fourni, on met 1 par défaut
            if len(t) >= 3:
                li, co = int(t[1]), int(t[2])
                if len(t) >= 4:
                    try:
                        niv = int(t[3])
                    except ValueError:
                        niv = 1
                else:
                    niv = 1
                aventurier = [[li, co], niv]
            else:
                # Ligne malformée, on ignore
                continue

        elif t[0] == "D":
            li, co, niv = int(t[1]), int(t[2]), int(t[3])
            dragons.append([[li, co], niv])

        elif t[0] == "B":
            li, co = int(t[1]), int(t[2])
            bonus.append([li, co])

    return donjon, aventurier, dragons, bonus

def load_donjon(fichier="sauvegarde.txt"):
    """
    Charge un donjon depuis fichier et met à jour les variables
    de l'interface en place, puis rafraîchit l'affichage.
    """
    # Charger les données depuis le fichier
    donjon_charge, aventurier_charge, dragons_charge, bonus_charge = charger_donjon(fichier)

    # Mettre à jour les globals du module 'interface' (c'est ce que l'UI utilise)
    interface.donjon = donjon_charge
    interface.aventurier = aventurier_charge
    interface.dragons = dragons_charge
    interface.bonus = bonus_charge

    # Réinitialiser l'intention et adapter l'affichage
    interface.intention = []
    interface.nb_lignes = len(interface.donjon)
    interface.nb_colonnes = len(interface.donjon[0]) if interface.nb_lignes > 0 else 0
    interface.mettre_a_jour_taille_case()
    interface.rafraichir_affichage()