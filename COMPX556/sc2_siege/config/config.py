import types as t

from gp.fitness import SquashFitness


class Config():
    mineral_weight: float
    """The importance of minerals to the fitness function"""
    gas_weight: float
    """The importance of gas to the fitness function"""
    time_weight: float
    """The importance of survival time to the fitness function"""

    selection_size: int
    """The number of individuals to select for reproduction"""
    population_size: int
    """The number of individuals in the population"""
    init_depth: int
    """The depth of the initial trees"""

    sex_probability: float
    """The probability of a reproduction being sexual"""
    mutation_probability: float
    """The probability of mutation"""
    mutant_tree_depth: int
    """The depth of the mutation"""
    generations: int
    """The number of generations to run the simulation for"""

    generation_log: str
    """Where to log pickle files of each generation"""
    tensorboard_log: str
    """Where to log time series tensorboard data"""

    win_timeout: float
    """How long until the game is considered a win"""
    ready_time_limit: float
    """How long until the agent is forced to start"""

    def __init__(self):
        # Set default values
        self.mineral_weight = -1
        self.gas_weight = -1.5
        self.time_weight = 100.

        self.selection_size = 50
        self.population_size = 100
        self.init_depth = 1

        self.sex_probability = 0.9
        self.mutation_probability = 0.1
        self.generations = 1_000

        self.generation_log = "logs/generation"
        self.tensorboard_log = "logs/tensorboard"

        self.win_timeout = 200
        self.ready_time_limit = 200
        self.mutant_tree_depth = 2

    def fitness_scorer(self):
        return SquashFitness(
            self.time_weight,
            self.mineral_weight,
            self.gas_weight
        )
