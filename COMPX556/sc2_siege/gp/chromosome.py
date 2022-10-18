import typing as t
from copy import deepcopy
from gp.rectangle import Rectangle
import re

class BadChromosome(Exception):
    pass


class Gene():
    """The base class for all genes in a chromosome.
    A chromosome is a tree of genes. Each gene has a parent and a list of
    children. The root gene has no parent and the leaf genes have no children.
    """

    _parent: t.Optional['Composite'] = None

    def set_parent(self, parent: 'Gene'):
        """Set the parent of this gene. This is used to modify the tree
        structure easily.
        """
        self._parent = parent

    @property
    def parent(self) -> t.Optional['Composite']:
        """Return the parent of this gene"""
        return self._parent

    def is_root(self) -> bool:
        """Return True if this gene is the root gene"""
        return self.parent is None

    def to_json(self):
        """Convert this gene to a JSON string"""
        return "{}"

    def __str__(self) -> str:
        """Return a short string representation of this gene"""
        return ""

    def copy(self) -> 'Gene':
        """Return a deep copy of this gene"""
        new_copy = deepcopy(self)
        new_copy._update_parent_references()
        return new_copy

    def iterate(self) -> 'Gene':
        """Iterate over all genes in this gene"""
        yield self

    def locations(self, parent_quad: Rectangle) -> t.Tuple['Gene', t.Tuple[float, float]]:
        """Return a list of genes and their locations"""
        yield (self, parent_quad.center())

    def replace_node(self, replacement: 'Gene'):
        """Replace the target node with the source node"""
        if self.is_root():
            raise ValueError("Cannot replace the root node")

        parent = self.parent
        parent.replace_child(self, replacement)

    def _update_parent_references(self):
        """When a gene is copied, the parent references need to be updated"""
        pass

    def depth(self) -> int:
        """Return the depth of this gene"""
        return 0

    def size(self) -> int:
        """Return the size of this gene"""
        return 1
        

class Leaf(Gene):
    """A leaf gene is a gene that has no children"""
    pass


class Composite(Gene):
    """A composite gene is a gene that has children"""

    child_count = 4
    _children: t.List[Gene] = []

    def __init__(self, children: t.List[Gene] = None, parent: Gene = None) -> None:
        super().__init__()
        if parent:
            self.set_parent(parent)
        if children:
            self.children = children

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children: t.List[Gene]):
        # Bunker can have 2-4 children idk how to do this easily so we just yeetin the whole check
        # if len(children) != self.child_count:
        #     raise ValueError(
        #         f"{type(self)} must have {self.child_count} children")

        # Ensure that the child can be added to this gene
        for child in children:
            self._check_child(child)

        # Remove parent from old children
        for child in self._children:
            child.set_parent(None)

        self._children = children
        for child in children:
            child.set_parent(self)

    def _check_child(self, child: Gene):
        """Check if the child can be added to this gene"""
        pass

    def replace_child(self, old_child: Gene, new_child: Gene):
        """Replace a child of this gene with a new child"""
        if old_child not in self._children:
            raise ValueError(f"{old_child} is not a child of {self}")
        self._check_child(new_child)
        new_child.set_parent(self)
        old_child.set_parent(None)
        self._children[self._children.index(old_child)] = new_child

    def iterate(self) -> Gene:
        yield self
        for item in self._children:
            for sub_item in item.iterate():
                yield sub_item

    def locations(self, parent_quad: Rectangle) -> t.Tuple[Gene, t.Tuple[float, float]]:
        for item, rect in zip(self._children, parent_quad.quarters()):
            for sub_item in item.locations(rect):
                yield sub_item

    def _update_parent_references(self):
        for child in self._children:
            child.set_parent(self)
            child._update_parent_references()

    def depth(self) -> int:
        """Return the depth of this gene"""
        return max(child.depth() for child in self._children) + 1

    def size(self) -> int:
        """Return the size of this gene"""
        return sum(child.size() for child in self._children) + 1
        


class Infantry(Leaf):
    """A type of leaf gene. Notably they can be placed in Bunkers"""
    pass


class Marine(Infantry):
    """A basic infantry unit"""

    def to_json(self):
        return '"Marine"'

    def __str__(self) -> str:
        return "M"


class Marauder(Infantry):
    """An infantry unit that is good against armored units"""

    def to_json(self):
        return '"Marauder"'

    def __str__(self) -> str:
        return "Ma"


class Empty(Infantry):
    """An empty slot in a bunker"""

    def to_json(self):
        return '"Empty"'

    def __str__(self) -> str:
        return ""


class SiegeTank(Leaf):
    """A factory unit that can deal with swarms"""

    def to_json(self):
        return '"SiegeTank"'

    def __str__(self) -> str:
        return "St"


class Quadrant(Composite):
    """A composite gene that has 4 children. It splits the map into 4 quadrants
    and each child is responsible for one quadrant.
    """

    child_count = 4

    def to_json(self):
        str = ','.join(map(lambda x: x.to_json(), self._children))
        return f'{{"Quadrant":[[{str}]]}}'

    def __str__(self) -> str:
        return "Q(" + ''.join(map(lambda x: x.__str__(), self._children)) + ")"


class Bunker(Composite):
    """A composite gene that has 4 children. Only infantry units can be placed
    in a bunker.
    """
    child_count = 4

    def _check_child(self, child: Gene):
        if not isinstance(child, Infantry):
            raise BadChromosome(
                f"{type(self)} must have only Infantry children")
        super()._check_child(child)

    def to_json(self):
        str = ','.join(map(lambda x: x.to_json(), self._children))
        return f'{{"Bunker":[[{str}]]}}'

    def locations(self, parent_quad: Rectangle) -> t.Tuple[Gene, t.Tuple[float, float]]:
        yield from []

    def __str__(self) -> str:
        return "B(" + ''.join(map(lambda x: x.__str__(), self._children)) + ")"


INFANTRY = [
    Marine,
    Marauder,
    Empty
]
