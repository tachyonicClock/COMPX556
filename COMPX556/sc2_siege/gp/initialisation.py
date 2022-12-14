import random as rnd
import typing as t
import gp.genotype as gp


def random_bunker() -> gp.Bunker:
    return gp.Bunker([rnd.choice(gp.INFANTRY)() for _ in range(4)])


def initialise_genotype(depth: int, parent: t.Optional[gp.Gene] = None) -> gp.Gene:
    # Base Case
    if depth == 0:
        # add leaf node
        return rnd.choice([*gp.INFANTRY, gp.SiegeTank, random_bunker])()

    # Recursive Case
    depth -= 1
    gene = gp.Quadrant()
    gene.set_parent(parent)
    gene.children = [initialise_genotype(depth, gene) for _ in range(4)]
    return gene


def fill_bunker():
    i = 0
    units = []
    while i < 4:
        unit = rnd.choice(gp.INFANTRY)()
        if isinstance(unit, gp.Marine) or isinstance(unit, gp.Empty):
            if i + 1 <= 4:
                units.append(unit)
                i += 1
        elif isinstance(unit, gp.Marauder):
            if i + 2 <= 4:
                units.append(unit)
                i += 2
        else:
            raise gp.BadGenotype("Invalid infantry type")
    return units
