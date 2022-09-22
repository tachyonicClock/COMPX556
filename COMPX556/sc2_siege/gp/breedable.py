import gp.chromosome as gp
import random as rnd


def find_crossover_point(chromosome: gp.Gene) -> gp.Gene:
    """Return a random gene from the chromosome"""
    # The first element is the root node, so we don't want to select that
    return rnd.choice(list(chromosome.iterate())[1:])


def subtree_crossover(chromosome_1: gp.Gene, chromosome_2: gp.Gene, retries=5) -> gp.Gene:
    """Perform subtree crossover on the two chromosomes.
    This is a genetic operator that takes two chromosomes and returns a new
    chromosome. The new chromosome is created by taking a random subtree from
    one chromosome and replacing a random subtree in the other chromosome with
    the subtree from the first chromosome. This is repeated until a valid
    chromosome is created.
    """
    child = chromosome_1.copy()
    for _ in range(retries):
        crossover_point_1 = find_crossover_point(child)
        crossover_point_2 = find_crossover_point(chromosome_2)

        try:
            crossover_point_1.replace_node(crossover_point_2.copy())
            return child
        except gp.BadChromosome:
            continue

    raise gp.BadChromosome("Could not create a valid child")
