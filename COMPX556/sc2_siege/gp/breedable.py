import gp
import random as rnd


def find_crossover_point(chromosome: gp.Gene) -> gp.Gene:
    """Return a random gene from the chromosome"""
    # The first element is the root node, so we don't want to select that
    return rnd.choice(list(chromosome.iterate())[1:])


class SubtreeCrossover():
    """A crossover operator that performs subtree crossover"""

    def __init__(self, retries=5):
        self.retries = retries

    def crossover(self, chromosome_1: gp.Gene, chromosome_2: gp.Gene) -> gp.Gene:
        """Perform subtree crossover on the two chromosomes.
        This is a genetic operator that takes two chromosomes and returns a new
        chromosome. The new chromosome is created by taking a random subtree from
        one chromosome and replacing a random subtree in the other chromosome with
        the subtree from the first chromosome. This is repeated until a valid
        chromosome is created.
        """
        child = chromosome_1.copy()
        for _ in range(self.retries):
            crossover_point_1 = find_crossover_point(child)
            crossover_point_2 = find_crossover_point(chromosome_2)

            try:
                crossover_point_1.replace_node(crossover_point_2.copy())
                return child
            except gp.BadChromosome:
                continue

        raise gp.BadChromosome("Could not create a valid child")



class SubtreeMutator():
    """A mutation operator that performs subtree mutation"""

    def __init__(self, 
            random_subtree_depth: int,
            retries: int = 5
        ):
        self.random_subtree_depth = random_subtree_depth
        self.retries = retries

    def mutate(self, chromosome: gp.Gene) -> gp.Gene:
        """Perform subtree mutation on the chromosome.
        This is a genetic operator that takes a chromosome and returns a new
        chromosome. 
        """
        random_subtree = gp.initialise_chromosome(self.random_subtree_depth)
        child = chromosome.copy()
        for _ in range(self.retries):
            crossover_point = find_crossover_point(child)

            try:
                crossover_point.replace_node(random_subtree)
                return child
            except gp.BadChromosome:
                continue

        raise gp.BadChromosome("Could not create a valid child")


