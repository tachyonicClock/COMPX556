import gp
import pytest
from gp.breedable import SubtreeMutator

from gp.chromosome import BadChromosome


def test_quadrant():
    gene = gp.Quadrant()
    gene.children = [gp.SiegeTank(), gp.Marauder(), gp.Marine(), gp.Marine()]
    assert gene.to_json(
    ) == '{"Quadrant":[["SiegeTank","Marauder","Marine","Marine"]]}'
    assert gene.__str__() == "Q(StMaMM)"

    with pytest.raises(ValueError):
        gene.children = [gp.SiegeTank(), gp.Marauder(), gp.Marine()]


def test_initialise_chromosome():
    chromosome = gp.initialise_chromosome(2)


def test_replace_node():
    """Test that the replace_node method works and parent references are updated"""
    marine = gp.Marine()
    parent_a = gp.Quadrant(
        [
            marine,
            gp.Marine(),
            gp.Marine(),
            gp.Marine(),
        ]
    )

    siege_tank = gp.SiegeTank()
    marine.replace_node(siege_tank)
    assert marine.parent == None
    assert siege_tank.parent == parent_a
    assert str(parent_a) == "Q(StMMM)"


def test_invalid_replace():
    """Test that the replace_node method works and parent references are updated"""
    marine = gp.Marine()
    gp.Bunker(
        [
            marine,
            gp.Marine(),
            gp.Marine(),
            gp.Marine(),
        ]
    )

    siege_tank = gp.SiegeTank()
    with pytest.raises(BadChromosome):
        marine.replace_node(siege_tank)


def test_copy():
    """Test that the copy method works and parent references are updated"""
    marine = gp.Marine()
    parent_a = gp.Quadrant(
        [
            marine,
            gp.Marine(),
            gp.Marine(),
            gp.Marine(),
        ]
    )
    parent_b: gp.Quadrant = parent_a.copy()

    assert parent_a.to_json() == parent_b.to_json()
    assert parent_a is not parent_b
    assert parent_b.children[0].parent is parent_b
    assert parent_b.children[0].parent is not parent_a


def test_subtree_crossover():
    parent_a = gp.initialise_chromosome(3)
    parent_b = gp.initialise_chromosome(3)
    crossover = gp.SubtreeCrossover(5)

    for _ in range(10):
        parent_a = crossover.crossover(parent_a, parent_b)

def test_subtree_mutation():
    parent_a = gp.initialise_chromosome(1)
    mutator = SubtreeMutator(1, 5)
    for _ in range(10):
        parent_a = mutator.mutate(parent_a)
        print(parent_a)
