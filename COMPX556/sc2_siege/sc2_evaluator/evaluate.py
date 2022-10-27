import typing as t

import gp
from gp.fitness import Fitness
from gp.rectangle import Rectangle
from loguru import logger
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Race
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game
from sc2.player import Bot, Human
from sc2.position import Point2
from sc2.unit import Unit, UnitOrder

import sc2_evaluator.command as cmd


class Evaluategenotype(BotAI):


    def __init__(self, commands: t.List[cmd.Command], win_timeout: float, ready_time_limit: float) -> None:
        super().__init__()
        self.commands = commands
        self.placed_units: t.Set[int] = set()
        self.commands: t.List[cmd.Command]
        self.setup_done: bool = False
        self.score: float = -1
        self.bunkers = {}
        self.starting_minerals: int = -1
        self.starting_gas: int = -1
        self.starting_game_time: int = -1
        self.win_timeout = win_timeout
        self.ready_time_limit = ready_time_limit

    def consume_command(self) -> t.List[cmd.Command]:
        command = self.commands.pop()

        logger.trace(f'Performing command {command}')
        try:
            if isinstance(command, cmd.TrainUnit):
                command.train(self)
                logger.trace(
                    f'Training  {command.unit.name} in {command.building.name}')
            elif isinstance(command, cmd.PlaceUnit):
                tag = command.place(self, self.placed_units)
                self.placed_units.add(tag)
                logger.trace(
                    f'Placing   {command.unit.name} at {command.location}')
            elif isinstance(command, cmd.BuildStructure):
                command.build(self)
                self.bunkers[command.location] = command.after
                logger.trace(
                    f'Building  {command.unit.name} at {command.location}')

            self.commands.extend(command.after)

        except cmd.CommandFailed as e:
            logger.trace(f'Retrying {command} after exception {e}')
            self.commands.append(command)

    def num_outstanding_orders(self):
        return len(self.all_own_units.filter(lambda unit: len(unit.orders) > 0))

    def cancel_impossible_orders(self):
        def _cancel_impossible_order(self, unit: Unit, order: UnitOrder):
            # If the order is to over garrison a bunker that is full, cancel it
            if order.ability.id == AbilityId.MOVE and isinstance(order.target, int):
                bunker = self.structures.by_tag(order.target)
                
                if (bunker.cargo_left < 1 and unit.type_id == UnitTypeId.MARINE) or \
                   (bunker.cargo_left < 2 and unit.type_id == UnitTypeId.MARAUDER):
                    logger.trace(f'Canceling impossible order {order} on {unit}')
                    unit.stop()

        for unit in self.all_own_units:
            for order in unit.orders:
                _cancel_impossible_order(self, unit, order)

    @property
    def time_survived(self):
        if not self.setup_done:
            return 0
        return self.time - self.starting_game_time

    async def on_start(self):
        self.starting_gas = self.vespene
        self.starting_minerals = self.minerals

    async def on_setup_step(self, iteration):
        # While commands are available, consume them one by one
        if len(self.commands) != 0:
            self.consume_command()
        else:
            # Once all commands are consumed, we can start the game if 
            # everything is in position
            if self.num_outstanding_orders() == 0:
                await self.on_game_ready()
            else:
                # Some units cannot complete their orders, cancel them
                self.cancel_impossible_orders()

        if self.time > self.ready_time_limit:
            logger.warning("Ready time limit exceeded, starting game anyway")
            await self.on_game_ready()


    async def on_game_ready(self):
        # Tell all siege tanks to transform into siege mode
        for unit in self.all_own_units.of_type(UnitTypeId.SIEGETANK):
                unit(AbilityId.SIEGEMODE_SIEGEMODE)
        self.setup_done = True
        self.starting_game_time = self.time
        logger.info("Evaluating Now ...")
        await self.chat_send("Ready!")

    async def on_after_ready_step(self, iteration):
        # We have been destroyed
        if not self.townhalls.exists:
            await self.chat_send("Survived " + str(self.time) + " seconds")
            await self.client.leave()
        
        # win cond. Last wave spawns at roughly 108 seconds (1.8 minutes)
        # in testing: final wave actually spawns around 56-58
        if self.time_survived > self.win_timeout:
            await self.client.leave()


    async def on_step(self, iteration):
        if not self.setup_done:
            await self.on_setup_step(iteration)
        else:
            await self.on_after_ready_step(iteration)

    @property
    def gas_used(self):
        return self.starting_gas - self.vespene
    
    @property
    def minerals_used(self):
        return self.starting_minerals - self.minerals


    async def on_building_construction_complete(self, unit: Unit):
        p = Point2([unit.position.x - 0.5, unit.position.y - 0.5])
        if p in self.bunkers:
            self.commands.extend(self.bunkers[p])
            return await super().on_building_construction_complete(unit)


def evaluate(
        genotype: gp.Gene, 
        realtime: bool,
        win_timeout: float,
        ready_time_limit: float
    ) -> gp.Fitness:

    commands = cmd.build_command_queue(genotype, Rectangle(40, 40, 16, 16))
    bot = Evaluategenotype(commands, 
        win_timeout,
        ready_time_limit
    )
    game_map = maps.get("Siege")

    logger.info(f"Map Full Path  : {game_map.path}")
    logger.info(f"chr: {genotype}")
    # plot_gene(gene, "gene.png")
    # res just holds a Result enum value of either Victory or Defeat
    run_game(
        game_map,
        [Bot(Race.Terran, bot, name="EvaluationBot")],
        realtime=realtime,
    )

    fitness: Fitness = Fitness(bot.time_survived, bot.minerals_used, bot.gas_used)

    if not bot.setup_done:
        logger.error(f"Timeout before setup was done {genotype}")
    return fitness


def run_human_playable():
    game_map = maps.get("Siege")
    run_game(
        game_map,
        [Human(Race.Terran)],
        realtime=True,
    )
