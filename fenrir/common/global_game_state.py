"""Global Game state object used to track game state when switching scenes etc.

"""

from fenrir.common.config import DisplaySettings


class GameState:

    def __init__(self, player_name=""):
        # when we start saving games and other data
        self._player_name = "Player 1"
        self._player_level = 1  # default starting point

        # overworld player location variables
        self._game_state_location_x = 555
        self._game_state_location_y = 180

    @property
    def player_name(self):
        return self._player_name

    @player_name.setter
    def player_name(self, name: str):
        self._player_name = name

    @property
    def player_level(self):
        return self._player_level

    def increase_player_level(self):
        self._player_level += 1

    @property
    def game_state_location_x(self):
        return self._game_state_location_x

    @game_state_location_x.setter
    def game_state_location_x(self, x_val):
        self._game_state_location_x = x_val

    @property
    def game_state_location_y(self):
        return self._game_state_location_y

    @game_state_location_y.setter
    def game_state_location_y(self, y_val):
        self._game_state_location_y = y_val

    def reset_game_state(self):
        self._player_name = "Player 1"
        self._player_level = 1  # default starting point

        # overworld player location variables
        self._game_state_location_x = 555
        self._game_state_location_y = 180