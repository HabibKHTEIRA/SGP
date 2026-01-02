from enum import Enum
from dataclasses import dataclass

class VariableStrategy(Enum):
    RANDOM = "random"
    MINIMUM_REMAINING_VALUES = "minimum_values_left"
    LEAST_CONSTRAINTS ="least_constraints"
    MOST_CONSTRAINTS  = "most_constraints"

class RestartException(Exception):
    pass

class ValueStrategy(Enum):
    RANDOM = "random"
    LEAST_USED = "least_used"

class OperationType(Enum):
    ADD : int
    REMOVE: int

@dataclass(frozen= True)
class Operation:
    variable: str
    operation_type: OperationType
    value: int
    depth: int

@dataclass(frozen= True)
class NoGood:
    path: frozenset[tuple[str, bool, int]]