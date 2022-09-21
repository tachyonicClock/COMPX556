import random as rnd
import typing as t
import gp.genome as gp


def init_bunker(parent: t.Optional[gp.Gene]) -> gp.Bunker:
    bunker = gp.Bunker(parent)
    bunker.items = [rnd.choice(gp.INFANTRY)(bunker) for _ in range(4)]

def initialise_genome(depth: int, parent: t.Optional[gp.Gene] = None) -> gp.Gene:

    # Base Case
    if depth == 0:
        # add leaf node
        return rnd.choice(
            [*gp.INFANTRY, gp.SiegeTank, init_bunker]
        )(parent)

    # Recursive Case
    depth -= 1
    gene = gp.Quadrant(parent)
    gene.items = [initialise_genome(depth, gene) for _ in range(4)]
    return gene


    