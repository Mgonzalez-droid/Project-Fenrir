"""
.. module:: combat_character_data
  :synopsis: module for creating a new character in the combat scenes. Can be ally or enemy
"""

import math


class CombatCharacterData:
    """Class representing individual characters, and their attributes for the combat scenes

    :param id: given id value for the new character
    :param type: the class the unit should be set to knight/archer/mage
    :param level: level for the new character (can be updated later)
    :param hp: hp for the new character (can be updated later)
    :param speed: speed/initiative value for the new character (can be updated later)
    :param attack: base attack value for new character (can be updated later)
    :param enemy: boolean to determine if character is enemy. Defaults to false

    Other non-param values:
    :move_range: the distance the unit can move in a battle
    :attack_range: the distance the unit can hit other units from
    :mana: the total amount of energy available to a mage unit
    :magic_attack: base damage for magic type attacks
    :magic_defense: base magic defense from magic attacks
    :defense: base defense from physical type attacks
    """

    def __init__(self, id, type, level, hp, speed, attack, enemy=False):
        # id info
        self._id = id
        self._type = type
        self._enemy = enemy

        # general character traits
        self._level = level
        self._hp = hp
        self._speed = speed
        self._move_range = 0
        self._attack_range = 0

        # type specific traits
        self._mana = 0
        self._magic_attack = 0
        self._magic_defense = 0
        self._attack = attack
        self._defense = 0

        self.character_class_setup_by_type()

    def get_id(self):
        return self._id

    def get_type(self):
        return self._type

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

    def character_class_setup_by_type(self):
        # function sets non-defined traits based on given info when character is constructed

        if self._type == 'knight':
            self._attack_range = 1
            self._move_range = 3
            self._defense = self._attack - 1
        elif self._type == 'archer':
            self._attack_range = 4
            self._move_range = 1
            self._defense = self._attack - 3
            if self._enemy:
                self._defense = self._attack - 2
        elif self._type == 'mage':
            self._attack_range = 3
            self._move_range = 2
            self._magic_attack = self._attack
            self._attack = 1
            self._magic_defense = self._magic_attack - 1
            self._mana = math.floor(self._level * 2.5)
            if self._enemy:
                self._magic_defense = self._magic_attack
                self._mana = self._level * 3
