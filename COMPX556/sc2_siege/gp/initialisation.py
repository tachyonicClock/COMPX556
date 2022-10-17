import random as rnd
import typing as t
import gp.chromosome as gp


def random_bunker() -> gp.Bunker:
    return gp.Bunker([rnd.choice(gp.INFANTRY)() for _ in range(4)])


def initialise_chromosome(depth: int, parent: t.Optional[gp.Gene] = None) -> gp.Gene:
    # Base Case
    if depth == 0:
        # add leaf node
        return rnd.choice([*gp.INFANTRY, gp.SiegeTank, random_bunker])()

    # Recursive Case
    depth -= 1
    gene = gp.Quadrant()
    gene.set_parent(parent)
    gene.children = [initialise_chromosome(depth, gene) for _ in range(4)]
    return gene
