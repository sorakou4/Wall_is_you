Par TRICOIRE Lohan et PREASCA Daniel

---Présentation générale---

"Wall Is You" est un jeu de labyrinthe en Python (Version 3.11.9) dans lequel un aventurier se déplace dans un donjon composé de salles orientées.
Chaque salle possède des ouvertures (N, E, S, O).
En cliquant (clic gauche), le joueur pivote une salle.
En cliquant (clic droit), il dessine un chemin que l'aventurier parcourra.
L’aventurier combat les dragons rencontrés :

Il gagne un niveau si le dragon est d’un niveau ≤ au sien

Il meurt si le dragon est trop puissant

Après chaque tour, les dragons se déplacent vers l’aventurier si possible.

---Structure des fichiers---

moteur.py  : logique du jeu (donjon, déplacements, combat)

interface.py  : affichage FLTK, gestion clics, intention et animation

menu.py  : menu principal et choix du niveau

chargement_donjon.py : permet la gestion des sauvegrades, des chargements de donjons etc.

---Variables globales importantes (interface.py)---

nb_lignes, nb_colonnes --> Dimensions du donjon

nb_dragons --> Nombre de dragons pour la partie

graine_donjon --> Graine aléatoire (permet donjons reproductibles)

largeur_fenetre, hauteur_fenetre --> Taille fenêtre FLTK

taille_case --> Taille d’une salle en pixels

grille_x0, grille_y0 --> Décalage de la grille dans la fenêtre

donjon --> Grille contenant les salles et leur orientation

aventurier --> Position + niveau de l’aventurier

dragons --> Liste des dragons (position + niveau)

intention --> Liste de cases formant le chemin que l’aventurier va suivre

---Fonctionnement du jeu---

Le donjon est généré sous forme d’un chemin serpentin auquel on applique des rotations aléatoires.

L’aventurier commence niveau 1.

Les dragons sont placés aléatoirement, chacun avec un niveau unique.

Le joueur peut :

Pivoter une salle (clic gauche)

Placer un trésor (clic droit)

Valider le chemin (espace)

Avoir un indice (i)

Sauvegarder la partie (S)

Charger la partie Sauvegarder (L)

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

Dragon ≤ aventurier --> dragon tué

Dragon > aventurier --> défaite

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

Si défaite immédiate --> fin

Anime le déplacement de l’aventurier

Déplace les dragons

Vérifie victoire ou défaite

-programme_principal()-

Boucle événementielle FLTK :

Clic gauche

Déplacements souris

Clic droit ou Espace

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

Le joueur construit un chemin

--> Clics droits successifs

Il valide (espace)

Le moteur :

Vérifie la validité du chemin

Déplace l’aventurier

Traite les combats

Déplace les dragons

L’interface anime tout

Sauf en cas de défaite immédiate, où l'animation n’a pas lieu.

---Conditions de victoire et défaite---

-Victoire-

--> Tous les dragons sont morts.

-Défaite-

--> L’aventurier entre dans une salle où un dragon > à son niveau
--> OU un dragon atteint l’aventurier pendant son déplacement

---Nouveautés et ajustements---

-Ajout de la gestion des bonus (+1 niveau) dans le moteur et l’interface.

-Sauvegarde et chargement de donjons au format texte (box-drawing).

-Séparation claire du chargement de donjon dans un module dédié.

-Affichage du niveau de l’aventurier en bas de l’écran.

-Gestion améliorée des erreurs d’affichage (salles en rose, jaune, gris selon l’état).

-Correction des problèmes de conversion entre tuples et listes pour la gestion des entités.

---Choix technique---

Nous avons fait le choix d'afficher le niveau de l'aventurier en bas de l'écran pour une meilleure visibilité.

Nous avons également fait le choix de créer un fichier wall_is_you.py qui correspond au jeu, pour une compréhension plus simple du fichier à exécuter pour lancer le jeu.

Le sujet ne précisait pas de créer plusieurs niveaux de difficulté pour les donjons mais nous avons trouvé pertinent le fait d'ajuster la difficulté en fonction du donjon choisi en ajoutant des dragons.

---Difficulté rencontrée---

Nous avons rencontré des difficultés, principalement à cause des textures. Nous nous sommes trompés lors de la création initiale des salles des donjons, et aucune salle n'était reconnue et donc cela ne fonctionnait pas. Pour mieux comprendre, on a décidé d'afficher en rose les salles où la texture ne s'affichait pas mais qui existaient et qui étaient reconnues par le jeu, en jaune les salles qui n'ont aucun passage qui permet le déplacement et en gris les salles qui n'étaient pas du tout reconnues par le jeu. Cela a facilité l'analyse des problèmes.

Des problèmes entre tuples et listes ont été rencontrés également, ce qui provoquait un bug du jeu qui ne tuait pas les dragons ou l'aventurier au moment où il le fallait.

---Nouveautés supplémentaires implémentées---

-Ajout de la gestion des trésors dans le moteur et l’interface (liste de positions, et non plus un seul trésor).

-Possibilité pour le joueur de placer manuellement jusqu’à 4 trésors différents via le clic droit dans le donjon.

-Affichage graphique des trésors dans le donjon avec une texture dédiée.

-Priorité donnée aux trésors dans le calcul de l’intention automatique : si un trésor est accessible, le chemin calculé vise d’abord ce trésor.

-Priorité donnée aux trésors aussi dans la fonction d’indice (bfs_reel) sur le donjon de référence : l’indice cherche le trésor le plus proche avant de proposer un chemin vers un dragon.

-Ajout d’un compteur de trésors restants dans le panneau de droite, accompagné de l’icône du trésor pour une meilleure lisibilité.

-Intégration d’un retour automatique au menu principal : en cas de victoire ou de défaite, la fenêtre FLTK se ferme et le programme wall_is_you.py (menu) est relancé.

-Ajustement de l’animation de l’aventurier pour qu’elle suive le chemin calculé case par case, avec une temporisation adaptée.

---Fonctions supplémentaires – moteur.py---

-placer_tresor(donjon, pos, aventurier, dragons)-

Place un trésor dans une salle :

Vérifie que la salle n’est pas occupée par l’aventurier ou un dragon

Vérifie qu’il n’y a pas déjà un trésor à cet endroit

Limite le nombre total de trésors à 4

Stocke les trésors dans une liste globale tresor

Retourne True si le trésor est placé, False sinon

-intention(donjon, position_aventurier, dragons)-

Calcule un chemin automatique avec priorité aux trésors :

Si un trésor est accessible, un BFS cherche d’abord un chemin jusqu’à ce trésor

Si aucun trésor n’est accessible, le comportement d’origine est conservé :

--> on cherche un chemin vers les dragons, puis on choisit le dragon de plus haut niveau, avec chemin le plus court en cas d’égalité

-indice(donjon_reference, aventurier, dragons)-

Calcule un chemin dans le donjon de référence (non modifié par les rotations) :

Si des trésors existent, on cherche le trésor le plus proche en termes de distance BFS

Sinon, on cherche un chemin vers le dragon le plus faible

Retourne une liste de positions représentant le chemin conseillé

---Fonctions supplémentaires – interface.py---

-afficher_commandes()-

En plus des commandes initiales, affiche désormais :

Un texte "Trésors restants :" dans le panneau de droite

Une icône de trésor à côté du texte

Le nombre de trésors encore disponibles (variable globale compteur_tresors)

-rafraichir_affichage()-

Affiche maintenant :

Les trésors posés dans le donjon, à partir de la liste moteur.tresor

Le chemin d’intention automatique (en rouge), calculé par moteur.intention

Le chemin d’indice (en cyan), calculé par moteur.indice sur une copie de référence du donjon

-intention automatique dans l’affichage-

L’intention n’est plus construite à la main avec le clic droit :

Le clic droit sert à placer des trésors

Le chemin d’intention est calculé automatiquement par le moteur, en fonction des trésors et des dragons

-appliquer_intention()-

Gère maintenant :

La collecte de trésor : si le statut renvoyé est "tresor", un message de richesse est affiché et le compteur de trésors (compteur_tresors) est décrémenté sans passer en négatif

Les défaites : affichage du message, petite pause, puis retour au menu via retour_menu()

Les victoires : affichage du message "Victoire !", petite pause, puis retour au menu via retour_menu()

-retour_menu()-

Ferme la fenêtre FLTK actuelle (fltk.ferme_fenetre())

Relance le programme principal wall_is_you.py via os.system("python wall_is_you.py")

Permet de revenir proprement au menu après une partie (victoire ou défaite)

---Choix techniques supplémentaires---

-Nous avons choisi de représenter les trésors par une liste de positions dans le moteur, pour pouvoir en gérer plusieurs et les supprimer individuellement lorsqu’ils sont ramassés.

-Nous avons ajouté un compteur de trésors côté interface, indépendant de la structure interne, pour afficher simplement combien de trésors peuvent encore être posés, sans exposer la structure de données du moteur à l’utilisateur.

-L’intention automatique et l’indice s’appuient sur des parcours en largeur (BFS), ce qui garantit des chemins les plus courts possibles dans le graphe des salles connectées.

-Le retour au menu utilise uniquement des modules standards (os) et FLTK, respectant ainsi les contraintes du sujet (pas de modules externes, pas de notions avancées comme les classes).

---Difficultés supplémentaires rencontrées---

-La gestion de plusieurs trésors a demandé une refonte de la variable tresor : initialement pensée comme une seule position, elle a été transformée en liste de positions, ce qui a nécessité des corrections dans appliquer_tour_aventurier, indice, intention et l’affichage.

-L’intégration du compteur de trésors a provoqué des incohérences au début (valeurs négatives, désynchronisation entre ce qui est affiché et ce qui existe réellement dans le moteur), ce qui nous a obligés à bien séparer :
--> la logique de placement/ramassage côté moteur
--> la gestion d’un nombre maximum de placements côté interface.
