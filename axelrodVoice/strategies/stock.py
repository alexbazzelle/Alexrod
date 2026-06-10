from axelrod.action import Action
from axelrod.strategies import Defector as axlDefector
from axelrod.strategies import Cooperator as axlCooperator
from axelrod.strategies import Alternator as axlAlternator
from axelrodVoice import Player

"""
These are all of the boring, simply strategies.
"""

class Liar(axlDefector, Player): # cD
    name = "LIAR"
    def strategy_voice(self, opponent: Player) -> Action:
        return Action.C

class Defector(axlDefector, Player): # dD
    name = "DEFT"
    def strategy_voice(self, opponent: Player) -> Action:
        return Action.D

class Cooperator(axlCooperator, Player): # cC
    name = "COOP"
    def strategy_voice(self, opponent: Player) -> Action:
        return Action.C

class AllBarkNoBite(axlCooperator, Player): # dC
    name = "ABNB"
    def strategy_voice(self, opponent: Player) -> Action:
        return Action.D


class Alternator(axlAlternator, Player): # cC to dD
    name = "ALTRxx"
    def strategy_voice(self, opponent: Player) -> Action:
        if len(self.history_voice) == 0: return Action.C
        else: return Action.flip( self.history_voice[-1] )

class AlternatorCX(axlAlternator, Player): # cC to cD
    name = "ALTRcx"
    def strategy_voice(self, opponent: Player) -> Action:
        return Action.C