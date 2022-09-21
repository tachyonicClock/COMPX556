import gp.genome as gp
import random as rnd

def subtree_crossover(parent_a: gp.Gene, parent_b: gp.Gene):
    child: gp.Gene = parent_a.copy()
    candidate_crossover_a = list(child.iterate())
    candidate_crossover_b = list(parent_b.iterate())

    rnd.choice(candidate_crossover_a)
    rnd.choice(candidate_crossover_b)








    pass
