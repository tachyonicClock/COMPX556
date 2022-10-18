

import click

import gp
from sc2_evaluator.evaluate import evaluate
from loguru import logger as log

@click.group()
def cli():
    pass

@cli.command()
@click.option('--realtime/--fast', default=True, help='Run in realtime or as fast as possible')
@click.option('--depth', default=2, help='Depth of the chromosome')
def random(realtime: bool, depth: int):
    chromosome = gp.initialise_chromosome(depth)
    log.info(f'Evaluating Gene: {chromosome}')
    fitness = evaluate(
        chromosome,
        realtime,
        win_timeout=110,
        global_timeout=200
    )
    log.info(f'Fitness: {fitness}')

if __name__ == '__main__':
    cli()