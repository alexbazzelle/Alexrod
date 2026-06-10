from axelrod.action import Action
from axelrod.strategies import Grudger as axlGrudger

from axelrodVoice import Player



"""
Does cC until provoked.
If opponent does dD, then do dD until further provoked.
If opponent does cD, then do cD indefinitely.
"""
class Grudger(axlGrudger, Player):
    name = "GRUD"

    def strategy_voice(self, opponent : Player) -> Action:
        if not opponent.history: return Action.C
        if (Action.C, Action.D) in opponent.history_tuples: return Action.C
        if (Action.D, Action.D) in opponent.history_tuples: return Action.D
        else: return Action.C

    def strategy(self, opponent : Player) -> Action:
        # if the opponent said "D" or has ever defected, I defect
        if opponent.history.defections or opponent.history_voice[-1]==Action.D:
            return Action.D
        else: return Action.C



class GrudgerXX(axlGrudger, Player):
    name = "GRUDxx"
    def strategy_voice(self, opponent : Player) -> Action:
        return axlGrudger.strategy(opponent)
    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]

class GrudgerCX(axlGrudger, Player):
    name = "GRUDcx"
    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C