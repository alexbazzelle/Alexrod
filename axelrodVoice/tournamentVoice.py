
from typing import List, Optional, Tuple
from collections import defaultdict

import axelrod.game
import axelrodVoice.playerVoice as avPlayerVoice
import axelrodVoice.matchVoice as avMatchVoice

"""
Updates to Tournament class:
 - changed axl.Player to axlVoice.Player
 - changed match in play_matches to axlVoice.Match
"""
class Tournament(axelrod.tournament.Tournament):
    def __init__(
            self,
            players: List[avPlayerVoice.Player],
            name: str = "axelrodVoice",
            game: axelrod.game.Game = None,
            turns: Optional[int] = None,
            prob_end: Optional[float] = None,
            repetitions: int = 10,
            noise: float = 0,
            edges: Optional[List[Tuple]] = None,
            match_attributes: Optional[dict] = None,
            seed: Optional[int] = None,
    ) -> None:
        super().__init__(players, name, game, turns,
                         prob_end, repetitions, noise,
                         edges, match_attributes, seed)


    def _play_matches(self, chunk: avMatchVoice.Match, build_results: bool = True):
        """
        Play matches in a given chunk.

        Parameters
        ----------
        chunk : tuple (index pair, match_parameters, repetitions)
            match_parameters are also a tuple: (turns, game, noise)
        build_results : bool
            whether or not to build a results set

        Returns
        -------
        interactions : dictionary
            Mapping player index pairs to results of matches:

                (0, 1) -> [(C, D), (D, C),...]
        """
        interactions = defaultdict(list)
        p1_index, p2_index = chunk.index_pair
        player1 = self.players[p1_index].clone()
        player2 = self.players[p2_index].clone()
        chunk.match_params["players"] = (player1, player2)
        chunk.match_params["seed"] = chunk.seed
        match = avMatchVoice.Match(**chunk.match_params)
        for _ in range(chunk.repetitions):
            match.play()

            if build_results:
                results = self._calculate_results(match.result)
            else:
                results = None

            interactions[chunk.index_pair].append([match.result, results])
        return interactions

