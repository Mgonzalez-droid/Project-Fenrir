"""
.. module:: combat_character_data
  :synopsis: module for creating a new character in the combat scenes. Can be ally or enemy
"""

import math


class CombatCharacterData:
    """Class representing individual characters, and their attributes for the combat scenes

    :param id: given id value for the new character
    :param level: level for the new character (can be updated later)
    :param speed: speed/initiative value for the new character (can be updated later)
    :param hp: hp for the new character (can be updated later)
    :param attack: base attack value for new character (can be updated later)
    :param enemy: boolean to determine if character is enemy. Defaults to false
    """

    def __init__(self, id, level, speed, hp, attack, enemy=False):
        self._id = id
        self._level = level
        self._speed = speed
        self._hp = hp
        self._attack = attack
        self._enemy = enemy

    def get_id(self):
        return self._id

    def get_level(self):
        return self._level

    def get_speed(self):
        return self._speed

    def get_hp(self):
        return self._hp

    def get_attack(self):
        return self._attack

    def get_is_enemy(self):
        return self._enemy

    def update_level(self, newLevel):
        self._level = newLevel

    def update_speed(self, newSpeed):
        self._speed = newSpeed

    def update_hp(self, newHp):
        self._hp = newHp

    def update_attack(self, newAttack):
        self._attack = newAttack
