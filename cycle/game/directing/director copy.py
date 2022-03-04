from game.shared.point import Point
from game.casting.restorer import Restorer

class Director:
    """A person who directs the game. 

    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _display_service (DisplayService): For providing display output.
    """

    def __init__(self, keyboard_service, display_service):
        self._SCORE = 600
        self.__game_over = False
        """Constructs a new Director using the specified keyboard and display services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            display_service (DisplayService): An instance of DisplayService.
        """
        self._keyboard_service = keyboard_service
        self._display_service = display_service

    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._display_service.open_window()
        while self._display_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
            if self._is_over():
                self.__game_over = False
                self._display_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the player.

        Args:
            cast (Cast): The cast of actors.
        """
        player = cast.get_first_actor("players")
        velocity = self._keyboard_service.get_direction()
        player.set_velocity(velocity)

    def _do_updates(self, cast):
        """Updates the player's position and resolves any collisions with artifacts.

        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        player = cast.get_first_actor("players")
        artifacts = cast.get_actors("artifacts")
        rocks = cast.get_actors("rocks")
        rubys = cast.get_actors("rubys")
        its_alive = Restorer()

        max_x = self._display_service.get_width()
        max_y = self._display_service.get_height()
        player.move_next(max_x, max_y)
        artifact_count = 0
        rock_count = 0
        a = 0
        r = 0

        for artifact in artifacts:
            artifact_count +=1

        for rock in rocks:
            rock_count += 1


        for artifact in artifacts:
            a += 1
            artifact.set_velocity(Point(0, 5))
            artifact.move_next(max_x, max_y)

            if player.get_position().equals(artifact.get_position()):
                cast.remove_actor("artifacts", artifact)
                a -= 1
                self._SCORE += 1

        for rock in rocks:
            r += 1
            rock.set_velocity(Point(0, 5))
            rock.move_next(max_x, max_y)
            if player.get_position().equals(rock.get_position()):
                cast.remove_actor("rocks", rock)
                r -= 1
                self._SCORE -= 1
                
                if self._SCORE == 0:
                    self.__game_over = True

        for ruby in rubys:
            ruby.move_next(max_x, max_y)
            if player.get_position().equals(ruby.get_position()):
                self._SCORE += ruby.get_points()
                ruby.respawn()

        if self._SCORE == 0:
            self.__game_over = True

        if a < artifact_count:
            its_alive.resurrect_artifact(cast = cast)
        if r < rock_count:
            its_alive.resurrect_artifact2(cast = cast)

        banner.set_text("Score: " + str(self._SCORE))

    # The game overrocks

    def _is_over(self):
        return self.__game_over

    def _do_outputs(self, cast):
        """Draws the actors on the screen.

        Args:
            cast (Cast): The cast of actors.
        """
        self._display_service.clear_buffer()
        actors = cast.get_all_actors()
        self._display_service.draw_actors(actors)
        self._display_service.flush_buffer()
