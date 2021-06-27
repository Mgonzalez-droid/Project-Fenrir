"""Global Game state object used to track game state when switching scenes etc.

"""

from fenrir.common.config import DisplaySettings


class GameState:

    def __init__(self, player_name=""):
        # when we start saving games and other data
        self._player_name = "Player 1"
        self._player_level = 1  # default starting point

        # overworld battle vars
        self._in_battle = False
        self._won_battle = False

        # overworld player location variables
        self._overworld_location_x = DisplaySettings.CENTER_WIDTH.value
        self._overworld_location_y = DisplaySettings.CENTER_HEIGHT.value

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
    def in_battle(self):
        return self._in_battle

    @in_battle.setter
    def in_battle(self, val: bool):
        self._in_battle = val

    @property
    def won_battle(self):
        return self._won_battle

    @won_battle.setter
    def won_battle(self, val: bool):
        self._won_battle = val

    @property
    def overworld_location_x(self):
        return self._overworld_location_x

    @overworld_location_x.setter
    def overworld_location_x(self, x_val: int):
        self._overworld_location_x = x_val

    @property
    def overworld_location_y(self):
        return self._overworld_location_y

    @overworld_location_y.setter
    def overworld_location_y(self, y_val: int):
        self._overworld_location_x = y_val
