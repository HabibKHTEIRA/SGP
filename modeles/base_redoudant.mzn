include "globals.mzn";


int: q;
int: g;
int: p;
int: w;

set of int: GOLFEURS = 1..q;
set of int: SEMAINES = 1..w;
set of int: GROUPES  = 1..g;




array[SEMAINES, GROUPES] of var set of GOLFEURS: Groupes;

constraint assert(q = p*g, "q doit être égal à p*g");
constraint assert(
  w*g*p*(p-1) div 2 <= q*(q-1) div 2,
  "Nombre maximum de rencontres dépassé"
);

% Taille des groupes
constraint forall(s in SEMAINES, gr in GROUPES)(
  card(Groupes[s,gr]) = p
);

% Un golfeur dans un seul groupe par semaine
constraint forall(s in SEMAINES)(
  all_disjoint([ Groupes[s,gr] | gr in GROUPES ])
);

% Deux golfeurs ne jouent pas ensemble plus d'une fois
constraint forall(s1, s2 in SEMAINES where s1 < s2)(
  forall(g1, g2 in GROUPES)(
    card(Groupes[s1,g1] intersect Groupes[s2,g2]) <= 1
  )
);


% symetri breaking

% symetrie des golfeurs et groupes
% fixer la premiere ssemaine (1..p, p+1..2p, etc)
constraint forall(j in GROUPES)(
    Groupes[1,j] = {k | k in ((j-1)*p+1)..(j*p) }
);

% symétrie des groupes
% pour les semaines suivantes, on impose un ordre lexico sur les groupes
constraint forall(i in 2..w)(
    forall(j in 1..g-1)(
        Groupes[i, j] < Groupes[i, j+1]  % comparaison lexico des ensembles
    )
);

% symétrie des semaines
% on ordonne les semaines à partir de la même 2éme selon le contenu du prémiere groupe
constraint forall(i in 2..w-1)(
    Groupes[i, 1] < Groupes[i+1, 1]
);

% Contraintes redondantes
% Matrice auxiliaire pour suivre les rencontres entre joueurs
array[GOLFEURS, GOLFEURS] of var 0..1: Rencontres;

% Channeling : Si i et j sont dans le meme groupe, alors Rencontres[i,j] = 1
constraint forall(i, j in GOLFEURS where i < j)(
    Rencontres[i,j] = bool2int(
        exists(s in SEMAINES, gr in GROUPES)(
            {i, j} subset Groupes[s,gr]
        )
    )
);

% Symétrie de la matrice
constraint forall(i, j in GOLFEURS where i > j)(
   Rencontres[i,j] = Rencontres[j,i]
);
constraint forall(i in GOLFEURS)(Rencontres[i,i] = 0);

% Chaque joueur doit rencontrer exactement w * (p-1) adversaires distincts
constraint forall(i in GOLFEURS)(
    sum(j in GOLFEURS)(Rencontres[i,j]) = w * (p - 1)
);




solve satisfy;

output [
  "Semaine " ++ show(s) ++ ": "
  ++ concat([ show(Groupes[s,gr]) ++ " " | gr in GROUPES ])
  ++ "\n"
  | s in SEMAINES
];