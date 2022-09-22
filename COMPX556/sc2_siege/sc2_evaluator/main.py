import typing as t
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Race
from sc2.main import run_game
from sc2.player import Bot

class EvaluateChromosome(BotAI):

    def __init__(self) -> None:
        super().__init__()

    async def on_step(self, iteration):
        pass

def main():
    run_game(
        maps.get("Siege_0"),
        [Bot(Race.Terran, EvaluateChromosome(), name="CheeseCannon")],
        realtime=True,
    )


if __name__ == "__main__":
    main()