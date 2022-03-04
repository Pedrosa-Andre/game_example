from game.casting.trail import Trail


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
        """Gets directional input from the keyboard and applies it to the players.

        Args:
            cast (Cast): The cast of actors.
        """

        cycle1 = cast.get_first_actor("cycle1")
        vel = cycle1.get_direction()
        cycle1.set_velocity(vel)

        cycle2 = cast.get_first_actor("cycle2")
        vel = cycle2.get_direction()
        cycle2.set_velocity(vel)

    def _do_updates(self, cast):
        """Updates the players' positions and resolves any collisions with trails.

        Args:
            cast (Cast): The cast of actors.
        """
        cycle1 = cast.get_first_actor("cycle1")
        cycle2 = cast.get_first_actor("cycle2")

        max_x = self._display_service.get_width()
        max_y = self._display_service.get_height()
        cycle1.move_next(max_x, max_y)
        cycle2.move_next(max_x, max_y)


        trail1 = Trail(cycle1.get_previous_position(), cycle1.get_color())
        cast.add_actor("trails", trail1)
        trail2 = Trail(cycle2.get_previous_position(), cycle2.get_color())
        cast.add_actor("trails", trail2)

        all_trails = cast.get_actors("trails")
        for trail in all_trails:
            if cycle1.get_position().equals(trail.get_position()):
                cycle1.die()
                ### BE CAREFUL this closes the game, we have to change the
                ### game over system.
                #self.__game_over = True
            if cycle2.get_position().equals(trail.get_position()):
                cycle2.die()
                #self.__game_over = True

    # The game over

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
