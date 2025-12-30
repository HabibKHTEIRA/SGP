include "globals.mzn";

%parametres
int: q;
int: g;
int: p;
int: w;

set of int: GOLFEURS = 1..q;
set of int: SEMAINES = 1..w;
set of int: GROUPES = 1..g;

constraint assert(q = p*g, "q doit etre êgal à p*g");
constraint assert(w*g*p*(p-1) div 2 <= q*(q-1) div 2, "Nombre maximum des groupes possible");

%varaibles
array [SEMAINES, GROUPES] of var set of GOLFEURS: Groupes;

%contraintes

% taille des groupes
constraint forall(i in SEMAINES, j in GROUPES)(
    card(Groupes[i,j]) = p
);

% un golfeur ne peut pas jouer dans plusieurs groupes dans la même semaine
constraint forall(i in SEMAINES)(
    all_disjoint([Groupes[i,j] | j in GROUPES])
);


% deux golfeurs ne jouent pas ensemble plus d'une fois
constraint forall(s1, s2 in SEMAINES where s1 < s2)(
    forall(g1, g2 in GROUPES)(
        card(Groupes[s1, g1] intersect Groupes[s2, g2]) <= 1
    )  
);

solve satisfy;

output [
    "Semaine " ++ show(i) ++ ": " ++ concat([ show(Groupes[i, j]) ++ " " | j in GROUPES ]) ++ "\n" | i in SEMAINES ];
    
