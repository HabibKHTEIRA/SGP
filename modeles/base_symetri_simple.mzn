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








solve satisfy;

output [
  "Semaine " ++ show(s) ++ ": "
  ++ concat([ show(Groupes[s,gr]) ++ " " | gr in GROUPES ])
  ++ "\n"
  | s in SEMAINES
];


