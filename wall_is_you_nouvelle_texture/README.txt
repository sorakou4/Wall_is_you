---Présentation générale---

"Wall Is You" est un jeu de labyrinthe dans lequel un aventurier se déplace dans un donjon composé de salles orientées.
Chaque salle possède des ouvertures (N, E, S, O).
En cliquant, le joueur pivote une salle.
En maintenant la touche i, il dessine un chemin que l'aventurier parcourra.
L’aventurier combat les dragons rencontrés :

Il gagne un niveau si le dragon est d’un niveau ≤ au sien

Il meurt si le dragon est trop puissant

Après chaque tour, les dragons se déplacent vers l’aventurier si possible.

---Structure des fichiers---

moteur.py : logique du jeu (donjon, déplacements, combat)

interface.py : affichage FLTK, gestion clics, intention et animation

menu.py : menu principal et choix du niveau

---Variables globales importantes (interface.py)---

nb_lignes, nb_colonnes → Dimensions du donjon

nb_dragons → Nombre de dragons pour la partie

graine_donjon → Graine aléatoire (permet donjons reproductibles)

largeur_fenetre, hauteur_fenetre → Taille fenêtre FLTK

taille_case → Taille d’une salle en pixels

grille_x0, grille_y0 → Décalage de la grille dans la fenêtre

donjon → Grille contenant les salles et leur orientation

aventurier → Position + niveau de l’aventurier

dragons → Liste des dragons (position + niveau)

intention →	Liste de cases formant le chemin que l’aventurier va suivre

---Fonctionnement du jeu---

Le donjon est généré sous forme d’un chemin serpentin auquel on applique des rotations aléatoires.

L’aventurier commence niveau 1.

Les dragons sont placés aléatoirement, chacun avec un niveau unique.

Le joueur peut :

Pivoter une salle (clic gauche)

Construire un chemin (clic droit)

Valider le chemin (espace)

Le moteur :

Vérifie si le chemin est valide

Déplace l’aventurier le long du chemin

Déclenche les combats

Déplace les dragons

---Fonctions importantes – moteur.py---

-creer_donjon(nl, nc, nd, graine)-

Crée un donjon :

Génère un chemin serpentin

Ouvre les salles adjacentes

Mélange les orientations

Place l’aventurier

Place les dragons

Retourne : (donjon, aventurier, dragons)

-faire_pivoter_salle(s)-

Fait tourner une salle de 90° :
(N, E, S, O) devient (O, N, E, S).

-faire_pivoter_donjon(d, i, j)-

Applique faire_pivoter_salle à la salle (i, j) du donjon.

-sont_salles_connectees(d, p1, p2)-

Renvoie True si p1 et p2 sont adjacentes ET reliées par des ouvertures.
Permet de vérifier si un déplacement est possible.

-verifier_chemin(d, c)-

Renvoie True si toutes les étapes du chemin c sont connectées.

-trouver_dragon(dg, p)-

Renvoie l’indice du dragon situé sur p, sinon None.

-appliquer_tour_aventurier(d, a, dg, c)-

Cœur du moteur.
Exécute un TOUR COMPLET :

Vérifie que le chemin est valide

Déplace l’aventurier sur chaque case

Vérifie les combats :

Aventurier niveau ≥ dragon : dragon tué, aventurier +1 niveau

Sinon : défaite immédiate

Si tous les dragons meurent : victoire

Déplace tous les dragons d’une case

Retourne un statut :

"chemin_invalide"

"defaite"

"victoire"

"en_cours"

-deplacer_dragons(d, a, dg)-

Déplace chaque dragon si le mouvement le rapproche de l’aventurier.
Si un dragon atteint l’aventurier :

Dragon ≤ aventurier → dragon tué

Dragon > aventurier → défaite

---Fonctions importantes – interface.py---

-rafraichir_affichage()-

Redessine toute la fenêtre :

Donjon

Aventurier

Dragons

Intention

Commandes

C’est l’afficheur principal.

-pivoter_case(case)-

Appelle le moteur pour pivoter une salle + rafraîchit l’écran.

-ajouter_a_intention(case)-

Ajoute une case au chemin dessiné par le joueur.

-effacer_intention()-

Supprime le chemin dessiné.

-appliquer_intention()-

Déroulement :

Prépare le chemin

Appelle appliquer_tour_aventurier

Si défaite immédiate → fin

Anime le déplacement de l’aventurier

Déplace les dragons

Vérifie victoire ou défaite

-programme_principal()-

Boucle événementielle FLTK :

Clics

Déplacements souris

Touche 'i' ou espace

Redimensionnements

Quitter

---Fonctions importantes – menu.py---

-dessiner_menu()-

Affiche le menu principal, les boutons, et les sous-boutons (difficulté).

-programme_menu()-

Boucle du menu :

Clic sur "Charger un donjon"

Choix du niveau

Lancement du jeu (interface.programme_principal())

---Déroulement d’un tour---

1. Le joueur construit un chemin

→ clics droit successifs

2. Il valide (espace)
3. Le moteur :

Vérifie la validité du chemin

Déplace l’aventurier

Traite les combats

Déplace les dragons

4. L’interface anime tout

Sauf en cas de défaite immédiate, où l'animation n’a pas lieu.

---Conditions de victoire et défaite---

-Victoire-

→ Tous les dragons sont morts.

-Défaite-

→ L’aventurier entre dans une salle où un dragon > à son niveau
→ OU un dragon atteint l’aventurier pendant son déplacement

_______________________________________________________________

---Choix technique---

Nous avons fait le choix d'afficher le niveau de l'aventurier en bas de l'écran pour une meilleure visibilité

Nous avons également fait le choix de créer un fichier wall_is_you.py qui correspond au jeu, pour une compréhension plus simple du fichier à exécuter pour lancer le jeu

Le sujet ne précisait pas de créer plusieurs niveaux de difficulté pour les donjons mais nous avons trouver pertinent le fait d'ajuster la difficulté en fonction du donjon choisi en ajoutant des dragons.

---Difficulté rencontrée---

Nous avons rencontré des difficultés, principalement à cause des textures. Nous nous sommes trompés lors de la création initial des salles des donjons, et aucune salle n'était reconnue et donc cela ne fonctionnait pas. Pour mieux comprendre, on a décidé d'afficher en rose les salles où la texture ne s'affichait pas mais qui existaient et qui étaient reconnues pas le jeu, en jaune les salles qui n'ont aucun passage qui permet le déplacement et en gris les salles qui n'étaient pas du tout reconnues pas le jeu. Cela a facilité l'analyse des problèmes.

Des problèmes entre tuples et listes ont été rencontré également, ce qui provoquait un bug du jeu qui ne tuait pas les dragons ou l'aventurier au moment où il le fallait.

