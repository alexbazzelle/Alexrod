from axelrod.action import Action
from axelrod.strategies import FirstByNydegger as axlNydegger

from axelrodVoice import Player

"""
im gonna be so real.
i've tried to understand this.
i've got nothing.
"""
"""
class Nydegger(axlNydegger, Player):
    name = "Nydegger"

    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C
    def strategy(self, opponent : Player) -> Action:
        return Action.C
"""

class NydeggerXX(axlNydegger, Player):
    name = "NYDGxx"
    def strategy_voice(self, opponent : Player) -> Action:
        return axlNydegger.strategy(self, opponent)
    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]

class NydeggerCX(axlNydegger, Player):
    name = "NYDGcx"
    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C