class setVariable:
    def __init__(self, name, lower_bound = None, upper_bound = None):
        self.name = name
        self._lower_bound: set[int] = set() if lower_bound is None else set(lower_bound)
        self._upper_bound: set[int] = set() if upper_bound is None else set(upper_bound)

        if not self._lower_bound.issubset(self._upper_bound):
            raise Exception("lower bound d'une variable doit être inclus dans le upper bound")
    
    @property
    def lower_bound(self) -> set[int]:
        return self._lower_bound.copy()

    @property
    def upper_bound(self) -> set[int]:
        return self._upper_bound.copy()
    
    def determined(self):
        return self._lower_bound == self._upper_bound
    
    def __str__(self):
        return f"{self.name} lower bound: {self._lower_bound} , upper bound: {self._upper_bound}"