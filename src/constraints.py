from abc import ABC, abstractmethod
from src.variables import SetVariable

class Constraint(ABC):
    def __init__(self, vars: list[str]):
        self.vars = vars
    
    @abstractmethod
    def reduction(self, variables: dict[str, SetVariable]) -> set[str]:
        pass

    @abstractmethod
    def evaluate(self, variables: dict[str, SetVariable]) -> bool:
        """
            verifie qu'une contrainte est satisfaite par l'assignation actuelle des valeurs
            elle retourne True ssi une borne inferieure du resultat est égale à l'union
            des bornes inferieures des variables
            ex: lower(result) ⊇ lower(var1) ∪ lower(var2)
        """
        pass
    
    def get_variables(self) -> list[str]:
        return self.vars
    



class Union(Constraint):
    def __init__(self, vars, result):
        super().__init__(vars)
        self.result = result
    
    def reduction(self, variables) :
        changed = set()
        upper = variables[self.vars[0]].upper_bound().union(variables[self.vars[1]].upper_bound())

        if not variables[self.result].upper_bound().issuperset(upper):
            variables[self.result]._upper_bound = upper
            changed.add(self.result)
        
        lower = variables[self.vars[0]].lower_bound().union(variables[self.vars[1]].lower_bound())

        if not variables[self.result].lower_bound().issuperset(lower):
            variables[self.result]._lower_bound = lower
            changed.add(self.result)
        
        return changed
    
    def evaluate(self, variables):
        return variables[self.result].lower_bound() == (variables[self.vars[0]].lower_bound().union(variables[self.vars[1]].lower_bound()))

    def get_variables(self):
        return super().get_variables() + [self.result]



class Intersection(Constraint):
    def __init__(self, vars, result):
        super().__init__(vars)
        self.result = result
    
    def reduction(self, variables):
        changed = set()

        upper = variables[self.vars(0)].upper_bound().intersection(variables[self.vars[1]].upper_bound())

        if not variables[self.result].upper_bound().issubset(upper):
            variables[self.result]._upper_bound = upper
            changed.add(self.result)
        
        lower = variables[self.vars(0)].lower_bound().intersection(variables[self.vars[1]].lower_bound())

        if not variables[self.result].lower_bound().issubset(lower):
            variables[self.result]._lower_bound = lower
            changed.add(self.result)

        return changed
    
    def evaluate(self, variables):
        return variables[self.result].lower_bound() == (variables[self.vars[0]].lower_bound().intersection(variables[self.vars[1]].lower_bound()))

    def get_variables(self):
        return super().get_variables() + [self.result]
    


    
    
class CardinalityConstraint(Constraint):
    def __init__(self, vars, card):
        super().__init__(vars)
        self.card = card
    
    def reduction(self, variables):
        changed = set()
        
        # test cas impossible
        if len(variables[self.vars[0]].lower_bound()) > self.card:
            raise Exception("CardinalityConstraint: longeur du lower bound est plus grand que la cardinalité")
        
        if len(variables[self.vars[0]].upper_bound()) < self.card:
            raise Exception("CardinalityConstraint: cardinalité est plus grande que la taille du upper bound")
        
        if len(variables[self.vars[0]].lower_bound()) == self.card:
            if variables[self.vars[0]].upper_bound() != variables[self.vars[0]].lower_bound():
                variables[self.vars[0]]._upper_bound = variables[self.vars[0]].lower_bound()
                changed.add(self.vars[0])
            return changed
        
        if len(variables[self.vars[0]].upper_bound()) == self.card:
            if variables[self.vars[0]].lower_bound() != variables[self.vars[0]].upper_bound():
                variables[self.vars[0]]._lower_bound = variables[self.vars[0]].upper_bound()
                changed.add(variables[self.vars[0]]) 
            return changed
        left_to_find = self.card - len(variables[self.vars[0]].lower_bound())
        left_optional = variables[self.vars[0]].upper_bound() - variables[self.vars[0]].lower_bound()

        if len(left_optional) == left_to_find:
            # elements non present dans lower bound doivent être ajouté
            variables[self.vars[0]].update(left_optional)
            changed.add(self.vars[0])
        return changed

    def evaluate(self, variables):
        return len(variables[self.vars[0]].lower_bound()) == self.card

    def get_variables(self):
        return super().get_variables()
    


    
class IntersectionCardinalityConstraint(Constraint):
    def __init__(self, vars, max_intersections):
        super().__init__(vars)
        self.max_intersections = max_intersections
    
    def reduction(self, variables):
        changed = set()
        
        # verificatin lower bound
        intersection = variables[self.vars[0]].lower_bound().intersection(variables[self.vars[1]].lower_bound())
        if len(intersection) > self.max_intersections:
            raise Exception(f"IntersectionCardinalityConstraint: nb d'élements de l'intersection des lower bounds des variables dépassent {self.max_intersections}")
        
        # filtrage des upper bouns
        for value in variables[self.vars[0]].upper_bound():
            if value not in variables[self.vars[0]].lower_bound():
                intersection_ = len(intersection) + len({value}.intersection(variables[self.vars[1]].lower_bound()))
                if intersection_ > self.max_intersections:
                    variables[self.vars[0]]._upper_bound.remove(value)
                    changed.add(self.vars[0])
        
        for value in variables[self.vars[1]].upper_bound():
            if value not in variables[self.vars[1]].lower_bound():
                intersection_ = len(intersection) + len({value}.intersection(variables[self.vars[0]].lower_bound()))
                if intersection_ > self.max_intersections:
                    variables[self.vars[1]]._upper_bound.remove(value)
                    changed.add(self.vars[1])
        return changed

    def evaluate(self, variables):
        return len(variables[self.vars[0]].lower_bound().intersection(variables[self.vars[1]].lower_bound())) <= self.max_intersections
    
    def get_variables(self):
        return super().get_variables()