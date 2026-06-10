from axelrod.action import Action
from axelrod.strategies import RevisedDowning as axlDowningR
from axelrod.strategies import FirstByDowning as axlDowning

from axelrodVoice import Player

"""
Assumes the opponent is a lag-one matching strategy and maximizes EV while determining opponent's probabilities.
Picks between 10 different strategies (4 monotone, 6 alternating)
"""
DEBUG = False
class Downing(axlDowningR, Player):
    name = "DOWN"

    def __init__(self) -> None:
        super().__init__()
        self.voice = Action.C
        self.choice = Action.C

        # default values are for Tit-for-Tat
        # prob_xy_z := P( C_o | xY z_s )
        # coops_xy_z := number of C_o following xY z_s
        # total_xy_z := number of times I have done xY z
        self.prob_cc_c = 1
        self.coops_cc_c = 0
        self.total_cc_c = 0

        self.prob_cc_d = 1
        self.coops_cc_d = 0
        self.total_cc_d = 0

        self.prob_cd_c = 0
        self.coops_cd_c = 0
        self.total_cd_c = 0

        self.prob_cd_d = 0
        self.coops_cd_d = 0
        self.total_cd_d = 0

        self.prob_dc_c = 1
        self.coops_dc_c = 0
        self.total_dc_c = 0

        self.prob_dc_d = 1
        self.coops_dc_d = 0
        self.total_dc_d = 0

        self.prob_dd_c = 0
        self.coops_dd_c = 0
        self.total_dd_c = 0

        self.prob_dd_d = 0.25#0
        self.coops_dd_d = 0
        self.total_dd_d = 0

    def strategy_voice(self, opponent : Player) -> Action:
        round_number = len(self.history) + 1

        if round_number == 1:
            # on round 1, there is no info.
            # all we can do is act
            return Action.C

        if round_number == 2:
            # Assume opponent's opening move is based on me doing ["C", C]
            last_moves = (Action.C, Action.C, self.history_voice[-1])

        if round_number > 2:
            # Assume opponent's choice is based on my full play from last round
            # AND ALSO what I say this round
            last_moves = (self.history_voice[-2], self.history[-2], self.history_voice[-1])

        # Update recorded opponent probabilities
        match last_moves:
            # cC c_s
            case (Action.C, Action.C, Action.C):
                self.total_cc_c += 1
                if opponent.history[-1] == Action.C: self.coops_cc_c += 1
                self.prob_cc_c = self.coops_cc_c / self.total_cc_c
            # cC d_s
            case (Action.C, Action.C, Action.D):
                self.total_cc_d += 1
                if opponent.history[-1] == Action.C: self.coops_cc_d += 1
                self.prob_cc_d = self.coops_cc_d / self.total_cc_d
            # cD c
            case (Action.C, Action.D, Action.C):
                self.total_cd_c += 1
                if opponent.history[-1] == Action.C: self.coops_cd_c += 1
                self.prob_cd_c = self.coops_cd_c / self.total_cd_c
            # cD d_s
            case (Action.C, Action.D, Action.D):
                self.total_cd_d += 1
                if opponent.history[-1] == Action.C: self.coops_cd_d += 1
                self.prob_cd_d = self.coops_cd_d / self.total_cd_d
            # dC c_s
            case (Action.D, Action.C, Action.C):
                self.total_dc_c += 1
                if opponent.history[-1] == Action.C: self.coops_dc_c += 1
                self.prob_dc_c = self.coops_dc_c / self.total_dc_c
            # dC d_s
            case (Action.D, Action.C, Action.D):
                self.total_dc_d += 1
                if opponent.history[-1] == Action.C: self.coops_dc_d += 1
                self.prob_dc_d = self.coops_dc_d / self.total_dc_d
            # dD c_s
            case (Action.D, Action.D, Action.C):
                self.total_dd_c += 1
                if opponent.history[-1] == Action.C: self.coops_dd_c += 1
                self.prob_dd_c = self.coops_dd_c / self.total_dd_c
            # dD d_s
            case (Action.D, Action.D, Action.D):
                self.total_dd_d += 1
                if opponent.history[-1] == Action.C: self.coops_dd_d += 1
                self.prob_dd_d = self.coops_dd_d / self.total_dd_d


        # Calculate the expected score per turn for 10 different strategies
        ev_all_cc = 3 * self.prob_cc_c
        ev_all_cd = 4 * self.prob_cd_c + 1
        ev_all_dc = 3 * self.prob_dc_d
        ev_all_dd = 4 * self.prob_dd_d + 1
        ev_alt_cc_cd = 0.5 * (3*self.prob_cd_c + 4*self.prob_cc_c + 1)
        ev_alt_cc_dc = 0.5 * (3*self.prob_dc_c + 3*self.prob_cc_d)
        ev_alt_cc_dd = 0.5 * (3*self.prob_dd_c + 4*self.prob_cc_d + 1)
        ev_alt_cd_dc = 0.5 * (3*self.prob_cd_d + 4*self.prob_dc_c + 1)
        ev_alt_cd_dd = 0.5 * (4*self.prob_dd_c + 1 + 4*self.prob_cd_d + 1)
        ev_alt_dc_dd = 0.5 * (3*self.prob_dd_d + 4*self.prob_dc_d + 1)


        # Determine the best strategy.
        # If multiple strategies have the same expected value,
        #    then the strategy appearing first is picked.
        # This order was determined by vibes with the
        #    assumptions that cc > cd > dd >>> dc
        #    and monotone > alternating strategies
        max_same_strats = max(ev_all_cc, ev_all_cd, ev_all_dd, ev_all_dc)
        max_alt_strats = max(ev_alt_cc_cd, ev_alt_cc_dd, ev_alt_cd_dd,
                             ev_alt_cd_dc, ev_alt_dc_dd, ev_alt_cc_dc)

        if DEBUG:
            print(f"({round_number}): Same ("
                  f"CC={round(ev_all_cc, 3)},"
                  f"CD={round(ev_all_cd, 3)},"
                  f"DD={round(ev_all_dd, 3)},"
                  f"DC={round(ev_all_dc, 3)})")
        if DEBUG:
            print(f"({round_number}): Alt "
                  f"(CX={round(ev_alt_cc_cd,3)},"
                  f"XX={round(ev_alt_cc_dd,3)},"
                  f"XD={round(ev_alt_cd_dd,3)},"
                  f"XY={round(ev_alt_cd_dc,3)},"
                  f"DX={round(ev_alt_dc_dd,3)},"
                  f"XC={round(ev_alt_cc_dc,3)})")


        # Same Strategies: ["X", Y] -> ["X", Y]
        if max_same_strats >= max_alt_strats:
            if ev_all_cc == max_same_strats: # ["C", C]
                self.voice, self.choice = Action.C, Action.C
            elif ev_all_cd == max_same_strats: # ["C", D]
                self.voice, self.choice = Action.C, Action.D
            elif ev_all_dd == max_same_strats: # ["D", D]
                self.voice, self.choice = Action.D, Action.D
            else: #if ev_all_dc == max_same_strats: # ["D", C]
                self.voice, self.choice = Action.D, Action.C
            return self.voice



        # Alternating Strategies: ["W", X] -> ["Y", Z] -> ["W", X] -> ["Y", Z]
        #     (starting with ["W",X] vs ["Y",Z] was picked based on vibes)
        if max_alt_strats > max_same_strats:
            if ev_alt_cc_cd == max_alt_strats: # ["C", C] -> ["C", D]
                if (self.history_voice[-1], self.history[-1]) == (Action.C, Action.C):
                    self.voice, self.choice = Action.C, Action.D
                else: self.voice, self.choice = Action.C, Action.C # this is the default start for this strategy
            if ev_alt_cc_dd == max_alt_strats: # ["C", C] -> ["D", D]
                if (self.history_voice[-1], self.history[-1]) == (Action.C, Action.C):
                    self.voice, self.choice = Action.D, Action.D
                else: self.voice, self.choice = Action.C, Action.C
            if ev_alt_cd_dd == max_alt_strats: # ["C", D] -> ["D", D]
                if (self.history_voice[-1], self.history[-1]) == (Action.C, Action.D):
                    self.voice, self.choice = Action.D, Action.D
                else: self.voice, self.choice = Action.C, Action.D
            if ev_alt_cd_dc == max_alt_strats: # ["C", D] -> ["D", C]
                if (self.history_voice[-1], self.history[-1]) == (Action.C, Action.D):
                    self.voice, self.choice = Action.D, Action.C
                else: self.voice, self.choice = Action.C, Action.D
            if ev_alt_dc_dd == max_alt_strats: # ["D", D] -> ["D", C]
                if (self.history_voice[-1], self.history[-1]) == (Action.D, Action.D):
                    self.voice, self.choice = Action.D, Action.C
                else: self.voice, self.choice = Action.D, Action.D
            if ev_alt_cc_dc == max_alt_strats: # ["C", C] -> ["D", C]
                if (self.history_voice[-1], self.history[-1]) == (Action.C, Action.C):
                    self.voice, self.choice = Action.D, Action.C
                else: self.voice, self.choice = Action.C, Action.C

        # idea: if an alternating strat is best, use ev(all XY) to figure which option first?
        return self.voice

    def strategy(self, opponent : Player) -> Action:
        return self.choice


class DowningXX(axlDowning, Player):
    name = "DOWNxx"
    def strategy_voice(self, opponent : Player) -> Action:
        return axlDowning.strategy(self, opponent)
    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]

class DowningCX(axlDowning, Player):
    name = "DOWNcx"
    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C


class DowningRXX(axlDowningR, Player):
    name = "DOWRxx"
    def strategy_voice(self, opponent : Player) -> Action:
        return axlDowningR.strategy(self, opponent)
    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]

class DowningRCX(axlDowningR, Player):
    name = "DOWRcx"
    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C