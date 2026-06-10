from axelrod.action import Action
from axelrod.strategies import FirstByAnonymous as axlUnnamed

from axelrodVoice import Player

"""
According to Axelrod's appendix, this strategy was made
"by a graduate student of political science whose dissertation is in game theory".
It was by far the longest at 77 lines of code. For comparison, Downing was 33 and Stein was 50.
"""



"""
Calculates the opponent's kindness, apathy, and honesty.
P( c ) = kindness
P( C | cc ) = (kindness - apathy) * honesty
"""
class UnnamedStrategy(axlUnnamed, Player):
    name = "ANON"
    def __init__(self) -> None:
        super().__init__()
        self.apathy = 0
        self.kindness = 1
        self.honesty = 0.75
        self.my_score = 0
        self.op_score = 0
        self.op_is_nice = True

    def _count_plays(self, opponent: Player):
        num_D_D_o = 0
        num_D_C_o = 0
        num_C_D_o = 0
        num_C_C_o = 0
        for i in range(0,10):
            match (opponent.history_voice[-i], opponent.history[-i]):
                case (Action.C, Action.C): num_C_C_o += 1
                case (Action.C, Action.D): num_C_D_o += 1
                case (Action.D, Action.C): num_D_C_o += 1
                case (Action.D, Action.D): num_D_D_o += 1

        num_D_D_s = 0
        num_D_C_s = 0
        num_C_D_s = 0
        num_C_C_s = 0
        for i in range(0, 10):
            match (self.history_voice[-i], self.history[-i]):
                case (Action.C, Action.C): num_C_C_s += 1
                case (Action.C, Action.D): num_C_D_s += 1
                case (Action.D, Action.C): num_D_C_s += 1
                case (Action.D, Action.D): num_D_D_s += 1

        num_D_o = num_C_D_o + num_D_D_o
        num_D_s = num_C_D_s + num_D_D_s
        op_D_minus_me_D = num_D_o - num_D_s

        if num_C_C_o + num_C_D_o == 0:
            op_honesty = self.honesty
        else:
            op_honesty = num_C_C_o / (num_C_C_o + num_C_D_o)

        op_D_D_minus_op_D_C = num_D_D_o - num_D_C_o

        return op_D_minus_me_D, op_honesty, op_D_D_minus_op_D_C


    def strategy_voice(self, opponent : Player) -> Action:
        # update scores
        if opponent.history:
            last_round = (self.history[-1], opponent.history[-1])
            scores = self.match_attributes["game"].score(last_round)
            self.my_score += scores[0]
            self.op_score += scores[1]

        # every 10 rounds, update values
        if self.history and len(self.history) % 10 == 0:
            delta_d, recent_honesty, delta_weird = self._count_plays(opponent)
            if delta_d < -1: # you don't care that I defected more than you
                self.apathy = min(1, self.apathy + 0.2)
            elif delta_d > 1: # you were mean to me :(
                self.kindness = max(0, self.kindness - 0.2)
            else: # you kept defections even
                self.apathy = max(0, self.apathy - 0.2)

            self.honesty = (3*self.honesty + 1*recent_honesty) / 4

            # seems random
            if (0.4 < self.honesty < 0.6) and (delta_weird <= 1):
                self.apathy = min(1, self.apathy + 0.3)

            # losing
            if len(self.history) == 130 and self.op_score > self.my_score:
                self.apathy = 1

            #print(f"({len(self.history)}) k={self.kindness}, a={self.apathy}, h={self.honesty}")


        # P("C") = kindness
        # P( C | ["C"s, "C"o] ) = (kindness - apathy) * honesty
        return self._random.random_choice(self.kindness)



    def strategy(self, opponent : Player) -> Action:

        if self.history_voice[-1] == Action.D: return Action.D
        if opponent.history_voice[-1] == Action.C:
            return self._random.random_choice((self.kindness - self.apathy) * self.honesty)
        if opponent.history_voice[-1] == Action.D and self.kindness > 0.5:
            return self._random.random_choice((self.kindness) * self.honesty)
        else: return Action.D



class UnnamedNice(UnnamedStrategy):
    name = "UnnamedNice"
    def strategy_voice(self, opponent : Player) -> Action:
        if not opponent.history: return Action.C
        if opponent.history[-1] == Action.D: self.op_is_nice = False
        if self.op_is_nice: return Action.C
        return UnnamedStrategy.strategy_voice(self, opponent)
    def strategy(self, opponent : Player) -> Action:
        if opponent.history_voice[-1] == Action.D: self.op_is_nice = False
        if self.op_is_nice: return Action.C
        return UnnamedStrategy.strategy(self, opponent)

# Note: these are pure uniform(30,70)% cooperation
class UnnamedStrategyXX(axlUnnamed, Player):
    name = "ANONxx"
    def strategy_voice(self, opponent : Player) -> Action:
        return axlUnnamed.strategy(self, opponent)
    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]

class UnnamedStrategyCX(axlUnnamed, Player):
    name = "ANONcx"
    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C