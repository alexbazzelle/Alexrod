from typing import Callable, List, Optional
from axelrod import DEFAULT_TURNS, Game
from axelrod.deterministic_cache import DeterministicCache
from axelrod.graph import Graph

import axelrod.moran as moran
import axelrodVoice.playerVoice as avPlayerVoice
import axelrodVoice.matchVoice as avMatchVoice

"""
NOTE:
Although this feature was not used in the motivating article, it is functional. 
This class is included to emphasize the compatibility with most analysis tools provided by the AxelrodPython library.
I'm sure there is a way to make this type conversion automatic using class inheritance or abstract functions.
Please share any ideas or implementations!
"""
"""
Updates to MoranProcess class:
- replaced Player and Match with the voice variation
"""
class MoranProcess(moran.MoranProcess):
    def __init__(
            self,
            players: List[avPlayerVoice.Player], # this was changed
            turns: int = DEFAULT_TURNS,
            prob_end: Optional[float] = None,
            noise: float = 0,
            game: Game = None,
            deterministic_cache: DeterministicCache = None,
            mutation_rate: float = 0.0,
            mode: str = "bd",
            interaction_graph: Graph = None,
            reproduction_graph: Graph = None,
            fitness_transformation: Optional[Callable] = None,
            mutation_method="transition",
            stop_on_fixation=True,
            seed=None,
            match_class=avMatchVoice.Match, # this was changed
    ) -> None:
        super().__init__(players, turns, prob_end, noise, game, deterministic_cache, mutation_rate, mode, interaction_graph, reproduction_graph, fitness_transformation, mutation_method, stop_on_fixation, seed, match_class)
