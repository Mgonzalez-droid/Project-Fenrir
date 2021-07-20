"""
.. module:: combat_initiative_system
  :synopsis: module that determines the order of units in turn based combat mode.
"""

from itertools import cycle


class CombatInitiativeSystem:
    """Class represents the initiative system that will be deployed in each combat instance and will determine
        the order of battle.

        :param participants: list of combat character objects in combat instance
    """

    def __init__(self, participants):
        """Constructor method
        """
        self._ordered_initiative_list = sorted(list(participants), key=lambda p: p.speed, reverse=True)
        self._current_position = 0
        self._player_killed = False
        self._last_player_killed = False

    def get_current_player(self):
        """Gets the character that is up for turn in combat

        :returns: CombatCharacterData object
        """
        return self._ordered_initiative_list[self._current_position]

    def get_next_player_up(self):
        """Gets the character that is up next after the current turn is complete

            :returns: CombatCharacterData object
        """
        index = self._current_position + 1 if self._current_position + 1 < len(
            self._ordered_initiative_list) else 0
        return self._ordered_initiative_list[index]

    def update_system(self):
        """Updates the combat initiative system by updating current position in list. Operates as a cycle and will move
            to position 0 when reaching last participant. Must be called after each turn is completed.
        """
        self._current_position += 1

        if self._last_player_killed:
            if self._current_position >= len(self._ordered_initiative_list):
                self._current_position = 0
        elif self._player_killed and self._current_position == len(self._ordered_initiative_list):
            self._current_position -= 1
        elif self._current_position >= len(self._ordered_initiative_list):
            self._current_position = 0

        self._player_killed = False
        self._last_player_killed = False

    def remove_player(self, player_id):
        self._player_killed = True
        for i in range(0, len(self._ordered_initiative_list)):
            if self._ordered_initiative_list[i].get_id() == player_id:
                self._ordered_initiative_list.pop(i)
                if i == len(self._ordered_initiative_list) - 1:
                    self._last_player_killed = True
                break
