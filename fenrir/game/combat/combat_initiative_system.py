"""
.. module:: combat_initiative_system
  :synopsis: module that determines the order of units in turn based combat mode.
"""


class CombatInitiativeSystem:
    """Class represents the initiative system that will be deployed in each combat instance and will determine
        the order of battle.

        :param participants: list of combat character objects in combat instance
    """

    def __init__(self, participants):
        """Constructor method
        """
        # order participants then store them in private class variable
        self._ordered_initiative_list = sorted(list(participants), key=lambda p: p.speed, reverse=True)
        self._current_position = 0

    def get_current_participant(self):
        """Gets the character that is up for turn in combat

        :returns: CombatCharacterData object
        """
        return self._ordered_initiative_list[self._current_position]

    def get_next_participant(self):
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
        if self._current_position == len(self._ordered_initiative_list) - 1:
            self._current_position = 0
        else:
            self._current_position += 1
