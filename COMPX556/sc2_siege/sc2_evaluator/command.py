import queue
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
import typing as t
import gp
from gp.rectangle import Rectangle 
from sc2_evaluator.const import PRODUCTION_UNIT, UNIT_MAPPING
from sc2.bot_ai import BotAI

class CommandFailed(Exception):
    pass

class Command():
    def __init__(self) -> None:
        self.after: t.List['Command'] = []

    def then(self, command: 'Command') -> 'Command':
        self.after.append(command)
        return self

    def __repr__(self) -> str:
        if len(self.after) > 0:
            return f'{self.__class__.__name__}->{self.after}'
        else:
            return f'{self.__class__.__name__}'
    
class TrainUnit(Command):
    def __init__(self, unit: UnitTypeId, building: UnitTypeId,) -> None:
        self.unit = unit
        self.building = building
        super().__init__()

    def train(self, bot: BotAI):
        building = bot.structures(self.building).idle.random
        if building is None:
            raise CommandFailed(f'No idle {self.building} to train {self.unit}')
        building.train(self.unit)

class PlaceUnit(Command):
    def __init__(self, unit: UnitTypeId, location: Point2) -> None:
        self.unit = unit
        self.location = location
        super().__init__()

    def place(self, bot: BotAI, placed_units: t.Set[int]) -> int:
        # Find a valid unit to place
        units = bot.units(self.unit).tags_not_in(placed_units)
        if units.empty:
            raise CommandFailed(f'No {self.unit} to place')
        unit = units.random
        
        # Attempt to move the unit
        if unit.move(self.location) != True:
            raise CommandFailed("Failed to move unit")    
        return unit.tag 



class BuildStructure(Command):
    def __init__(self, unit: UnitTypeId, location: Point2) -> None:
        self.unit = unit
        self.location = location
        super().__init__()

    def build(self, bot: BotAI):
        if not bot.workers.idle.exists:
            raise CommandFailed("No idle workers to build")

        worker = bot.workers.idle.random
        worker.build(self.unit, self.location)
        
            

class GarrisonStructure(PlaceUnit):
    def __init__(self, unit: UnitTypeId, location: Point2, structure: UnitTypeId) -> None:
        super().__init__(unit, location)
        self.structure = structure

    def place(self, bot: BotAI, placed_units: t.Set[int]) -> int:
        # Are units available to garrison and does the structure exist?
        units = bot.units(self.unit).tags_not_in(placed_units)
        structures = bot.structures.ready.of_type(self.structure).closer_than(1, self.location)
        if units.empty:
            raise CommandFailed(f'No {self.unit} to place')
        if structures.empty:
            raise CommandFailed(f'No {self.structure} to garrison')

        # Attempt to garrison the unit
        unit = units.random
        if unit.smart(structures.first) != True:
            raise CommandFailed("Failed to move unit")    
        return unit.tag 


def build_command_queue(gene: gp.Gene, parent_quad: Rectangle) -> t.List[Command]:
    queue = []
    x, y = parent_quad.center()
    position = Point2([x, 80-y])

    if isinstance(gene, gp.Quadrant):
        # Recursively build the command queue
        for child, quad in zip(gene.children,  parent_quad.quarters()):
            queue.extend(build_command_queue(child, quad))
    elif isinstance(gene, gp.Empty):
        pass
    elif isinstance(gene, gp.Leaf):
        # Create a train command to build the unit and then a place command 
        # to place the unit on the battlefield
        unit = UNIT_MAPPING[type(gene)]
        prod = PRODUCTION_UNIT[unit]
        cmd = TrainUnit(unit, prod).then(PlaceUnit(unit, position))
        queue.append(cmd)
    elif isinstance(gene, gp.Bunker):
        # Create a command to build a bunker and then garrison units in it
        cmd = BuildStructure(UnitTypeId.BUNKER, position)
        for child in gene.children:
            # Skip empty children
            if isinstance(child, gp.Empty):
                continue

            unit = UNIT_MAPPING[type(child)]
            prod = PRODUCTION_UNIT[unit]
            cmd = cmd.then(TrainUnit(unit, prod).then(GarrisonStructure(unit, position, UnitTypeId.BUNKER)))
        queue.append(cmd)
    return queue
