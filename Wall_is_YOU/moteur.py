"""
Moteur du jeu "Wall Is You" (module supplémentaire)

Ce fichier complète le code existant sans le modifier. Il fournit :
- des utilitaires pour trouver un dragon à une position,
- l'application du tour de l'aventurier le long d'un chemin donné
  (vérification du chemin, résolutions des combats, mise à jour des niveaux),
- une petite démonstration exécutable pour tester rapidement le moteur.

Il importe les fonctions utilitaires déjà présentes dans
`Donjon_version_corrigee.py` (création du donjon, pivot, vérification de
chemin, affichage de debug).
"""

from typing import List, Optional, Tuple, Dict, Any
import Donjon_version_corrigee as base

Position = Tuple[int, int]
Personnage = List[Any]  # [position, niveau]


def trouver_dragon_en_position(dragons: List[Personnage], pos: Position) -> Optional[int]:
    """Retourne l'indice du dragon dans la liste `dragons` situé en `pos`,
    ou None si aucun dragon n'est présent.
    """
    for idx, d in enumerate(dragons):
        if d[0] == pos:
            return idx
    return None


def partie_gagnee(dragons: List[Personnage]) -> bool:
    """Renvoie True si la liste de dragons est vide (tous tués)."""
    return len(dragons) == 0


def appliquer_tour_aventurier(donjon: List[List[Tuple[bool, bool, bool, bool]]],
                             aventurier: Personnage,
                             dragons: List[Personnage],
                             chemin: List[Position]) -> Dict[str, Any]:
    """
    Applique le tour de l'aventurier suivant le `chemin` fourni.
    Comportement :
    - Vérifie que le chemin est valide (salles connectées) à l'aide
      de `base.verifier_chemin`.
    - Parcourt le chemin étape par étape ; à l'arrivée dans une salle,
      si un dragon s'y trouve :
        * si niveau(dragon) <= niveau(aventurier) -> le dragon meurt
          et l'aventurier gagne 1 niveau;
        * sinon -> l'aventurier meurt et la partie est perdue.
    - Retourne un dictionnaire décrivant le résultat et l'état mis à jour.
    """
    if not chemin:
        return {
            "status": "invalid_path",
            "message": "Chemin vide fourni.",
            "aventurier": aventurier,
            "dragons": dragons,
        }

   
    if chemin[0] != aventurier[0]:
        chemin = [aventurier[0]] + chemin

    if not base.verifier_chemin(donjon, chemin):
        return {
            "status": "invalid_path",
            "message": "Le chemin n'est pas valide (salles non connectées).",
            "aventurier": aventurier,
            "dragons": dragons,
        }

    for pos in chemin[1:]:
        aventurier[0] = pos
        idx = trouver_dragon_en_position(dragons, pos)
        if idx is not None:
            dragon = dragons[idx]
            if dragon[1] <= aventurier[1]:
                # Aventurier tue le dragon
                del dragons[idx]
                aventurier[1] += 1
            else:
                # Aventurier meurt : partie perdue
                return {
                    "status": "lose",
                    "message": f"L'aventurier a été tué par un dragon de niveau {dragon[1]} en {pos}.",
                    "aventurier": aventurier,
                    "dragons": dragons,
                }

    if partie_gagnee(dragons):
        return {
            "status": "win",
            "message": "Tous les dragons ont été tués. Victoire !",
            "aventurier": aventurier,
            "dragons": dragons,
        }

    return {
        "status": "ongoing",
        "message": "Tour de l'aventurier terminé.",
        "aventurier": aventurier,
        "dragons": dragons,
    }


def chemin_ligne_droite(dep: Position, arr: Position) -> List[Position]:
    """
    Construit un chemin simple (lignes puis colonnes) entre deux positions.
    Utile pour les démonstrations lorsque le donjon est totalement connecté.
    Ne vérifie pas la connectivité des salles (il faut appeler `verifier_chemin`).
    """
    path = [dep]
    (i0, j0), (i1, j1) = dep, arr
    step = 1 if i1 >= i0 else -1
    for i in range(i0 + step, i1 + step, step):
        path.append((i, j0))
    step = 1 if j1 >= j0 else -1
    for j in range(j0 + step, j1 + step, step):
        path.append((i1, j))
    return path


def demo() -> None:
    """
    Petit démonstrateur exécutable en ligne de commande.
    - crée un petit donjon (complètement connecté par défaut dans
      `Donjon_version_corrigee.creer_donjon`),
    - affiche l'état,
    - construit un chemin simple vers le premier dragon et applique le tour.
    """
    donjon, aventurier, dragons = base.creer_donjon(3, 3, 3)
    print("Donjon créé pour la démo :")
    base.afficher_etat(donjon, aventurier, dragons)

    if not dragons:
        print("Aucun dragon — partie triviale.")
        return

    cible = dragons[0][0]
    chemin = chemin_ligne_droite(aventurier[0], cible)
    print("Chemin proposé :", chemin)
    res = appliquer_tour_aventurier(donjon, aventurier, dragons, chemin)
    print("Résultat :", res["status"], "-", res["message"])
    base.afficher_etat(donjon, aventurier, dragons)


if __name__ == "__main__":
    demo()
