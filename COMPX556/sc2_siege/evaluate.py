import pickle
import click
from config.config import Config
from evolution.evolution import Population

import gp
from sc2_evaluator.evaluate import evaluate, run_human_playable
from loguru import logger as log


@click.group()
def cli():
    pass


@cli.command()
@click.option('--realtime/--fast', default=True, help='Run in realtime or as fast as possible')
@click.option('--depth', default=2, help='Depth of the genotype')
@click.option('--no-eval', default=False, is_flag=True, help='Skip evaluation')
def random(realtime: bool, depth: int, no_eval: bool):
    genotype = gp.initialise_genotype(depth)
    log.info(f'Evaluating Gene: {genotype}')
    if not no_eval:
        fitness = evaluate(
            genotype,
            realtime,
            win_timeout=110,
            ready_time_limit=200
        )
        log.info(f'Fitness: {fitness}')


@cli.command()
@click.argument("genotype")
@click.option('--no-eval', default=False, is_flag=True, help='Skip evaluation')
@click.option('--realtime/--fast', default=True, help='Run in realtime or as fast as possible')
def load(genotype: str, no_eval: bool, realtime: bool):
    cfg = Config()
    gene = gp.from_str(genotype)
    log.info(f'Evaluating Gene: {gene}')
    if not no_eval:
        fitness = evaluate(
            gene,
            realtime,
            win_timeout=cfg.win_timeout,
            ready_time_limit=cfg.ready_time_limit
        )
        log.info(f'Fitness: {fitness}')


@cli.command()
def manual():
    run_human_playable()


@cli.command()
@click.argument("genotype")
@click.argument("filename")
def plot(genotype: str, filename: str):
    gene = gp.from_str(genotype)
    img = gp.plot_individual(gene)
    img.save(filename)


@cli.command()
@click.argument("population_pickle")
def population(population_pickle: str):
    cfg = Config()

    with open(population_pickle, 'rb') as f:
        population: Population = pickle.load(f)

    to_fitness_score = cfg.fitness_scorer()
    for individual in population.select(len(population)):

        log.info(
            f'{to_fitness_score(individual.fitness):.2f}: {individual.genotype}')


if __name__ == '__main__':
    cli()
