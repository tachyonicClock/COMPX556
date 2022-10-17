import click
from config.config import Config
from evolution.loggers import LogCallback, SaveGeneration, Tensorboard
import gp
from evolution.evolution import Population
from gp.fitness import SquashFitness
from loguru import logger as log
import ray
import typing as t
import os

def pretty_print(pop: Population):
    for i, individual in enumerate(pop._population):
        print(f"{individual.fitness}: {individual}")


@click.command()
@click.option('--purge', default=False, is_flag=True, help='Remove all existing results')
def main(purge: bool):
    cfg = Config()
    ray.init()

    if purge:
        os.system(f'rm -rf {cfg.tensorboard_log} {cfg.generation_log}')
        os.system(f'mkdir -p {cfg.tensorboard_log} {cfg.generation_log}')

    loggers: t.List[LogCallback] = [
        Tensorboard(f"{cfg.tensorboard_log}"),
        SaveGeneration(f"{cfg.generation_log}")
    ]

    to_fitness_score = SquashFitness(
        cfg.time_weight,
        cfg.mineral_weight, 
        cfg.gas_weight)

    population: Population = Population.initialize(cfg.population_size, cfg.init_depth, to_fitness_score)

    log.info("Initial population")

    mutator = gp.SubtreeMutator(2)
    sexual_reproduction = gp.SubtreeCrossover()

    for i in range(cfg.generations):
        log.info(f"## Generation {i} ##")
        population = population.evaluate()

        log.info("Logging population")
        for logger in loggers:
            logger.after_pop_eval(i, population)

        pretty_print(population.select(1))
        population = population.select(cfg.selection_size)
        population = population.sample(cfg.population_size)
        population = population.stochastic_mutate(mutator.mutate, cfg.mutation_probability)
        population = population.stochastic_sex(sexual_reproduction.crossover, cfg.sex_probability)



if __name__ == '__main__':
    main()