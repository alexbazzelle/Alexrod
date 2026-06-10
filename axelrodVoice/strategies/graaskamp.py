from axelrod.action import Action
from axelrod.strategies import FirstByGraaskamp as axlGraaskamp

from axelrodVoice import Player
from axelrodVoice.strategies.titfortat import TitForTat

C, D = Action.C, Action.D

from scipy.stats import chisquare


"""
Rounds 1-50: TitForTat
Round 51: ["D", D] for reaction to honest defection
Round 52: ["C", C] to reset
Round 53: ["C", D] for reaction to lying
Round 54: ["C", C] to reset
Rounds 55-59: TitForTat
Round 60:
Check for Random/TitForTat/FaceValue/Self
- if Random or FaceValue: ["C", D]
- if TatForTat or Clone: ["C", C]
- else: ["C", C], but every 5 to 15 rounds do ["C", D]
"""
class Graaskamp(axlGraaskamp, Player):
    name = "GRAS"

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
        self.opponent_is_titfortat = False
        self.opponent_is_facevalue = False
        self.opponent_is_clone = True
        self.next_random_defection_turn = None  # type: Optional[int]


    def strategy_voice(self, opponent : Player) -> Action:
        round_number = len(self.history_voice) + 1

        # check for opponent on round 60
        if round_number == 60:
            opponent_cooperated = True
            for i in range(0,50):
                if (opponent.history_voice[i] != C) or (opponent.history[i] != C):
                    opponent_cooperated = False

            if opponent_cooperated and (opponent.history_voice[50:59] == [C, D, C, D, C, C, C, C, C]):
                if (opponent.history[50:59] == [C, D, C, D, C, C, C, C, C]):
                    self.opponent_is_titfortat = True
                elif (opponent.history[50:59] == [D, C, C, C, C, C, C, C, C]):
                    self.opponent_is_facevalue = True
            elif (opponent.history == self.history) and (opponent.history_voice == self.history_voice):
                self.opponent_is_clone = True
            elif chisquare([opponent.history.cooperations, opponent.history.defections]).pvalue > self.alpha:
                self.opponent_is_random = True


        if round_number < 50: # rounds [0,49]
            return TitForTat.strategy_voice(self, opponent)
        elif round_number < 55: # rounds [50,54]
            return [D, C, C, C][round_number - 51]
        elif round_number < 60: # rounds [55, 59]
            return TitForTat.strategy_voice(self, opponent)
        elif self.opponent_is_random or self.opponent_is_facevalue:
            return C
        elif self.opponent_is_titfortat or self.opponent_is_clone:
            return TitForTat.strategy_voice(self, opponent)
        else: return TitForTat.strategy_voice(self, opponent)


    def strategy(self, opponent : Player) -> Action:
        round_number = len(self.history) + 1

        if round_number < 50: # rounds [0,49] do titfortat
            return TitForTat.strategy(self, opponent)
        elif round_number < 55: # rounds [50,54] do D C D C
            return [D, C, D, C][round_number - 51]
        elif round_number < 60: # rounds [55, 59] do titfortat
            return TitForTat.strategy(self, opponent)
        elif self.opponent_is_random or self.opponent_is_facevalue:
            return D
        elif self.opponent_is_titfortat or self.opponent_is_clone:
            return TitForTat.strategy(self, opponent)
        else: # play titfortat with random defections every 5-15 turns
            if self.next_random_defection_turn is None:
                self.next_random_defection_turn = self._random.randint(5, 15) + round_number
            if round_number == self.next_random_defection_turn:
                self.next_random_defection_turn = self._random.randint(5, 15) + round_number
                return D
            else: return TitForTat.strategy(self, opponent)



class GraaskampCX(axlGraaskamp, Player):
    name = "GRAScx"
    def __init__(self) -> None:
        super().__init__()
    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C

class GraaskampXX(axlGraaskamp, Player):
    name = "GRASxx"
    def __init__(self) -> None:
        super().__init__()
    def strategy_voice(self, opponent : Player) -> Action:
        return super().strategy(opponent)
    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]