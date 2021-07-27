"""Global Game state object used to track game state when switching scenes etc.
"""

from datetime import datetime
from fenrir.common.config import GameConstants


class GameState:

    def __init__(self, player_id=None, player_name="Player 1", last_save=None,
                 player_level=1, location_x=550, location_y=230,
                 player_party=["knight", "mage", "archer", "archer"], map_name="hub_world", boss_victory=0):
        # when we start saving games and other data
        self._player_name = player_name
        self._player_id = player_id
        self._last_save = last_save
        self._player_level = player_level
        self._player_party = player_party

        # Saving enemy data that player will fight against
        self._enemy_name = ""
        self._enemy_party = []
        self._enemy_level = None
        self._game_state_current_map = map_name
        self._final_victory = boss_victory

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
        if self._player_level < GameConstants.MAX_LEVEL.value:
            self._player_level += 1

    @property
    def final_victory(self):
        return self._final_victory

    @final_victory.setter
    def final_victory(self, victory_bool):
        self._final_victory = victory_bool

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
    def game_state_current_map(self):
        return self._game_state_current_map

    @game_state_current_map.setter
    def game_state_current_map(self, game_state_current_map):
        self._game_state_current_map = game_state_current_map

    @property
    def enemy_name(self):
        return self._enemy_name

    @enemy_name.setter
    def enemy_name(self, enemy_name):
        self._enemy_name = enemy_name

    @property
    def enemy_party(self):
        return self._enemy_party

    @enemy_party.setter
    def enemy_party(self, enemy_party):
        self._enemy_party = enemy_party

    @property
    def enemy_level(self):
        return self._enemy_level

    @enemy_level.setter
    def enemy_level(self, level):
        self._enemy_level = level

    def reset_game_state(self):
        self._player_name = "Player 1"
        self._player_level = 1  # default starting point

        # overworld player location variables
        self._game_state_current_map = "hub_world"
        self._game_state_location_x = 550
        self._game_state_location_y = 230
