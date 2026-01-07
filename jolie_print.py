import re
import sys
import time

try:
    from run import solve_social_golfer
except ImportError:
    print("Erreur : Impossible de trouver 'run.py'. Assurez-vous que ce fichier est dans le même dossier.")
    sys.exit(1)

def print_schedule(solution: dict[str, set[int]] | None):
    if solution is None:
        print("\n" + "!"*40)
        print("AUCUNE SOLUTION TROUVEE")
        print("!"*40 + "\n")
        return

    print("\n" + "="*46)
    print("PLANNING FINAL DU SOCIAL GOLFER PROBLEM")
    print("="*46 + "\n")

    schedule = {}
    pattern = re.compile(r"W(\d+)G(\d+)")

    for var_name, players_set in solution.items():
        match = pattern.match(var_name)
        if match:
            week = int(match.group(1)) + 1
            group = int(match.group(2)) + 1
            
            if week not in schedule:
                schedule[week] = {}
            
            schedule[week][group] = sorted(list(players_set))

    sorted_weeks = sorted(schedule.keys())

    for w in sorted_weeks:
        week_label = f"SEMAINE {w}"
        groups_data = schedule[w]
        
        group_strings = []
        sorted_groups = sorted(groups_data.keys())
        
        for g in sorted_groups:
            players = groups_data[g]
            p_str = "{" + ", ".join(f"{p:>2}" for p in players) + "}"
            group_strings.append(f"G{g}: {p_str}")
        
        line_content = "   ".join(group_strings)
        
        print(f"{week_label:<10} |  {line_content}")
        print("-" * (len(line_content) + 15))

    print("\nFin de l'affichage.\n")

if __name__ == "__main__":
    WEEKS = 4
    GROUPS = 3
    PLAYERS_PER_GROUP = 3

    print(f"Lancement de la résolution via run.py ({WEEKS} sem, {GROUPS} grp, {PLAYERS_PER_GROUP} j/grp)...")
    
    start_time = time.time()
    result = solve_social_golfer(WEEKS, GROUPS, PLAYERS_PER_GROUP)
    end_time = time.time()
    
    print_schedule(result)
    
    print(f"Temps d'exécution : {end_time - start_time:.4f} secondes")