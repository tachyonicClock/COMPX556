import gp
import random as rnd


def find_crossover_point(genotype: gp.Gene) -> gp.Gene:
    """Return a random gene from the genotype"""
    # The first element is the root node, so we don't want to select that
    return rnd.choice(list(genotype.iterate())[1:])


class SubtreeCrossover():
    """A crossover operator that performs subtree crossover"""

    def __init__(self, retries=5):
        self.retries = retries

    def crossover(self, genotype_1: gp.Gene, genotype_2: gp.Gene) -> gp.Gene:
        """Perform subtree crossover on the two genotypes.
        This is a genetic operator that takes two genotypes and returns a new
        genotype. The new genotype is created by taking a random subtree from
        one genotype and replacing a random subtree in the other genotype with
        the subtree from the first genotype. This is repeated until a valid
        genotype is created.
        """
        child = genotype_1.copy()
        for _ in range(self.retries):
            crossover_point_1 = find_crossover_point(child)
            crossover_point_2 = find_crossover_point(genotype_2)

            try:
                crossover_point_1.replace_node(crossover_point_2.copy())
                return child
            except gp.BadGenotype:
                continue

        raise gp.BadGenotype("Could not create a valid child")


class SubtreeMutator():
    """A mutation operator that performs subtree mutation"""

    def __init__(self,
                 random_subtree_depth: int,
                 retries: int = 5
                 ):
        self.random_subtree_depth = random_subtree_depth
        self.retries = retries

    def mutate(self, genotype: gp.Gene) -> gp.Gene:
        """Perform subtree mutation on the genotype.
        This is a genetic operator that takes a genotype and returns a new
        genotype. 
        """
        random_subtree = gp.initialise_genotype(self.random_subtree_depth)
        child = genotype.copy()
        for _ in range(self.retries):
            crossover_point = find_crossover_point(child)

            try:
                crossover_point.replace_node(random_subtree)
                return child
            except gp.BadGenotype:
                continue

        raise gp.BadGenotype("Could not create a valid child")
