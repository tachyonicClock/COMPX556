import random
import pytest
from config.config import Config
from evolution.evolution import Individual, Population
import gp
from gp.fitness import SquashFitness

cfg = Config()

@pytest.fixture
def population():
    return Population.initialize(10, 2)

@pytest.fixture
def simple_population() -> Population:
    return Population([Individual(gp.Marine()) for _ in range(5)])

def test_init(population):
    assert population is not None

def test_evaluate(population):
    population.evaluate()

def test_select(population: Population):
    cmp = SquashFitness(cfg.mineral_weight, cfg.gas_weight, cfg.time_weight)

    for p in population._population:
        p.fitness = gp.Fitness(random.random(), random.random(), random.random())

    selected = population.remove_unfit(5, cmp)
    assert len(selected._population) == 5

    # Assert they are in order
    for i in range(len(selected._population) - 1):
        assert cmp(selected._population[i].fitness) >= cmp(selected._population[i + 1].fitness)


def test_stochastic_mutate(simple_population: Population):
    random.seed(42) # IMPORTANT: This is required to get the same result every time
    mutator = lambda x: gp.Marauder()

    # Count marines in population
    marauder = 0
    new_pop = simple_population.stochastic_mutate(mutator, 0.5)
    for individual in new_pop._population:
        if isinstance(individual.genotype, gp.Marauder):
            marauder += 1
    assert marauder == 3, "Expected 3 marauders but got {}".format(marauder)

def test_stochastic_sex(simple_population: Population):
    random.seed(42) # IMPORTANT: This is required to get the same result every time
    sex = lambda a, b : gp.Quadrant([a, b, gp.Empty(), gp.Empty()])

    new_pop = simple_population.stochastic_sex(sex, 0.5)
    i = 0
    for individual in new_pop._population:
        if str(individual.genotype) == "Q(MM)":
            i += 1
    assert i == 2, "Expected 2 individuals with Q(MM) but got {}".format(i)


def test_sample(population: Population):
    pop = population.sample(5)
    assert len(pop) == 5
    pop = pop.sample(10)
    assert len(pop) == 10


    
