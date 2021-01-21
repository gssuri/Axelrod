from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D

class Gursahib(Player):

name = "Gursahib"

    def __init__(self, q: float = 0.9) -> None:
 
    self.q = q
    four_vector = (q, 1 - q, q, 1 - q)
    super().__init__(four_vector)

    def __repr__(self) -> str:
        return "%s: %s" % (self.name, round(self.q, 2))
    def strategy(self, opponent: Player) -> Action:
        if len(opponent.history) == 0:
            return self._initial
        # Determine which probability to use
        p = self._four_vector[(self.history[-1], opponent.history[-1])]
        # Draw a random number in [0, 1] to decide
        return random_choice(p)
