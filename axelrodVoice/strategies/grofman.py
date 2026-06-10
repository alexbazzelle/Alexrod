from axelrod.action import Action
from axelrod.strategies import FirstByGrofman as axlGrofman

from axelrodVoice import Player


"""
If CC, then cooperate.
If DD, then P(cC)=2/7, P(cD)=5/7
If sucker, then P(cC)=4/49, P(cD)=10/49, P(dD)=35/49
If temptation, then P(c)=2/7. If cc or dd, then P(C)=5/7. If cd or dc, P(C)=2/7


Alternatively,

CASE 1: CC or DD
P(c)=1. P(C|d_op)=2/7. P(C|c_op) = 1

CASE 2: CD
P(cC) = 10/49
P(cD) = 25/49
P(dD) = 14/49

CASE 3: DC
P(c) = 2/7
P(C | xx) = 5/7
P(C | xy) = 2/7

"""
class Grofman(axlGrofman, Player):

    name = "GROF"
    def __init__(self):
        super().__init__()
        self.choiceState = 0

    def strategy_voice(self, opponent : Player) -> Action:
        if not self.history: return Action.C # first round

        # matched opponent [C, C]
        if self.history[-1] == opponent.history[-1]:
            self.choiceState = 1
            return Action.C

        # I lost [C, D]
        if (self.history[-1] == Action.C) and (opponent.history[-1] == Action.D):
            self.choiceState = 2
            return self._random.random_choice(5 / 7) # probably lie

        # I won [D, C]
        if (self.history[-1] == Action.D) and (opponent.history[-1] == Action.C):
            self.choiceState = 3
            return self._random.random_choice(2 / 7) # probably say "defect"

        # backup
        return Action.C


    def strategy(self, opponent : Player) -> Action:
        match self.choiceState:
            case 1: # (matched last round) if op says "D", then probably do D. otherwise, I do C.
                if opponent.history_voice[-1] == Action.D:
                    return self._random.random_choice(2 / 7) # probably D
                else: return Action.C
            case 2: # (op beat me last round) if I said "C", then probably do D. otherwise, I do D.
                if self.history_voice[-1] == Action.C:
                    return self._random.random_choice(2 / 7) # probably D
                else: return Action.D
            case 3: # (i beat op last round) if we said the same thing, I probably do C. otherwise, I probably do D
                if self.history_voice[-1] == opponent.history_voice[-1]:
                    return self._random.random_choice(5 / 7)  # probably C
                else: return self._random.random_choice(2 / 7)  # probably D
        # otherwise, do C
        return Action.C



class GrofmanXX(axlGrofman, Player):
    name = "GROFxx"

    def strategy_voice(self, opponent : Player) -> Action:
        return axlGrofman.strategy(self, opponent)

    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]

class GrofmanCX(axlGrofman, Player):
    name = "GROFcx"

    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C

    def strategy(self, opponent : Player) -> Action:
        return axlGrofman.strategy(self, opponent)