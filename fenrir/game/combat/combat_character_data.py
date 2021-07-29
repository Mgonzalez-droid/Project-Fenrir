"""
.. module:: combat_character_data
  :synopsis: module for creating a new character in the combat scenes. Can be ally or enemy
"""

import math
import random


class CombatCharacterData:
    """Class representing individual characters, and their attributes for the combat scene.

    :param char_id: (int) given id value for the new character.
    :param char_type: (string) the class the unit should be set to 'knight','archer', or 'mage'.
    :param level: (int) level for the new character (can be updated later).
    :param enemy: (boolean) determine if character is enemy. Defaults to false.

    Other non-param values:
    :alive: (boolean) for checking if character died.
    :xpos: (int) x pixel coordinate of unit on battlefield.
    :ypos: (int) y pixel coordinate of unit on battlefield.
    :move_range: (int) the distance the unit can move in a battle turn.
    :attack_range: (int) the distance the unit can hit other units from.
    :luck: (int) value provided to the combat system for a chance of an incoming attack to miss.
    :mana: (float) the total amount of energy available to a mage unit.
    :magic_attack: (float) base damage for magic type attacks.
    :magic_defense: (float) base magic defense from magic attacks.
    :defense: (float) base defense from physical type attacks.
    """

    def __init__(self, char_id, char_type, level=1, enemy=False):

        # id info
        self._id = char_id
        self._type = char_type
        self._enemy = enemy
        self._alive = True

        # general character traits
        self._level = level
        self._max_hp = 0
        self._hp = 0
        self._speed = 0
        self._move_range = 0
        self._attack_range = 0
        self._luck = 0
        self._movable_tiles = []
        self._attackable_tiles = []

        # type specific traits
        self._mana = 0
        self._magic_attack = 0
        self._magic_defense = 0
        self._attack = 0
        self._defense = 0

        self.character_class_setup_by_type()

    def get_id(self):
        return self._id

    def get_type(self):
        return self._type

    def get_is_enemy(self):
        return self._enemy

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, newState):
        self._alive = newState

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, newLevel):
        self._level = newLevel

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, newHp):
        self._hp = newHp

    @property
    def max_hp(self):
        return self._max_hp

    @max_hp.setter
    def max_hp(self, newMaxHp):
        self._max_hp = newMaxHp

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, newSpeed):
        self._speed = newSpeed

    @property
    def move_range(self):
        return self._move_range

    @move_range.setter
    def move_range(self, newMoveRange):
        self._move_range = newMoveRange

    @property
    def attack_range(self):
        return self._attack_range

    @attack_range.setter
    def attack_range(self, newAttackRange):
        self._attack_range = newAttackRange

    @property
    def luck(self):
        return self._luck

    @luck.setter
    def luck(self, newLuck):
        self._luck = newLuck

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, newMana):
        self._mana = newMana

    @property
    def magic_attack(self):
        return self._magic_attack

    @magic_attack.setter
    def magic_attack(self, newMagicAttack):
        self._magic_attack = newMagicAttack

    @property
    def magic_defense(self):
        return self._magic_defense

    @magic_defense.setter
    def magic_defense(self, newMagicDefense):
        self._magic_defense = newMagicDefense

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, newAttack):
        self._attack = newAttack

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, newDefense):
        self._defense = newDefense

    @property
    def xpos(self):
        return self.rect.centerx

    @property
    def ypos(self):
        return self.rect.centery

    def character_class_setup_by_type(self):
        """function sets all stats based on given level when character is constructed.
        """
        # All characters have same HP at a given level
        self.max_hp = 75 + (self.level * 25)
        self.hp = self.max_hp

        # Luck increases 1 each level 3 times then freezes 1 level. So luck doesn't change for levels 4, 8, 12, 16,...
        self._luck = math.ceil(self.level * .75)

        # knight move is always 4 and range is always 1
        # archer move is always 1 and range is always 4
        # mage   move is always 2 and range is always 3
        if self._type == 'knight':
            self._move_range = 4
            self._attack_range = 1
            self._attack = 20 + (self.level * 3)
            self._defense = 10 + (self.level * 7)
            self._speed = 5 + (self.level * 5)
        elif self._type == 'archer':
            self.move_range = 2
            self.attack_range = 4
            self.attack = 10 + (self.level * 5)
            self.defense = 20 + (self.level * 5)
            self._speed = 20 + (self.level * 5)
        elif self._type == 'mage':
            self.move_range = 2
            self.attack_range = 3
            self.magic_attack = 15 + (self.level * 7)
            self.magic_defense = 15 + (self.level * 3)
            self._speed = 15 + (self.level * 5)

        if self.get_is_enemy():
            self.attack = self.attack + (math.ceil(self.level/5) - 1) * 2
            self.defense = self.defense + (math.ceil(self.level/5) - 1) * 2
            self.magic_attack = self.magic_attack + (math.ceil(self.level/5) - 1) * 2
            self.magic_defense = self.magic_defense + (math.ceil(self.level/5) - 1) * 2
            self.max_hp = self.max_hp + (math.ceil(self.level/5) - 1) * 5
            self.hp = self.max_hp

    def check_if_incoming_attack_misses(self, incomingAttackValue):
        """function to calculate chance that an attack misses the character (calculated value must be less than 2 to miss)
        """
        # TODO this function needs to be reworked to scale correctly
        attackModifier = (incomingAttackValue / 100) * 1.5
        chanceTheyMissed = random.uniform(0, 10) + attackModifier + (self.luck / 5)
        if chanceTheyMissed <= 2 * self.luck:
            return True
        return False

    def take_damage(self, incomingAttackValue, attackType):
        """Calculate the damage an incoming attack does on the character and update the hp value. Returns 0, 1 or 2 for
        miss, hit or critical hit respectively.
        """
        damage = incomingAttackValue
        if attackType == 'magic' and self._type == "mage":
            damage = damage - math.floor(self.magic_defense / 2)
        elif attackType == 'physical':
            damage = damage - math.floor(self.defense / 2)
        # didTheyMiss = self.check_if_incoming_attack_misses(damage)
        if damage < 5:
            damage = 5
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False


