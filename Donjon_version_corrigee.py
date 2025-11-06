# Projet Wall Is You - Tâche 1
# Moteur de jeu (logique interne)
# Auteur : Lohan, Daniel
# Date : 21 novembre 2025

from random import randrange

def creer_donjon(nb_lignes, nb_colonnes, nb_dragons):
    """
    Crée un donjon avec des salles initialisées et des dragons placés aléatoirement.
    Retourne (donjon, aventurier, dragons)
    """
    # Création du donjon : chaque salle = (haut, droite, bas, gauche)
    donjon = [[(True, True, True, True) for _ in range(nb_colonnes)] for _ in range(nb_lignes)]

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
    Fonctionne de paire avec la fonction pivot_donjon.
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
