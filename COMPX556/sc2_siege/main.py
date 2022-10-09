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


# from sc2_evaluator.const import BARRACKS_UNIT_MAPPING, FACTORY_UNIT_MAPPING, UNIT_MAPPING


class EvaluateChromosome(BotAI):

    placed_units: t.Set[int] = set()
    commands: t.List[cmd.Command]
    setup_done: Boolean = False
    game_over: Boolean = False
    score: float = -1

    def __init__(self, commands: t.List[cmd.Command]) -> None:
        super().__init__()
        self.commands = commands

    def consume_command(self) -> bool:
        do_now: cmd.Command = self.commands.pop()
        try:
            if isinstance(do_now, cmd.TrainUnit):
                do_now.train(self)
                logger.info(
                    f'Training  {do_now.unit.name} in {do_now.building.name}')
            elif isinstance(do_now, cmd.PlaceUnit):
                tag = do_now.place(self, self.placed_units)
                self.placed_units.add(tag)
                logger.info(
                    f'Placing   {do_now.unit.name} at {do_now.location}')
            elif isinstance(do_now, cmd.BuildStructure):
                do_now.build(self)
                logger.info(
                    f'Building  {do_now.unit.name} at {do_now.location}')

            self.commands.extend(do_now.after)

        except cmd.CommandFailed as e:
            self.commands.append(do_now)

    async def on_step(self, iteration):

        if len(self.commands) != 0:
            self.consume_command()
        elif not self.setup_done:
            await self.chat_send("Ready!")
            self.setup_done = True
        if not self.townhalls and not self.game_over:
            self.game_over = True

            await self.chat_send("Survived " + str(self.time) + " seconds")
            logger.info(f"Survived {str(self.time)} seconds")
            self.score = self.time
            await self.client.leave()


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
    gene = gp.initialise_chromosome(2)

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


if __name__ == "__main__":
    main()
