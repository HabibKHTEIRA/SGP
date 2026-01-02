from .variables import SetVariable
from .utils import NoGood, ValueStrategy, VariableStrategy, Operation, RestartException, NoGood, OperationType
from .constraints import Constraint

import random

class SetSolver:
    RESTART_THRESHOLD = 10
    TOP_K = 3
    MAX_DEPTH = 100
    def __init__(self, variable_strategy = None, valeur_strategy= None):
        self.nogoods: set[NoGood]                = set()
        self.variable_strategy: VariableStrategy = variable_strategy if variable_strategy else VariableStrategy.RANDOM
        self.valeur_strategy: ValueStrategy      = valeur_strategy if valeur_strategy else ValueStrategy.RANDOM
        self.variables: dict[str, SetVariable] = {}
        self.constraints: list[Constraint] = list()
        self.nb_var_values: dict[str, dict[int, int]] = {}

        self.operations_history: list[Operation] = list()
        self.solution: list[Operation] = list()
        self.visited_states: set[tuple[Operation, ...]] = set()

        self.current_depth = 0
        self.cpt_since_random_selection = 0
        self.cpt_since_restart =0
        self.nogoods_learned  =0

        self.restarting = False
        




    def _add_variable(self, variable: SetVariable):
        self.variables[variable.name] = variable

        if variable.name not in self.nb_var_values:
            self.nb_var_values[variable.name] = {}
        
        for value in variable.upper_bound():
            self.nb_var_values[variable.name][value] = 0

    def _add_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)
    
    def _get_cpt_variable_constraint(self, name: str) -> int:
        return sum(1 for c in self.constraints if name in (c.get_variables()) )

    def _choose_value(self, var: SetVariable) -> list[int]:
        values = list(var.upper_bound() - var.lower_bound())

        if self.valeur_strategy == ValueStrategy.RANDOM:
            random.shuffle(values)
            return values
        else:
            return sorted(values, key = lambda x: self.nb_var_values.get(var.name, {}).get(x, 0))


    def _choose_variable(self, variables: dict[str, SetVariable]) -> tuple[str, SetVariable] | None:
        unsorted_variables = [
            (name, setvar) for name, setvar in variables.items() if not setvar.determined()
        ]

        if not unsorted_variables:
            return None
        
        if self.variable_strategy == VariableStrategy.RANDOM:
            return random.choice(unsorted_variables)
        
        # trie selon heuristique
        sorted_variables = None

        if self.variable_strategy == VariableStrategy.MINIMUM_REMAINING_VALUES:
            sorted_variables = sorted(
                unsorted_variables, key = lambda x: len(x[1].upper_bound() - x[1].lower_bound()) 
            )

        elif self.variable_strategy == VariableStrategy.LEAST_CONSTRAINTS:
            sorted_variables = sorted(
                unsorted_variables, key = lambda x: self._get_cpt_variable_constraint(x[0])
            )

        elif self.variable_strategy == VariableStrategy.MOST_CONSTRAINTS:
            sorted_variables = sorted(
                unsorted_variables, key = lambda x: self._get_cpt_variable_constraint(x[0]),
                reverse = True
            )

        # introduction d'une randomisation pour sortir des minima locaux
        self.cpt_since_random_selection += 1
        if self.cpt_since_random_selection >= self.RESTART_THRESHOLD and len(sorted_variables) >=1:
            self.cpt_since_random_selection =0
            candidats = sorted_variables[:min(self.TOP_K, len(sorted_variables))]
            return random.choice(candidats)

        if self.current_depth >= self.MAX_DEPTH:
            self._restart()

        return sorted_variables[0] 
        
    def _restart(self):
        if self.current_depth >= self.MAX_DEPTH:
            # reinit métriques:
            self.cpt_since_random_selection =0
            self.cpt_since_restart =0
            self.current_depth =0

            # reinit historique
            self.solution.clear()
            self.operations_history.clear()

            # reinit des variables
            for var in self.variables.values:
                var.reset() # non encore implementé
            
            # reinitialisation de nb_var_values
            for var_name in self.nb_var_values:
                for value in self.nb_var_values[var_name]:
                    self.nb_var_values[var_name][value]=0

            raise RestartException()
        return False
    
    def _path_to_nogood(self, current_path : list[Operation]) -> NoGood:
        operations= set()
        for operation in reversed(current_path):
            if not any(a[0] == operation.variable for a in operations): # verifie qu'un operation n'existe pas déja
                operations.add(operation.variable, operation.operation_type == OperationType.ADD, operation.value )

    def _learn_nogood(self, failed_path: list[Operation]):
        if failed_path:
            nogood= self._path_to_nogood(failed_path)
            if nogood not in self.nogoods:
                self.nogoods.add(nogood)
                self.nogoods_learned +=1
    
    def _is_nogood(self, current_path: list[Operation]) -> bool:
        # transformer le chemin actuel en dict d'assignations uniques
        current_assignments = {
            op.variable: (op.variable, op.op_type == OperationType.ADD, op.value)
            for op in current_path
        }

        for nogood in self.nogoods:
            # vérifier si toutes les assignations du nogood sont présentes et identiques
            if all(
                current_assignments.get(var[0]) == var
                for var in nogood.assignments
            ):
                self.metrics.nogood_hits += 1
                return True

        return False



    def solve(self) -> dict[str, set] |None:
        try:
            while not self.restarting:
                try:
                    self.restarting = False
                    return self._solve()
                except RestartException:
                    pass
        except Exception as e:
            print(f"erreur: {str(e)}")
            return None



    def _solve(self):
        pass
        