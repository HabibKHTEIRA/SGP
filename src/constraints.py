from abc import ABC, abstractmethod
from src import setVariable

class Constraints(ABC):
    def __init__(self, vars: list[str]):
        self.vars = vars
    
    @abstractmethod
    def reduction(self, variables: dict[str, setVariable]) -> set[str]:
        pass

    @abstractmethod
    def evaluate(self, variables: dict[str, setVariable]) -> bool:
        """
            verifie qu'une contrainte est satisfaite par l'assignation actuelle des valeurs
            elle retourne True ssi une borne inferieure du resultat est égale à l'union
            des bornes inferieures des variables
            ex: lower(result) ⊇ lower(var1) ∪ lower(var2)
        """
        pass
    
    def get_variables(self) -> list[str]:
        return self.vars