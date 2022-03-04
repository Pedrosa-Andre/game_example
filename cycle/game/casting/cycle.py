from game.casting.actor import Actor
import game.shared.gamecontants as gameconstants

from game.services.keyboard_service_flex import KeyboardServiceFlex


class Cycle(Actor):
    """
    """
    def __init__(self, pos, num = 0):
        """
        """
        super().__init__()
        self.set_text("@")
        self.set_position(pos)
        self._keyboard_service_flex = KeyboardServiceFlex(num)
        self._DEAD = False
        self._previous_position = pos
    
    def get_direction(self):
        """
        """
        velocity = self._keyboard_service_flex.get_direction()
        return velocity

    def die(self):
        """
        """
        self._dead = True
        self.set_color(gameconstants.WHITE)

    def move_next(self, max_x, max_y):
        self._previous_position = self._position
        super().move_next(max_x, max_y)

    def get_previous_position(self):
        return self._previous_position
