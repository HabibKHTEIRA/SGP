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

        upper = variables[self.vars[0]].upper_bound().intersection(variables[self.vars[1]].upper_bound())

        if not variables[self.result].upper_bound().issubset(upper):
            variables[self.result]._upper_bound = upper
            changed.add(self.result)
        
        lower = variables[self.vars[0]].lower_bound().intersection(variables[self.vars[1]].lower_bound())

        if not variables[self.result].lower_bound().issubset(lower):
            variables[self.result]._lower_bound = lower
            changed.add(self.result)

        return changed
    
    def evaluate(self, variables):
        return variables[self.result].lower_bound() == (variables[self.vars[0]].lower_bound().intersection(variables[self.vars[1]].lower_bound()))

    def get_variables(self):
        return super().get_variables() + [self.result]
    

class Difference(Constraint):
    def __init__(self, vars, result):
        super().__init__(vars)
        self.result = result

    def reduction(self, variables):
        changed = set()
        
        upper = variables[self.vars[0]].upper_bound() - variables[self.vars[1]].lower_bound()
        
        if not variables[self.result].upper_bound().issuperset(upper):
            variables[self.result]._upper_bound = upper
            changed.add(self.result)
        
        lower = variables[self.vars[0]].lower_bound() - variables[self.vars[1]].upper_bound()
        
        if not variables[self.result].lower_bound().issuperset(lower):
            variables[self.result]._lower_bound = lower
            changed.add(self.result)
        
        return changed
    
    def evaluate(self, variables):
        return variables[self.result].lower_bound() == (
            variables[self.vars[0]].lower_bound() - variables[self.vars[1]].lower_bound()
        )
    
    def get_variables(self):
        return super().get_variables() + [self.result]
    

class Subset(Constraint):
    """
    Contrainte de sous-ensemble: var1 ⊆ var2
    (tous les éléments de var1 doivent être dans var2)
    """
    def __init__(self, vars):
        super().__init__(vars)
    
    def reduction(self, variables):
        changed = set()
        
        upper_var1 = variables[self.vars[0]].upper_bound() & variables[self.vars[1]].upper_bound()
        
        if not variables[self.vars[0]].upper_bound().issuperset(upper_var1):
            variables[self.vars[0]]._upper_bound = upper_var1
            changed.add(self.vars[0])
        
        lower_var2 = variables[self.vars[1]].lower_bound() | variables[self.vars[0]].lower_bound()
        
        if not variables[self.vars[1]].lower_bound().issuperset(lower_var2):
            variables[self.vars[1]]._lower_bound = lower_var2
            changed.add(self.vars[1])
        
        return changed
    
    def evaluate(self, variables):
        return variables[self.vars[0]].lower_bound().issubset(
            variables[self.vars[1]].lower_bound()
        )
    
    def get_variables(self):
        return super().get_variables()

class Different(Constraint):
    """
    Contrainte de différence: var1 ≠ var2
    (var1 et var2 ne peuvent pas être égaux)
    """
    def __init__(self, vars):
        super().__init__(vars)
    
    def reduction(self, variables):
        changed = set()

        if(
            variables[self.vars[0]].determined() and variables[self.vars[1]].determined()
            and variables[self.vars[0]].lower_bound == variables[self.vars[1]].lower_bound
        ):
            raise ValueError("contrainte 'Different' insatisfaisable")
        
        return changed
    
    def evaluate(self, variables):
        return variables[self.vars[0]].lower_bound() != variables[self.vars[1]].lower_bound()
    
    def get_variables(self):
        return super().get_variables()
    
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
                changed.add(self.vars[0]) 
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

    def reduction(self, variables) -> bool:
        x = variables[self.vars[0]]
        y = variables[self.vars[1]]

        changed = False

        # Recalcul systématique
        lb_x = x.lower_bound()
        lb_y = y.lower_bound()
        ub_x = x.upper_bound().copy()
        ub_y = y.upper_bound().copy()

        intersection_lb = lb_x & lb_y

        # Incohérence immédiate
        if len(intersection_lb) > self.max_intersections:
            raise ValueError(
                f"IntersectionCardinalityConstraint: |LB(x) ∩ LB(y)| > {self.max_intersections}"
            )

        # Filtrage UB(x)
        for v in ub_x:
            if v in lb_x:
                continue
            if v in lb_y and len(intersection_lb) + 1 > self.max_intersections:
                x._upper_bound.remove(v)
                changed = True

        # Filtrage UB(y)
        for v in ub_y:
            if v in lb_y:
                continue
            if v in lb_x and len(intersection_lb) + 1 > self.max_intersections:
                y._upper_bound.remove(v)
                changed = True

        return changed

    def evaluate(self, variables) -> bool:
        x = variables[self.vars[0]]
        y = variables[self.vars[1]]
        return len(x.lower_bound() & y.lower_bound()) <= self.max_intersections
