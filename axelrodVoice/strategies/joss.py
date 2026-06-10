from axelrod.action import Action
from axelrod.strategies import FirstByJoss as axlJoss

from axelrodVoice import Player

# interesting note: when playing against TitForTat-based strategies, Joss starts alternating


"""
Joss Liar:
If opponent does cD, then P(cD) = .90 and P(dD) = .90
If opponent does cC, then P(cD) = .90 and P(cC) = .90
"""
class JossLiar(axlJoss, Player):
    name = "JOSS"

    def strategy_voice(self, opponent: Player) -> Action:
        if not opponent.history:
            return Action.C

        if opponent.history_tuples[-1] == (Action.C, Action.D):
            return self._random.random_choice(9 / 10)
        else:
            return opponent.history[-1]

    def strategy(self, opponent: Player) -> Action:
        return axlJoss.strategy(self, opponent)



"""
Joss Classic:
Ignores Voice
"""
class JossClassic(axlJoss, Player):
    name = "JOSSog"

    def strategy_voice(self, opponent : Player) -> Action:
        if not opponent.history: return Action.C
        else: return opponent.history[-1]

    def strategy(self, opponent : Player) -> Action:
        return axlJoss.strategy(self, opponent)


class JossCX(axlJoss, Player):
    name = "JOSScx"
    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C
    def strategy(self, opponent : Player) -> Action:
        return axlJoss.strategy(self, opponent)



# Conceptually, this one does not make sense.
# BECAUSE Joss relies on the SURPRISE of 10% defection
class JossXX(axlJoss, Player):
    name = "JOSSxx"
    def strategy_voice(self, opponent : Player) -> Action:
        return axlJoss.strategy(self, opponent)
    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]