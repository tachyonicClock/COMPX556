from config.config import Config
import gp
from evolution.evolution import Population
from gp.fitness import SquashFitness
from loguru import logger as log
import ray


def pretty_print(pop: Population):
    for i, individual in enumerate(pop._population):
        print(f"{individual.fitness}: {individual}")


def main():
    cfg = Config()
    ray.init()

    cmp = SquashFitness(
        cfg.time_weight,
        cfg.mineral_weight, 
        cfg.gas_weight)

    population: Population = Population.initialize(cfg.population_size, cfg.init_depth)

    mutator = gp.SubtreeMutator(2)
    sexual_reproduction = gp.SubtreeCrossover()

    for i in range(cfg.generations):
        log.info(f"## Generation {i} ##")
        population = population.evaluate()
        pretty_print(population.select(1, cmp))
        population = population.select(cfg.selection_size, cmp)
        population = population.sample(cfg.population_size)
        population = population.stochastic_mutate(mutator.mutate, cfg.mutation_probability)
        population = population.stochastic_sex(sexual_reproduction.crossover, cfg.sex_probability)



if __name__ == '__main__':
    main()