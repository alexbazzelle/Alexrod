import axelrod.match
import axelrod.classifier
from axelrod import Action
C, D = Action.C, Action.D

"""
Updates to Match class:
- added result_voice:List
- updated simultaneous_play to store results
- added debug:int, show_output, and _print_output (used in play)
"""

class Match(axelrod.match.Match):
    def __init__(
        self,
        players,
        turns=None,
        prob_end=None,
        game=None,
        deterministic_cache=None,
        noise=0,
        match_attributes=None,
        reset=True,
        seed=None,
    ):
        super().__init__(players, turns, prob_end,
            game, deterministic_cache, noise,
            match_attributes, reset, seed)
        self.debug = 0
        self.result_voice = []

# NEW FUNCTIONS
    def show_output(self, output_mode=1) -> None:
        match output_mode:
            case 1:
                self.debug = 1;  # abAB  (#/#)
            case 2:
                self.debug = 2;  # ["a" "b"] [.A. .B.] (# /#)
            case 3:
                self.debug = 3;  # abAB abAB abAB ...
            case 4:
                self.debug = 4;  # ab AB   ab AB   ...
            case _:
                print(f"Output modes:")
                print(f"   1: abAB  (#/#)")
                print(f"   2: [\"a\" \"b\"] [.A. .B.] # /#")
                print(f"   3: abAB abAB abAB ...")
                print(f"   4: ab AB   ab AB   ...")

    def _print_output(self, p1, p2) -> None:
        # Assign colors to each response type
        c = "\033[32mc\033[39m\033[49m"
        C = "\033[92mC\033[39m\033[49m"
        d = "\033[31md\033[39m\033[49m"
        D = "\033[91mD\033[39m\033[49m"

        actions = zip(p1.history_voice, p2.history_voice, p1.history, p2.history, range(1, self.turns + 1))

        # Format for output
        header = f"aA = {p1.name}, bB = {p2.name}\n"
        match self.debug:
            case 1:
                header += f"abAB  (#/#)"
            case 2:
                header += f"[\"a\" \"b\"] [.A. .B.] # /#"
            case 3:
                header += f"abAB abAB abAB ..."
            case 4:
                header += f"ab AB   ab AB   ..."
        print(header)

        # Print rounds
        for (v1, v2, c1, c2, i) in actions:
            p1v = c if v1 == axelrod.action.Action.C else d
            p2v = c if v2 == axelrod.action.Action.C else d
            p1c = C if c1 == axelrod.action.Action.C else D
            p2c = C if c2 == axelrod.action.Action.C else D

            match self.debug:
                case 1:
                    print(f"{p1v}{p2v}{p1c}{p2c}  ({i}/{self.turns})")
                case 2:
                    print(f"[\"{p1v}\" \"{p2v}\"] [.{p1c}. .{p2c}.] {i} /{self.turns}")
                case 3:
                    print(f"{p1v}{p2v}{p1c}{p2c}", end=" ")
                case 4:
                    print(f"{p1v}{p2v} {p1c}{p2c}", end="   ")
        if self.debug == 3 or self.debug == 4: print()  # new line at end
# END NEW FUNCTIONS


    def play(self):
        if self.prob_end:
            r = self._random.random()
            turns = min(super().sample_length(self.prob_end, r), self.turns)
        else:
            turns = self.turns
        cache_key = (self.players[0], self.players[1])

        if self._stochastic or not self._cached_enough_turns(cache_key, turns):
            for p in self.players:
                if self.reset:
                    p.reset()
                p.set_match_attributes(**self.match_attributes)
                # Generate a random seed for the player, if stochastic
                if axelrod.classifier.Classifiers["stochastic"](p):
                    p.set_seed(self._random.random_seed_int())
            result = []
            for _ in range(turns):
                plays = self.simultaneous_play(
                    self.players[0], self.players[1], self.noise
                )
                result.append(plays)

            if self._cache_update_required:
                self._cache[cache_key] = result
        else:
            result = self._cache[cache_key][:turns]
        self.result = result

        # NEW: print debug output
        if self.debug: self._print_output(p1=self.players[0], p2=self.players[1])
        # END NEW
        return result
    

    def simultaneous_play(self, player, coplayer, noise=0):
        # NEW: record voice responses
        v1, v2 = player.strategy_voice(coplayer), coplayer.strategy_voice(player)
        player.update_history_voice(v1, v2)
        coplayer.update_history_voice(v2, v1)
        self.result_voice.append((v1, v2))
        # END NEW

        """This pits two players against each other."""
        s1, s2 = player.strategy(coplayer), coplayer.strategy(player)
        if noise:
            # Note this uses the Match classes random generator, not either
            # player's random generator. A player shouldn't be able to
            # predict the outcome of this noise flip.
            s1 = self._random.random_flip(s1, noise)
            s2 = self._random.random_flip(s2, noise)
        player.update_history(s1, s2)
        coplayer.update_history(s2, s1)
        # NEW: update complete history
        player.update_history_tuples()
        coplayer.update_history_tuples()
        # NEW END
        return s1, s2

