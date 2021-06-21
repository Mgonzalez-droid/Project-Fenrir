"""
.. module:: combat_character_data
  :synopsis: module for creating a new character in the combat scenes. Can be ally or enemy
"""

import math
import pygame
import random


class CombatCharacterData:
    """Class representing individual characters, and their attributes for the combat scenes

    :param id: (int) given id value for the new character
    :param type: (string) the class the unit should be set to knight/archer/mage
    :param level: (int) level for the new character (can be updated later)
    :param hp: (float) hp for the new character (can be updated later)
    :param speed: (float) speed/initiative value for the new character (can be updated later)
    :param attack: (float) base attack value for new character (can be updated later)
    :param enemy: (boolean) determine if character is enemy. Defaults to false

    Other non-param values:
    :alive: (boolean) for checking if character died
    :xpos: (int) x coordinate of unit on battlefield
    :ypos: (int) y coordinate of unit on battlefield
    :sprite_sheet: (image) images that the character is pulled from
    :character_image: (image) single image of the character
    :move_range: (int) the distance the unit can move in a battle
    :attack_range: (int) the distance the unit can hit other units from
    :luck: (int) value provided to the combat system for a chance of an incoming attack to miss
    :mana: (float) the total amount of energy available to a mage unit
    :magic_attack: (float) base damage for magic type attacks
    :magic_defense: (float) base magic defense from magic attacks
    :defense: (float) base defense from physical type attacks
    """

    def __init__(self, id, type, level, hp, speed, attack, enemy=False):
        # id info
        self._id = id
        self._type = type
        self._enemy = enemy
        self._alive = True
        self._xpos = 0
        self._ypos = 0
        self.sprite_sheet = None
        self._character_image = None

        # general character traits
        self._level = level
        self._hp = hp
        self._speed = speed
        self._move_range = 0
        self._attack_range = 0
        self._luck = 1

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

    def get_is_enemy(self):
        return self._enemy

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, newState):
        self._alive = newState

    @property
    def xpos(self):
        return self._xpos

    @xpos.setter
    def xpos(self, newXPos):
        self._xpos = newXPos

    @property
    def ypos(self):
        return self._ypos

    @ypos.setter
    def ypos(self, newYPos):
        self._ypos = newYPos

    def set_character_image(self):
        if self._type == 'knight':
            self.sprite_sheet = pygame.image.load("../../resources/chars/gabe/gabe-idle-run.png").convert()
        else:
            self.sprite_sheet = pygame.image.load("../../resources/chars/gabe/gabe-idle-run.png").convert()

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

    def character_class_setup_by_type(self):
        """function sets non-defined traits based on given info when character is constructed
        """
        if self._type == 'knight':
            self.attack_range = 1
            self.move_range = 3
            self.defense = self.attack - 1
        elif self._type == 'archer':
            self.attack_range = 4
            self.move_range = 1
            self.defense = self.attack - 3
            if self._enemy:
                self.defense = self.attack - 2
        elif self._type == 'mage':
            self.attack_range = 3
            self.move_range = 2
            self.magic_attack = self.attack
            self.attack = 1
            self.magic_defense = self.magic_attack - 1
            self.mana = math.floor(self.level * 2.5)
            if self._enemy:
                self.magic_defense = self.magic_attack
                self.mana = self.level * 3

    def check_if_incoming_attack_misses(self, incomingAttackValue, attackType):
        """function to calculate chance that an attack misses the character (calculated value must be less than 2 to miss)
        """
        attackModifier = incomingAttackValue / 100
        if attackType == 'magic':
            attackModifier *= 2
        else:
            attackModifier *= 1.5
        chanceTheyMissed = random.uniform(0, 10) + attackModifier - (self.luck / 5)
        if chanceTheyMissed <= 2:
            return True
        return False

    def take_damage(self, incomingAttackValue, attackType):
        """Calculate the damage an incoming attack does on the character and update the hp value. Returns 0, 1 or 2 for
        miss, hit or critical hit respectively.
        """
        damage = 0
        if attackType == 'magic':
            damage = incomingAttackValue - self.magic_defense
        elif attackType == 'physical':
            damage = incomingAttackValue - self.defense
        didTheyMiss = self.check_if_incoming_attack_misses(incomingAttackValue, attackType)
        if not didTheyMiss:
            damageSuccess = 1
            self.hp -= damage
            if self.hp <= 0:
                self.hp = 0
                self.alive = False
                damageSuccess = 2
        else:
            damageSuccess = 0
        return damageSuccess
