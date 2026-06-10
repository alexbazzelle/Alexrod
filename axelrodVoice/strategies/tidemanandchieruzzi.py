from axelrod.action import Action
from axelrod.strategies import FirstByTidemanAndChieruzzi as axlTidemanAndChieruzzi
import random

from axelrodVoice import Player



"""
Does streaks of defections equal to the number of times the opponent has defected.
Gives a "fresh start" if the opponent is losing and did cC last round.
    Fresh starts are limited to every 20 rounds
Defection streaks mimic the opponent's number of defections and lies.
    Order of dD/cD is changed with variants.
"""
# all lies are done at the end of retaliation
class TidemanAndChieruzzi(axlTidemanAndChieruzzi, Player):
    name = "TICH"
    def __repr__(self):
        return self.name

    def __init__(self) -> None:
        super().__init__()
        self.rounds_since_fresh_start = -1
        self.will_cooperate = True
        self.remembered_defections = []
        self.current_retaliations = []
        self.retaliation_remaining = 0
        self.my_score = 0
        self.op_score = 0

    def _sort_retaliation_lies(self):
        # puts all lies at the start of the list
        # actions are picked beginning with the end of the list
        self.current_retaliations.sort(key=lambda act: "C" if act == "C" else "D")



    def strategy_voice(self, opponent : Player) -> Action:
        # increase counter for rounds since fresh start
        self.rounds_since_fresh_start += 1

        # update scores
        if opponent.history:
            last_round = (self.history[-1], opponent.history[-1])
            scores = self.match_attributes["game"].score(last_round)
            self.my_score += scores[0]
            self.op_score += scores[1]

        # if first round or fresh start, do C
        if self.rounds_since_fresh_start == 0:
            self.will_cooperate = True
            return Action.C

        # if you defected, add it to the counter
        try:
            if opponent.history[-1] == Action.D:
                self.remembered_defections.append(opponent.history_voice[-1])
        except:
            #print(f"TICH ERROR: op={opponent.name}, round={len(self.history_voice)}")
            return Action.C

        # fresh start check
        if (self.op_score + 10 <= self.my_score) and (opponent.history[-1] == Action.C) and (
                self.rounds_since_fresh_start >= 20) and (
                self.match_attributes["length"] - (len(self.history) + 1) >= 10):
            # check random using standard deviation of Binomial(n,p)
            n = self.rounds_since_fresh_start
            p = 0.5
            mean = n * p # expected random defections = np
            std_dev = (n * p * (1 - p))**(1/2) # standard deviation of random = sqrt( np(1-p) )
            # if opponent's defections are outside 3 standard deviations from the mean, they aren't random
            defections = len(self.remembered_defections)
            if (defections > mean + 3 * std_dev) or (
                    defections < mean - 3 * std_dev):
                # not random. give fresh start
                self.rounds_since_fresh_start = -1

        # if fresh start, reset everything
        if self.rounds_since_fresh_start == -1:
            self.remembered_defections = []
            self.current_retaliations = []
            self.retaliation_remaining = 0
            self.will_cooperate = True
            return Action.C

        # if you set me off, start the retaliation process
        if (self.retaliation_remaining == 0) and (opponent.history[-1] == Action.D):
            self.current_retaliations.append(opponent.history_voice[-1])
            # determine which retaliation defections are lies versus honest
            self._sort_retaliation_lies()
            self.retaliation_remaining = len(self.current_retaliations)

        # am I currently retaliating? then do that
        if self.retaliation_remaining > 0:
            self.will_cooperate = False
            self.retaliation_remaining -= 1
            return self.current_retaliations[self.retaliation_remaining]

        # done with checks! not retaliating. not a fresh start. cooperate
        self.will_cooperate = True
        return Action.C


    def strategy(self, opponent : Player) -> Action:
        if self.will_cooperate:
            return Action.C
        else:
            return Action.D



# randomize lying turns (but match op's lie count)
class TidemanAndChieruzziRandom(TidemanAndChieruzzi):
    name = "TICHra"
    def __repr__(self):
        return self.name
    def _sort_retaliation_lies(self):
        random.shuffle(self.current_retaliations)



# matches opponent's lying order
class TidemanAndChieruzziOrdered(TidemanAndChieruzzi):
    name = "TICHor"
    def __repr__(self):
        return self.name
    def _sort_retaliation_lies(self):
        self.current_retaliations.reverse()





class TidemanAndChieruzziXX(axlTidemanAndChieruzzi, Player):
    name = "TICHxx"
    def __repr__(self):
        return self.name
    def strategy_voice(self, opponent : Player) -> Action:
        return axlTidemanAndChieruzzi.strategy(self, opponent)
    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]

class TidemanAndChieruzziCX(axlTidemanAndChieruzzi, Player):
    name = "TICHcx"
    def __repr__(self):
        return self.name
    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C
    def strategy(self, opponent : Player) -> Action:
        return axlTidemanAndChieruzzi.strategy(self, opponent)