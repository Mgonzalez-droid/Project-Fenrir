import math


class CombatCharacterData:
    def __init__(self, level, speed, hp, attack, enemy = False):
        self._level = level
        self._speed = speed
        self._hp = hp
        self._attack = attack
        self._enemy = enemy
