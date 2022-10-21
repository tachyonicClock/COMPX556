import pickle
import click
from config.config import Config
from evolution.loggers import LogCallback, SaveGeneration, Tensorboard
import gp
from evolution.evolution import Population, PopulationEvaluator
from gp.fitness import SquashFitness
from loguru import logger as log
import ray
import typing as t
import os

def pretty_print(pop: Population, to_fitness_score: SquashFitness):
    log.info("---------------------------------------------------------------")
    for i, individual in enumerate(pop._population):
        log.info(f"Fitness score:      {to_fitness_score(individual.fitness)}")
        log.info(f"Fitness components: {individual.fitness}")
        log.info(f"Chromosome:         {individual.chromosome}")
    log.info("---------------------------------------------------------------")



@click.command()
@click.option('--purge', default=False, is_flag=True, help='Remove all existing results')
@click.option('--num-cpus', default=1, help='Number of CPUs to use')
@click.option('--resume', default=False, is_flag=True, help='Continue from last generation')
def main(purge: bool, num_cpus: int, resume: bool):
    cfg = Config()
    ray.init(num_cpus=num_cpus)

    if purge and resume:
        log.warning("Cannot purge and resume at the same time")
    elif purge:
        os.system(f'rm -rf {cfg.tensorboard_log} {cfg.generation_log}')
        os.system(f'mkdir -p {cfg.tensorboard_log} {cfg.generation_log}')

    loggers: t.List[LogCallback] = [
        Tensorboard(f"{cfg.tensorboard_log}"),
        SaveGeneration(f"{cfg.generation_log}")
    ]

    to_fitness_score = cfg.fitness_scorer()

    population = Population.initialize(
        cfg.population_size,
        cfg.init_depth,
        to_fitness_score,
    )

    pop_eval = PopulationEvaluator(
        cfg.win_timeout,
        cfg.ready_time_limit
    )

    log.info("Initial population")

    mutator = gp.SubtreeMutator(2)
    sexual_reproduction = gp.SubtreeCrossover()

    start_generation = 0
    if resume:
        # get last generation from file
        start_generation = max(map(lambda x : int(x[-len("0000.pkl"):-len(".pkl")]), os.listdir(cfg.generation_log)))
        
        log.info(f"Resuming from generation {start_generation}")
        with open(f'{cfg.generation_log}/generation_{start_generation:04d}.pkl', 'rb') as f:
            population = pickle.load(f)

    for i in range(start_generation, cfg.generations):
        log.info(f"## Generation {i} ##")
        population = pop_eval.evaluate(population)

        log.info("Logging population")
        for logger in loggers:
            logger.after_pop_eval(i, population)

        pretty_print(population.select(1), to_fitness_score)
        population = population.select(cfg.selection_size)
        population = population.sample(cfg.population_size)
        population = population.stochastic_mutate(mutator.mutate, cfg.mutation_probability)
        population = population.stochastic_sex(sexual_reproduction.crossover, cfg.sex_probability)



if __name__ == '__main__':
    main()