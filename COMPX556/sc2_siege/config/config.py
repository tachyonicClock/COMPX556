import types as t

class Config():

    
    mineral_weight: float
    gas_weight: float
    time_weight: float

    selection_size: int
    population_size: int
    init_depth: int

    sex_probability: float
    mutation_probability: float
    generations: int

    generation_log: str
    tensorboard_log: str

    win_timeout: float
    """How long until the game is considered a win"""
    ready_time_limit: float
    """How long until the agent is forced to start"""


    def __init__(self):
        self.mineral_weight = -1
        self.gas_weight = -1.5
        self.time_weight = 100.

        self.selection_size = 10
        self.population_size = 20
        self.init_depth = 1

        self.sex_probability = 0.5
        self.mutation_probability = 0.01
        self.generations = 1_000

        self.generation_log = "logs/generation"
        self.tensorboard_log = "logs/tensorboard"

        self.win_timeout = 120
        self.ready_time_limit = 200
