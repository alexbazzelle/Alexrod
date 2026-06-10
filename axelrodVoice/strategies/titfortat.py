from axelrod.action import Action
from axelrod.strategies import TitForTat as axlTitForTat
from axelrod.strategies import TitFor2Tats as axlTitFor2Tats

from axelrodVoice import Player

# echoes rounds
class TitForTat(axlTitForTat, Player):
    name = "TIFT"
    def strategy_voice(self, opponent):
        if not opponent.history: return Action.C
        return opponent.history_voice[-1]

# echoes phases
class FaceValue(axlTitForTat, Player):
    name = "FACE"
    def strategy_voice(self, opponent: Player) -> Action:
        if len(self.history) == 0: return Action.C
        else: return opponent.history[-1]
    def strategy(self, opponent: Player) -> Action:
        return opponent.history_voice[-1]



class TitFor2Tats(axlTitFor2Tats, Player):
    name = "TFTT"
    def strategy_voice(self, opponent):
        if len(self.history) > 2 and opponent.history_voice[-2:] != [Action.C, Action.C]:
            return Action.D
        return Action.C

class TitForTatXX(axlTitForTat, Player):
    name = "TIFTxx"
    def strategy_voice(self, opponent : Player) -> Action:
        return axlTitForTat.strategy(self,opponent)
    
class TitForTatCX(axlTitForTat, Player):
    name = "TIFTcx"
    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C


