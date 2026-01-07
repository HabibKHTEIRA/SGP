
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

array[GOLFEURS] of var set of SLOTS: Planning_Joueur;

% 1. Chaque joueur joue une fois par semaine
constraint forall(j in GOLFEURS)(
    card(Planning_Joueur[j]) = w
);

constraint forall(j in GOLFEURS, s in 0..w-1)(
    card(Planning_Joueur[j] intersect (s*g + 1)..(s*g + g)) = 1
);

% 2. Taille des groupes
constraint forall(k in SLOTS)(
    sum(j in GOLFEURS)(bool2int(k in Planning_Joueur[j])) = p
);

% 3. Contrainte Sociale
constraint forall(j1, j2 in GOLFEURS where j1 < j2)(
    card(Planning_Joueur[j1] intersect Planning_Joueur[j2]) <= 1
);

% --- CASSAGE DE SYMÉTRIES---

% A. Fixer la Semaine 1 entièrement (Statique)
% On force les joueurs à être dans l'ordre pour la première semaine.
% Joueurs 1..p -> Groupe 1
% Joueurs p+1..2p -> Groupe 2
% etc.
% C'est la contrainte la plus importante pour la performance.
constraint forall(j in GOLFEURS)(
    (((j-1) div p) + 1) in Planning_Joueur[j]
);

% B. Fixer le planning du Joueur 1 (Statique)
% Le Joueur 1 prend toujours le 1er groupe de chaque semaine.
% Cela fixe "l'ordre des semaines" et évite de les permuter.
constraint Planning_Joueur[1] = { k*g + 1 | k in 0..w-1 };


solve satisfy;

% --- Affichage reconstructif ---
output [
  "Semaine " ++ show(s) ++ ": " ++
  concat([
    show({ j | j in GOLFEURS where ((s-1)*g + gr) in Planning_Joueur[j] }) ++ " "
    | gr in 1..g
  ]) ++ "\n"
  | s in 1..w
];