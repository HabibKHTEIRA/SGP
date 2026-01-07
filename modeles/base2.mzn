include "globals.mzn";

% Paramètres
int: q; % Nombre de golfeurs
int: g; % Nombre de groupes par semaine
int: p; % Taille d'un groupe
int: w; % Nombre de semaines

% Vérifications
constraint assert(q = p*g, "q doit être égal à p*g");

% --- NOUVELLE MODÉLISATION ---

% On identifie chaque "créneau" possible par un entier.
% Semaine 1 possède les groupes 1 à g
% Semaine 2 possède les groupes g+1 à 2g, etc.
int: TOTAL_SLOTS = w * g;
set of int: SLOTS = 1..TOTAL_SLOTS;

set of int: GOLFEURS = 1..q;

% Variable : Pour chaque golfeur, l'ensemble des slots (groupes) qu'il occupe
array[GOLFEURS] of var set of SLOTS: Planning_Joueur;

% 1. Chaque joueur doit jouer exactement une fois par semaine
% Cela signifie qu'il doit avoir exactement 'w' slots au total,
% et un seul slot par tranche de 'g' slots.
constraint forall(j in GOLFEURS)(
    card(Planning_Joueur[j]) = w
);

constraint forall(j in GOLFEURS, s in 0..w-1)(
    % L'intersection entre le planning du joueur et les slots de la semaine 's'
    % doit être de taille 1 (il joue dans 1 seul groupe cette semaine-là)
    card(Planning_Joueur[j] intersect (s*g + 1)..(s*g + g)) = 1
);

% 2. Taille des groupes (Contrainte inversée)
% Chaque slot (numéro de groupe) doit apparaître dans le planning de exactement 'p' joueurs.
constraint forall(k in SLOTS)(
    sum(j in GOLFEURS)(bool2int(k in Planning_Joueur[j])) = p
);

% 3. Contrainte Sociale (Le cœur du problème)
% Deux joueurs ne doivent jamais avoir plus d'un slot en commun.
% S'ils ont 2 slots en commun, ça veut dire qu'ils jouent ensemble 2 fois.
constraint forall(j1, j2 in GOLFEURS where j1 < j2)(
    card(Planning_Joueur[j1] intersect Planning_Joueur[j2]) <= 1
);

% On peut forcer le joueur 1 à prendre les premiers groupes de chaque semaine
% pour fixer "l'étalon".
constraint Planning_Joueur[1] = { k*g + 1 | k in 0..w-1 };

solve satisfy;

% --- Affichage ---
% L'affichage est un peu plus complexe car on doit reconstruire la vue "Groupe"
% --- Affichage reconstructif ---
output [
  "Semaine " ++ show(s) ++ ": " ++
  concat([
    % Pour chaque groupe de la semaine, on retrouve les joueurs qui ont ce créneau (slot)
    show({ j | j in GOLFEURS where ((s-1)*g + gr) in Planning_Joueur[j] }) ++ " "
    | gr in 1..g
  ]) ++ "\n"
  | s in 1..w
];