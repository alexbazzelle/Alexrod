from axelrod.action import Action
from axelrod.strategies import FirstBySteinAndRapoport as axlSteinAndRapoport

from axelrodVoice import Player
from axelrodVoice.strategies.titfortat import TitForTat, FaceValue

from scipy.stats import chisquare





"""
TIFT, but lies if the opponent is predicted to be random, which is checked every 15 turns
"""
class SteinAndRapoport(axlSteinAndRapoport, Player):
    name = "STRA"

    def __init__(self, alpha: float = 0.05) -> None:
        super().__init__()
        self.alpha = alpha
        self.opponent_is_random = False

    # since the original had a @FinalTransformer
    # I need to do this so the name is clean
    def __repr__(self):
        return self.name

    def strategy_voice(self, opponent : Player) -> Action:
        round_number = len(self.history) + 1

        if round_number < 5: # first 4 moves, say "C"
            return Action.C
        
        elif round_number < 15: #  moves 5-14, play tit for tat
            return TitForTat.strategy_voice(self, opponent)
        
        if self.opponent_is_random: # if opponent is predicted to be random, play liar ["C", D]
            return Action.C
        else:  # otherwise, play tit for tat
            return TitForTat.strategy_voice(self, opponent)
    

    def strategy(self, opponent: Player) -> Action:
        round_number = len(self.history) + 1

        if round_number < 5: # first 4 moves, do C
            return Action.C
        
        elif round_number < 15: # moves 5-14, play tit for tat
            return TitForTat.strategy(self, opponent)

        if round_number % 15 == 0: # every 15 rounds, check if random
            # specifically, this test if vC = vD = cC = cD. each should be ~50
            # if voice is always random and choice is mostly C, then it'd be [ 50 50 75 25 ] which fails
            p_value = chisquare(
                [opponent.history.cooperations, opponent.history.defections,
                 opponent.history_voice.cooperations, opponent.history_voice.defections]
            ).pvalue
            self.opponent_is_random = p_value >= self.alpha

        if self.opponent_is_random: # if opponent is predicted to be random, play liar ["C", D]
            return Action.D 
        else:  # otherwise, play tit for tat
            return TitForTat.strategy(self, opponent)
        


# Same as above, but TitForTat is replaced by FaceValue
class SteinAndRapoportFV(axlSteinAndRapoport, Player):
    name = "STRAfv"

    def __init__(self, alpha: float = 0.05) -> None:
        """
        Parameters
        ----------
        alpha: float
            The significant level of p-value from chi-squared test with
            alpha == 0.05 by default.
        """
        super().__init__()
        self.alpha = alpha
        self.opponent_is_random = False

    def __repr__(self):
        return self.name

    def strategy_voice(self, opponent : Player) -> Action:
        round_number = len(self.history) + 1

        if round_number < 5: # first 4 moves, say "C"
            return Action.C
        
        elif round_number < 15: #  moves 5-14, play tit for tat
            return FaceValue.strategy_voice(self, opponent)
        
        if self.opponent_is_random: # if opponent is predicted to be random, play liar ["C", D]
            return Action.C
        else:  # otherwise, play tit for tat
            return FaceValue.strategy_voice(self, opponent)
    

    def strategy(self, opponent: Player) -> Action:
        round_number = len(self.history) + 1

        if round_number < 5: # first 4 moves, do C
            return Action.C
        
        elif round_number < 15: # moves 5-14, play tit for tat
            return FaceValue.strategy(self, opponent)

        if round_number % 15 == 0: # every 15 rounds, check if random
            p_value = chisquare( # ADDED VOICE HISTORY. IDK IF I DID IT RIGHT THO
                [opponent.history.cooperations, opponent.history.defections,
                 opponent.history_voice.cooperations, opponent.history_voice.defections]
            ).pvalue
            self.opponent_is_random = p_value >= self.alpha

        if self.opponent_is_random: # if opponent is predicted to be random, play liar ["C", D]
            return Action.D 
        else:  # otherwise, play tit for tat
            return FaceValue.strategy(self, opponent)


class SteinAndRapoportCX(axlSteinAndRapoport, Player):
    name = "STRAcx"

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self):
        return self.name

    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C


class SteinAndRapoportXX(axlSteinAndRapoport, Player):
    name = "STRAxx"

    def __init__(self) -> None:
        super().__init__()
    def __repr__(self):
        return self.name
    def strategy_voice(self, opponent: Player) -> Action:
        return axlSteinAndRapoport.strategy(self, opponent)
    def strategy(self, opponent: Player) -> Action:
        return self.history_voice[-1]