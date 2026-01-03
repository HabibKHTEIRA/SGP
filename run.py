from src import SetSolver, SetVariable, CardinalityConstraint, IntersectionCardinalityConstraint, Intersection

from itertools import combinations, product

def solve_social_golfer(num_weeks, num_groups, group_size):
    total_players = num_groups * group_size
    all_players = set(range(total_players))

    solver = SetSolver()
    week_groups = {}

    # Création des groupes
    for w in range(num_weeks):
        for g in range(num_groups):
            name = f"W{w}G{g}"
            group = SetVariable(name, set(), all_players)
            week_groups[name] = group
            solver._add_variable(group)

            # Taille fixe des groupes
            solver._add_constraint(
                CardinalityConstraint([name], group_size)
            )

    # Un joueur ne peut être que dans un groupe par semaine
    for w in range(num_weeks):
        groups = [f"W{w}G{g}" for g in range(num_groups)]
        for g1, g2 in combinations(groups, 2):
            solver._add_constraint(
                IntersectionCardinalityConstraint([g1, g2], 0)
            )

    # Deux joueurs ne peuvent pas jouer ensemble plus d'une fois
    for w1, w2 in combinations(range(num_weeks), 2):
        for g1, g2 in product(range(num_groups), repeat=2):
            solver._add_constraint(
                IntersectionCardinalityConstraint(
                    [f"W{w1}G{g1}", f"W{w2}G{g2}"], 1
                )
            )

    # Bris de symétrie : le joueur 0 est toujours dans le groupe 0
    for w in range(num_weeks):
        week_groups[f"W{w}G0"]._lower_bound.add(0)

    return solver.solve()


if __name__ == "__main__":
    print(solve_social_golfer(4, 3, 3))