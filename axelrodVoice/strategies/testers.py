from axelrod.action import Action
from axelrodVoice import Player
from axelrod.strategies import Random as axlRandom


"""
Strategies solely for testing.
These either defect honestly or lie...
    on turns ending in 7 (once every 10)
    on turns ending in 7 or 8 (twice every 10)
    on turns ending in 4 or 7 (twice spaced out every 10)
    with P(D) = 15%
    with P(D) = 30%
    with P(D) = 70%
"""

class TestD7(Player):
    name = "_d7"
    def strategy_voice(self, opponent: Player) -> Action:
        if len(self.history)+1 % 10 == 7: return Action.D
        return Action.C
    def strategy(self, opponent: Player) -> Action:
        return self.history_voice[-1]
class TestD78(Player):
    name = "_d78"
    def strategy_voice(self, opponent: Player) -> Action:
        if len(self.history)+1 % 10 in [7,8]: return Action.D
        return Action.C
    def strategy(self, opponent: Player) -> Action:
        return self.history_voice[-1]
class TestD47(Player):
    name = "_d47"
    def strategy_voice(self, opponent: Player) -> Action:
        if len(self.history)+1 % 10 in [4,7]: return Action.D
        return Action.C
    def strategy(self, opponent: Player) -> Action:
        return self.history_voice[-1]

class TestDp15(axlRandom,Player):
    name = "_dp15"
    def strategy_voice(self, opponent: Player) -> Action:
        return self._random.random_choice(1 - 0.15)
    def strategy(self, opponent: Player) -> Action:
        return self.history_voice[-1]
class TestDp30(axlRandom,Player):
    name = "_dp30"
    def strategy_voice(self, opponent: Player) -> Action:
        return self._random.random_choice(1 - 0.30)
    def strategy(self, opponent: Player) -> Action:
        return self.history_voice[-1]
class TestDp70(axlRandom,Player):
    name = "_dp70"
    def strategy_voice(self, opponent: Player) -> Action:
        return self._random.random_choice(1 - 0.70)
    def strategy(self, opponent: Player) -> Action:
        return self.history_voice[-1]


class TestL7(Player):
    name = "_l7"
    def strategy_voice(self, opponent: Player) -> Action:
        return Action.C
    def strategy(self, opponent: Player) -> Action:
        if len(self.history) + 1 % 10 == 7: return Action.D
        return Action.C
class TestL78(Player):
    name = "_l78"
    def strategy_voice(self, opponent: Player) -> Action:
        return Action.C
    def strategy(self, opponent: Player) -> Action:
        if len(self.history) + 1 % 10 in [7, 8]: return Action.D
        return Action.C
class TestL47(Player):
    name = "_l47"
    def strategy_voice(self, opponent: Player) -> Action:
        return Action.C
    def strategy(self, opponent: Player) -> Action:
        if len(self.history) + 1 % 10 in [4, 7]: return Action.D
        return Action.C

class TestLp15(axlRandom,Player):
    name = "_lp15"
    def strategy_voice(self, opponent: Player) -> Action:
        return Action.C
    def strategy(self, opponent: Player) -> Action:
        return self._random.random_choice(1 - 0.15)
class TestLp30(axlRandom,Player):
    name = "_lp30"
    def strategy_voice(self, opponent: Player) -> Action:
        return Action.C
    def strategy(self, opponent: Player) -> Action:
        return self._random.random_choice(1 - 0.30)
class TestLp70(axlRandom,Player):
    name = "_lp70"
    def strategy_voice(self, opponent: Player) -> Action:
        return Action.C
    def strategy(self, opponent: Player) -> Action:
        return self._random.random_choice(1 - 0.70)