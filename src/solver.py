from .variables import SetVariable
from .utils import NoGood, ValueStrategy, VariableStrategy, Operation
from .constraints import Constraint

import random

class SetSolver:
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

    def _choose_variable(self, variables: dict[str, SetVariable]) -> tuple[str, SetVariable]:
        pass