from axelrod.action import Action
from axelrod.strategies import FirstByFeld as axlFeld

from axelrodVoice import Player

"""
Plays TIFTxx, but replaces intended cooperations with defections
FELD   : 100% honest -> 50% lies over 200 turns. Builds trust.
"""
class FeldHonestToLiar(axlFeld, Player):
    name = "FELDhl"

    def __init__(self) -> None:
        super().__init__()
        self.coop_prob = 1.0
        self.lie_prob = 0.0
        self.choice_action = Action.C

    def strategy_voice(self, opponent: Player) -> Action:
        if not self.history: return Action.C

        # update probabilities          x is the round number
        self.coop_prob -= 0.5 / 200  # c(x) = (-0.5/200)x + 1,   c(0)=1, c(200)=0.5
        self.lie_prob  += 0.5 / 200  # l(x) = (0.5/200)x,         l(0)=1, l(200)=0.5

        # tit for tat defection
        if opponent.history[-1] == Action.D:
            self.choice_action = Action.D
            return Action.D

        # decide if I will defect when I'm supposed to cooperate
        self.choice_action = self._random.random_choice(max(self.coop_prob, 0.5))

        # if I am defecting, decide if I will lie about it
        if self.choice_action == Action.D:
            return self._random.random_choice(min(self.lie_prob, 0.5))

        return Action.C

    def strategy(self, opponent: Player) -> Action:
        if self.history_voice[-1] == Action.D:
            return Action.D
        else:
            return self.choice_action

"""
Plays TIFTxx, but replaces intended cooperations with defections
FELDlh : 100% lies -> 50% lies over 200 turns. Sneaky defections.
"""
class FeldLiarToHonest(axlFeld, Player):
    name = "FELD"

    def __init__(self) -> None:
        super().__init__()
        self.coop_prob = 1.0
        self.lie_prob = 1.0
        self.choice_action = Action.C

    def strategy_voice(self, opponent : Player) -> Action:
        if not self.history: return Action.C

        # update probabilities          x is the round number
        self.coop_prob -= 0.5 / 200 # c(x) = (-0.5/200)x + 1,   c(0)=1, c(200)=0.5
        self.lie_prob  -= 0.5 / 200 # l(x) = (-0.5/200)x + 1,   l(0)=1, l(200)=0.5

        # tit for tat defection
        if opponent.history[-1] == Action.D:
            self.choice_action = Action.D
            return Action.D

        # decide if I will defect when I'm supposed to cooperate
        self.choice_action = self._random.random_choice( max( self.coop_prob, 0.5 ) )

        # if I am defecting, decide if I will lie about it
        if self.choice_action == Action.D:
            return self._random.random_choice( max( self.lie_prob, 0.5 ) )

        return Action.C


    def strategy(self, opponent : Player) -> Action:
        if self.history_voice[-1] == Action.D:
            return Action.D
        else: return self.choice_action


class FeldXX(axlFeld, Player):
    name = "FELDxx"
    def strategy_voice(self, opponent : Player) -> Action:
        return axlFeld.strategy(self, opponent)
    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]

class FeldCX(axlFeld, Player):
    name = "FELDcx"
    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C