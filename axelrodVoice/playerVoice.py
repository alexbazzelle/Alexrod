import axelrod.player
import axelrod.history
import axelrod.action

"""
Updates to Player class:
- added history_voice:History
- added history_tuples:List
- overrode repr (names no longer have parameters appended)
- added strategy_voice
"""
class Player(axelrod.player.Player):

    def __init__(self):
        super().__init__() # original player
        self._history_voice = axelrod.history.History() # [ x, ... ]
        self._history_tuples = [] # [ (x,Y) , ... ]


    # this overrides adding parameters to names
    def __repr__(self):
        return self.name

    def strategy_voice(self, opponent):
        raise NotImplementedError()

    def update_history_voice(self, play, coplay):
        self.history_voice.append(play, coplay)

    def update_history_tuples(self):
        self._history_tuples.append( (self.history_voice[-1], self.history[-1]) )

    @property
    def history_voice(self):
        return self._history_voice
    @property
    def history_tuples(self):
        return self._history_tuples
