include "globals.mzn";

% Paramètres
int: q; % Nombre de golfeurs
int: g; % Nombre de groupes par semaine
int: p; % Taille d'un groupe
int: w; % Nombre de semaines

% Vérifications
constraint assert(q = p*g, "q doit être égal à p*g");

% --- MODÉLISATION JOUEURS ---

int: TOTAL_SLOTS = w * g;
set of int: SLOTS = 1..TOTAL_SLOTS;
set of int: GOLFEURS = 1..q;

% Variable : Pour chaque golfeur, l'ensemble des slots (groupes) qu'il occupe
array[GOLFEURS] of var set of SLOTS: Planning_Joueur;

% 1. Chaque joueur doit jouer exactement une fois par semaine
constraint forall(j in GOLFEURS)(
    card(Planning_Joueur[j]) = w
);

constraint forall(j in GOLFEURS, s in 0..w-1)(
    card(Planning_Joueur[j] intersect (s*g + 1)..(s*g + g)) = 1
);

% 2. Taille des groupes
% Chaque slot (numéro de groupe) doit apparaître dans le planning de exactement 'p' joueurs.
constraint forall(k in SLOTS)(
    sum(j in GOLFEURS)(bool2int(k in Planning_Joueur[j])) = p
);

% 3. Contrainte Sociale (Base)
% Deux joueurs ne doivent jamais avoir plus d'un slot en commun.
constraint forall(j1, j2 in GOLFEURS where j1 < j2)(
    card(Planning_Joueur[j1] intersect Planning_Joueur[j2]) <= 1
);

% --- CASSAGE DE SYMÉTRIES---

% A. Fixer la Semaine 1 entièrement
constraint forall(j in GOLFEURS)(
    (((j-1) div p) + 1) in Planning_Joueur[j]
);

% B. Fixer le planning du Joueur 1
constraint Planning_Joueur[1] = { k*g + 1 | k in 0..w-1 };

% --- CONTRAINTES REDONDANTES ---

% R1. Vérification globale des rencontres
% Au lieu de vérifier juste "pas plus de 1 rencontre", on vérifie aussi
% "est-ce que j'ai rencontré tout le monde que je devais ?"
% La somme des intersections (0 ou 1) avec tous les autres joueurs doit être égale au nombre total d'adversaires requis.
constraint forall(j1 in GOLFEURS)(
    sum(j2 in GOLFEURS where j1 != j2)(
        card(Planning_Joueur[j1] intersect Planning_Joueur[j2])
    ) = w * (p - 1)
);

solve satisfy;

% --- Affichage ---
output [
  "Semaine " ++ show(s) ++ ": " ++
  concat([
    show({ j | j in GOLFEURS where ((s-1)*g + gr) in Planning_Joueur[j] }) ++ " "
    | gr in 1..g
  ]) ++ "\n"
  | s in 1..w
];