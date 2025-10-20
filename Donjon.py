#PREMIER COMPTE RENDU DE PROJET VENDREDI 21 NOVEMBRE 2025 
#— la tâche 1 (section 1.2.1) et tâche 2 (section 1.2.2);
#— au moins une variante de la liste donnée en section 2.
from random import randrange

def creer_donjon(nb_lignes, nb_colonnes,nb_dragons):
    dragons = []
    donjon = [[(True, True, False, False) for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
    for i in range(nb_dragons):
        dragon = [(randrange(nb_lignes+1),randrange(nb_colonnes+1)), i]
        dragons.append(dragon)
    return donjon, dragons

def pivot_salle(salle):
    haut, droite, bas, gauche = salle
    return (gauche, haut, droite, bas)

def pivot_donjon(donjon,i,j):
    donjon[i][j] = pivot_salle(donjon[i][j])

def salle_connectee(salle1: tuple, salle2:tuple) -> bool:
    """
    Détermine si deux salles sont connectées. True s'il existe une connexrion entre les deux salles, False sinon.
    """
    haut1, droite1, bas1, gauche1 = salle1
    haut2, droite2, bas2, gauche2 = salle2
    
    if bas1 and haut2:
        return True
    if droite1 and gauche2:
        return True
    if haut1 and bas2:
        return True
    if gauche1 and droite2:
        return True
    return False

def personnages(donjon):
    aventurier = [(0, 0),1]
    dragon = [(0,0),3]
    dragons = []
    
def etat_jeu(donjon, personnages):
    pass