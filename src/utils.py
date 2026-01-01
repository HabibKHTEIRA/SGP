from enum import Enum
from dataclasses import dataclass

class VariableStrategy(Enum):
    RANDOM = "random"
    SMALLEST_DOMAIN = "smallest_domain"


class ValueStrategy(Enum):
    RANDOM = "random"

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
    pass