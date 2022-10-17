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


    def __init__(self):
        self.mineral_weight = -1.
        self.gas_weight = -1.
        self.time_weight = 1.

        self.selection_size = 10
        self.population_size = 100
        self.init_depth = 2

        self.sex_probability = 0.5
        self.mutation_probability = 0.1
        self.generations = 1_000

        self.generation_log = "logs/generation"
        self.tensorboard_log = "logs/tensorboard"
