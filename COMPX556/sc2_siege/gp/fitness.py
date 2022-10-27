from dataclasses import dataclass

@dataclass
class Fitness():
    time: float
    """The time the genotype survived. Measured in game seconds"""
    minerals: int
    """The amount of minerals the genotype consumed"""
    gas: int
    """The amount of gas the genotype consumed"""

    def __str__(self):
        return f'Fitness(time={self.time}, minerals={self.minerals}, gas={self.gas})'


class SquashFitness():
    """Squash the fitness into a single value. Used for sorting and selection."""

    def __init__(self, time_weight: float, mineral_weight: float, gas_weight: float):
        self.mineral_weight = mineral_weight
        self.gas_weight = gas_weight
        self.time_weight = time_weight

    def __call__(self, a: Fitness) -> float:
        return a.time * self.time_weight + a.minerals * self.mineral_weight + a.gas * self.gas_weight
