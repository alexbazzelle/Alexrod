from axelrod.action import Action
from axelrod.strategies import FirstByShubik as axlShubik

from axelrodVoice import Player



"""
Strives to maintain score equilibrium (with harsher punishments for liars)
"""
class Shubik(axlShubik, Player):
    name = "SHUB"
    def __init__(self):
        super().__init__()
        self.lying_violations = 0
        self.attacks_remaining = 0
        self.current_state = 0

    def strategy_voice(self, opponent : Player) -> Action:
        if not opponent.history: return Action.C
        while True:
            match self.current_state:
                case 0: # EQUILIBRIUM
                    #print(f"({len(opponent.history)+1}) V: equilibrium")
                    if opponent.history[-1] == Action.C:
                        return Action.C
                    # switch to ATTACK ["C", .D.]
                    if opponent.history_tuples[-1] == (Action.C, Action.D):
                        #print(f"({len(opponent.history) + 1}) V: switch to attack C .D.")
                        self.lying_violations += 1
                        self.attacks_remaining = self.lying_violations
                        self.current_state = 1
                    # switch to ATTACK ["D", .D.]
                    elif opponent.history_tuples[-1] == (Action.D, Action.D):
                        #print(f"({len(opponent.history) + 1}) V: switch to attack D .D.")
                        self.current_state = 2

                case 1: # ATTACK ["C", .D.]
                    #print(f"({len(opponent.history)+1}) V: attack C .D.")
                    if self.attacks_remaining > 0:
                        # I still have attacks to do
                        self.attacks_remaining -= 1
                        return Action.D
                    elif self.attacks_remaining == 0:
                        self.current_state = 0
                        #print(f"({len(opponent.history) + 1}) V: switch to equilibrium")
                        return Action.C

                case 2: # ATTACK ["D", .D.]
                    #print(f"({len(opponent.history) + 1}) V: attack D .D.")
                    if opponent.history[-1] == Action.C:
                        #print(f"({len(opponent.history) + 1}) V: switch to equlibrium")
                        self.current_state = 0
                        return Action.C
                    else: return Action.D

                case 3:
                    #print(f"({len(opponent.history)+1}) V: op said C last round")
                    if opponent.history[-1] == Action.C:
                        #print(f"({len(opponent.history) + 1}) V: switch to equilibrium")
                        self.current_state = 0
                        return Action.C
                    else: # op did ["C", .D.]: (score = -2)
                        #print(f"({len(opponent.history) + 1}) V: switch to double liar")
                        self.current_state = 4
                case 4: # ["D", .D.] until op picks .C. (score = -1)
                    #print(f"({len(opponent.history) + 1}) V: double liar")
                    if opponent.history[-1] == Action.C:
                        #print(f"({len(opponent.history) + 1}) V: switch to single liar")
                        self.current_state = 5
                        return Action.D
                    else:
                        return Action.D
                case 5: # ["D", .D.] until op picks .C. (score = 0)
                    #print(f"({len(opponent.history)+1}) V: single liar")
                    if opponent.history[-1] == Action.C:
                        #print(f"({len(opponent.history) + 1}) V: switch to equilibrium")
                        self.current_state = 0 # swap to equilibrium
                        return Action.C
                    else:
                        return Action.D
        print("SHUBIK MESSED UP - VOICE")
        return Action.C




    def strategy(self, opponent : Player) -> Action:
        match self.current_state:
            case 0: return Action.C # equilibrium
            case 1: return Action.D # liars
            case 2:
                if (opponent.history_voice[-2], opponent.history[-1]) == (Action.D, Action.D):
                    # i gotta do at least one defection
                    return Action.D
                if opponent.history_voice[-1] == Action.D:
                    return Action.D
                else:
                    self.current_state = 3
                    return Action.C
            case 3: return Action.D
            case 4: return Action.D
            case 5: return Action.D

        print("SHUBIK MESSED UP - CHOICE")
        return Action.C


class ShubikXX(axlShubik, Player):
    name = "SHUBxx"
    def strategy_voice(self, opponent : Player) -> Action:
        return axlShubik.strategy(self, opponent)
    def strategy(self, opponent : Player) -> Action:
        return self.history_voice[-1]

class ShubikCX(axlShubik, Player):
    name = "SHUBcx"
    def strategy_voice(self, opponent : Player) -> Action:
        return Action.C