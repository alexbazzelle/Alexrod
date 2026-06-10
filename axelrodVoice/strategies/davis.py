from axelrod.action import Action
from axelrod.strategies import FirstByDavis as axlDavis
from axelrodVoice import Player
from axelrodVoice.strategies.grudger import Grudger

"""
Honestly cooperates for 10 rounds, then plays Grudger
"""
class Davis(axlDavis, Player):
    name = "DAVI"

    def strategy_voice(self, opponent : Player) -> Action:
        if not self.history: return Action.C
        if len(self.history) < 10: return Action.C
        else: return Grudger.strategy_voice(self, opponent)

    def strategy(self, opponent : Player) -> Action:
        if not self.history: return Action.C
        if len(self.history) < 10: return Action.C
        else: return Grudger.strategy(self, opponent)



class DavisXX(axlDavis, Player):
    name = "DAVIxx"
    def strategy_voice(self, opponent : Player) -> Action:
        return axlDavis.strategy(self, opponent)
    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]

class DavisCX(axlDavis, Player):
    name = "DAVIcx"
    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C