from axelrod.action import Action
from axelrod.strategies import Random as axlRandom
from axelrodVoice import Player

# Does xY
class Random(axlRandom, Player):
    name = "RAND"
    def __init__(self, p: float = 0.5) -> None:
        super().__init__(p)

    def strategy_voice(self, opponent: Player) -> Action:
        return self.strategy(opponent)


# Does cX
class RandomCX(axlRandom, Player):
    name = "RANDcx"
    def __init__(self, p: float = 0.5) -> None:
        super().__init__(p)
    def strategy_voice(self, opponent: Player) -> Action:
        return Action.C
# Does xX
class RandomXX(axlRandom, Player):
    name = "RANDxx"
    def __init__(self, p: float = 0.5) -> None:
        super().__init__(p)
    def strategy_voice(self, opponent: Player) -> Action:
        return axlRandom.strategy(self, opponent)
    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]