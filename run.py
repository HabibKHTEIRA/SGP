from src import SetSolver, SetVariable, CardinalityConstraint, IntersectionCardinalityConstraint, Intersection



def solve_social_golfer_1(num_groups, group_size, num_weeks):
    total_golfers = num_groups * group_size
    all_players = set(range(total_golfers))

    solver = SetSolver()

    # Crée les variables de chaque groupe pour chaque semaine
    week_groups = {}
    for w in range(num_weeks):
        for g in range(num_groups):
            name = f"W{w}G{g}"
            group = SetVariable(name, lower_bound=set(), upper_bound=all_players.copy())
            week_groups[name] = group
            solver._add_variable(group)
            # Contrainte sur la taille du groupe
            solver._add_constraint(CardinalityConstraint([name], group_size))

    # Contrainte : pas de joueur dans deux groupes la même semaine
    for w in range(num_weeks):
        group_names = [f"W{w}G{g}" for g in range(num_groups)]
        for i, g1 in enumerate(group_names):
            for g2 in group_names[i + 1:]:
                solver._add_constraint(IntersectionCardinalityConstraint([g1, g2], 0))

    # Contrainte : pas de joueur avec un même partenaire plus d'une fois
    for w1 in range(num_weeks):
        for w2 in range(w1 + 1, num_weeks):
            for g1 in range(num_groups):
                for g2 in range(num_groups):
                    solver._add_constraint(
                        IntersectionCardinalityConstraint(
                            [f"W{w1}G{g1}", f"W{w2}G{g2}"], 1
                        )
                    )

    # Symmetry breaking : joueur 0 toujours dans le premier groupe
    for w in range(num_weeks):
        week_groups[f"W{w}G0"]._lower_bound.add(0)

    result = solver.solve()
    print(result)
    return result


if __name__ == "__main__":
    solve_social_golfer_1(4, 4, 4)