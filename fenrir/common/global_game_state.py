"""Global Game state object used to track game state when switching scenes etc.
"""

from datetime import datetime
from fenrir.common.config import DisplaySettings


class GameState:

    def __init__(self, player_id=None, player_name="Player 1", last_save=None,
                 player_level=1, location_x=555, location_y=180):
        # when we start saving games and other data
        self._player_name = player_name
        self._player_id = player_id
        self._last_save = last_save
        self._player_level = player_level
        self._player_party = []
        self._enemy_party = []

        # overworld player location variables
        self._game_state_location_x = location_x
        self._game_state_location_y = location_y

        # All possible heroes to use in combat
        self._all_heroes = [["knight", "chars/knight/knight_menu.png"], ["archer", "chars/archer/archer_menu.png"],
                            ["mage", "chars/mage/mage_menu.png"]]

        # TODO need inventory and other persistent data to save in Database

    @property
    def player_name(self):
        return self._player_name

    @player_name.setter
    def player_name(self, name: str):
        self._player_name = name

    @property
    def player_id(self):
        return self._player_id

    @property
    def last_save(self):
        return self._last_save

    @last_save.setter
    def last_save(self, save_date_time: datetime):
        self._last_save = save_date_time

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

    @property
    def all_heroes(self):
        return self._all_heroes

    @all_heroes.setter
    def all_heroes(self, all_heroes):
        self._all_heroes = all_heroes

    @property
    def player_party(self):
        return self._player_party

    @player_party.setter
    def player_party(self, player_party):
        self._player_party = player_party

    @property
    def enemy_party(self):
        return self._enemy_party

    @enemy_party.setter
    def enemy_party(self, enemy_party):
        self._enemy_party = enemy_party

    def reset_game_state(self):
        self._player_name = "Player 1"
        self._player_level = 1  # default starting point

        # overworld player location variables
        self._game_state_location_x = 555
        self._game_state_location_y = 180
