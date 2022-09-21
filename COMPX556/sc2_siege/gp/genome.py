import typing as t
from copy import deepcopy

class Gene():
    def __init__(self, parent: t.Optional['Gene']) -> None:
        self.parent = parent

    def to_json(self):
        return "{}"

    def copy(self) -> 'Gene':
        return deepcopy(self)

    def iterate(self) -> 'Gene':
        yield self

class Terminal(Gene):
    pass

class Composite(Gene):
    items: t.List[Gene]

    def iterate(self) -> Gene:
        yield self
        for item in self.items:
            for sub_item in item.iterate():
                yield sub_item

class Infantry(Terminal):
    pass

class Marine(Infantry):
    def to_json(self):
        return '"Marine"'

class Marauder(Infantry):
    def to_json(self):
        return '"Marauder"'

class SiegeTank(Terminal):
    def to_json(self):
        return '"SiegeTank"'

class Quadrant(Composite):
    def to_json(self):
        str = ','.join(map(lambda x: x.to_json(), self.items))
        return f'{{"Quadrant":[[{str}]]}}'


class Bunker(Composite):
    def to_json(self):
        str = ','.join(map(lambda x: x.to_json(), self.items))
        return f'{{"Bunker":[[{str}]]}}'

INFANTRY = [
    Marine,
    Marauder,
]
