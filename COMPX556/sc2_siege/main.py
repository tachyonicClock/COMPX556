from email.errors import HeaderMissingRequiredValue
from os import system
import typing as t
from wsgiref.util import setup_testing_defaults
from xmlrpc.client import Boolean
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Race
from sc2.main import run_game
from sc2.player import Bot
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
from sc2.unit import Unit
import gp
from gp.plot_chromosome import plot_gene
from gp.rectangle import Rectangle
import sc2_evaluator.command as cmd
from loguru import logger
from sc2.ids.ability_id import AbilityId


# from sc2_evaluator.const import BARRACKS_UNIT_MAPPING, FACTORY_UNIT_MAPPING, UNIT_MAPPING


class EvaluateChromosome(BotAI):

    placed_units: t.Set[int] = set()
    commands: t.List[cmd.Command]
    setup_done: Boolean = False
    game_over: Boolean = False
    score: float = -1
    bunkers = {}

    starting_minerals: int = -1
    starting_gas: int = -1

    minerals_used: int = -1
    gas_used: int = -1

    starting_game_time: int = -1

    def __init__(self, commands: t.List[cmd.Command]) -> None:
        super().__init__()
        self.commands = commands

    def consume_command(self, command: cmd.Command) -> t.List[cmd.Command]:
        # do_now: cmd.Command = self.commands.pop()
        logger.info(f'Performing command {command}')
        try:
            if isinstance(command, cmd.TrainUnit):
                command.train(self)
                logger.info(
                    f'Training  {command.unit.name} in {command.building.name}')
            elif isinstance(command, cmd.PlaceUnit):
                tag = command.place(self, self.placed_units)
                self.placed_units.add(tag)
                logger.info(
                    f'Placing   {command.unit.name} at {command.location}')
            elif isinstance(command, cmd.BuildStructure):
                command.build(self)
                self.bunkers[command.location] = command.after
                logger.info(
                    f'Building  {command.unit.name} at {command.location}')
                return

            self.commands.extend(command.after)

        except cmd.CommandFailed as e:
            logger.info(f'### cmd failed with exception {e}')
            self.commands.append(command)

    def num_outstanding_orders(self):
        units = self.all_own_units
        return len(units.filter(lambda unit: len(unit.orders) > 0))

    def time_dif(self):
        return self.time - self.starting_game_time

    async def on_step(self, iteration):
        logger.info(f'Number of enemy units: {len(self.all_enemy_units)}')
        # init starting resources counts for end-of-game calculations
        if self.starting_gas < 0 and self.starting_minerals < 0:
            self.starting_gas = self.vespene
            self.starting_minerals = self.minerals
        if len(self.commands) != 0:
            command = self.commands.pop()
            self.consume_command(command)
        elif self.num_outstanding_orders() == 0 and not self.setup_done:
            # transform all siege tanks
            for unit in self.all_own_units.filter(lambda unit: unit.type_id == UnitTypeId.SIEGETANK):
                unit(AbilityId.SIEGEMODE_SIEGEMODE)
            await self.chat_send("Ready!")
            self.setup_done = True
            self.starting_game_time = self.time

        if not self.townhalls and not self.game_over:
            self.game_over = True

            await self.chat_send("Survived " + str(self.time) + " seconds")
            logger.info(f"Survived {str(self.time)} seconds")
            self.score = self.time
            await self.client.leave()

        if self.time_dif() > 1:
            logger.info(
                f'Time since ready: {self.time_dif()}')

        # win cond. Last wave spawns at roughly 108 seconds (1.8 minutes) and base enemy structures/units is 11
        # in testing: final wave actually spawns around 56-58 seconds in, as reported by time_dif(). gotta test with real_time true and some other stuff to figure out what i need.
        if self.time_dif() > 110 and len(self.all_enemy_units) <= 11 and not self.game_over:
            self.gas_used = self.starting_gas - self.vespene
            self.minerals_used = self.starting_minerals - self.minerals
            self.game_over = True
            self.score = self.time
            await self.client.leave()

    async def on_building_construction_complete(self, unit: Unit):
        p = Point2([unit.position.x - 0.5, unit.position.y - 0.5])
        self.commands.extend(self.bunkers[p])
        return await super().on_building_construction_complete(unit)


def main():
    # gene = gp.Quadrant([
    #     gp.Quadrant(
    #         [gp.Bunker(
    #             [gp.Marine(), gp.Marine(), gp.Marine(), gp.Marine()]
    #         ), gp.Marine(), gp.Marine(), gp.Marine()],
    #     ),
    #     gp.Marine(),
    #     gp.Marauder(),
    #     gp.SiegeTank()
    # ])

    # gene = gp.Bunker(
    #     [gp.Marine(), gp.Marine(), gp.Marine(), gp.Marine()]
    # )
    gene = gp.initialise_chromosome(3)

    commands = cmd.build_command_queue(gene, Rectangle(40, 40, 16, 16))
    bot = EvaluateChromosome(commands)
    game_map = maps.get("Siege")

    logger.info(f'Evaluating Gene: {gene}')
    logger.info(f"Map Full Path  : {game_map.path}")
    plot_gene(gene, "gene.png")
    # res just holds a Result enum value of either Victory or Defeat
    res = run_game(
        game_map,
        [Bot(Race.Terran, bot, name="EvaluationBot")],
        realtime=True,
    )
    logger.info(f'Gametime (score): {bot.score}')
    logger.info(f'Vespene gas used: {bot.gas_used}')
    logger.info(f'Minerals used:    {bot.minerals_used}')
    # bot.score: time in seconds the bot survived
    # bot.gas_used: amount of gas resource used
    # bot.minerals_used: amount of minerals resource used


if __name__ == "__main__":
    main()
