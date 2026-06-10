from axelrod.action import Action
from axelrod.strategies import FirstByTullock as axlTullock

from axelrodVoice import Player



"""
Does cC for the first 11 rounds.
Defects 10% more than the opponent has defected
    When defecting, lie 10% more than the opponent has lied
"""
class Tullock(axlTullock, Player):
    name = "TULL"

    def __init__(self) -> None:
        super().__init__()
        self.choice_action = Action.C

    def strategy_voice(self, opponent : Player) -> Action:
        # cooperate honestly for the first 11 rounds
        if not self.history_voice or len(self.history) < 11:
            return Action.C

        # find (dis-)honest defection count
        op_honest_defection_count = 0
        op_dishonest_defection_count = 0
        for i in range(10):
            if opponent.history[-i] == Action.D:
                if opponent.history_voice[-i] == Action.C:
                    op_honest_defection_count += 1
                else:
                    op_dishonest_defection_count += 1

        # plan to defect 10% more than opponent
        op_defection_count = op_honest_defection_count + op_dishonest_defection_count
        op_defection_rate = op_defection_count / 10
        self.choice_action = self._random.random_choice( max(0, 0.9 - op_defection_rate) )

        # if defecting, lie 10% more than opponent
        if self.choice_action == Action.D:
            if op_defection_count == 0: op_lie_rate = 0
            else: op_lie_rate = op_dishonest_defection_count / op_defection_count
            return self._random.random_choice( min(1, op_lie_rate+0.1) )

        # otherwise, honest cooperation
        return Action.C

    def strategy(self, opponent : Player) -> Action:
        # decided in voice
        return self.choice_action

"""
Says c 10% than opponent said c.
Does C 10% less than opponent did C.
"""
class TullockIndependent(axlTullock, Player):
    name = "TULLnd"

    def strategy_voice(self, opponent : Player) -> Action:
        # say "cooperate" for the first 11 rounds
        if not self.history_voice or len(self.history) < 11:
            return Action.C

        # find opponent's VOICE cooperation rate
        coop_count = opponent.history_voice[-10:].count(Action.C)
        op_coop_rate = coop_count / 10

        # say "cooperate" 10% less than opponent
        return self._random.random_choice( max(0, op_coop_rate - 0.1) )

    def strategy(self, opponent : Player) -> Action:
        # cooperate for the first 11 rounds
        if not self.history or len(self.history) < 11:
            return Action.C

        # find opponent's CHOICE cooperation rate
        coop_count = opponent.history[-10:].count(Action.C)
        op_coop_rate = coop_count / 10

        # pick cooperate 10% less than opponent
        return self._random.random_choice( max(0, op_coop_rate - 0.1) )

"""
Cooperates 10% less than the opponent, but is always honest.
"""
class TullockClassic(axlTullock, Player):
    name = "TULLog"

    def strategy_voice(self, opponent : Player) -> Action:
        # cooperate honestly for the first 11 rounds
        if not self.history_voice or len(self.history) < 11:
            return Action.C

        # find opponent's cooperation rate
        coop_count = opponent.history[-10:].count(Action.C)
        op_coop_rate = coop_count / 10

        # cooperate 10% less than opponent
        return self._random.random_choice( max(0, op_coop_rate - 0.1) )

    def strategy(self, opponent : Player) -> Action:
        # do whatever you said you would.
        return self.history_voice[-1]



class TullockCX(axlTullock, Player):
    name = "TULLcx"
    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C

class TullockXX(axlTullock, Player):
    name = "TULLxx"
    def strategy_voice(self, opponent : Player) -> Action:
        return axlTullock.strategy(self, opponent)
    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]