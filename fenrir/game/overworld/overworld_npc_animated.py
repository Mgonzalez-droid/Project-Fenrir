from fenrir.game.overworld.overworld_npc import overworld_npc
from fenrir.game.overworld.Spritesheet import Spritesheet
import pygame

class overworld_npc_animated(overworld_npc):
    def __init__(self, x, y, filename):
        super().__init__(x, y, filename)
        self.__spritesheet = Spritesheet(filename)
        self.__index = 0
        self.__sprite_names = []

    @property
    def spritesheet(self):
        return self.__spritesheet

    @spritesheet.setter
    def spritesheet(self, filename):
        self.__spritesheet = Spritesheet(filename)

    @property
    def sprite_names(self):
        return self.__sprite_names

    @sprite_names.setter
    def sprite_names(self, names):
        for name in names:
            self.__sprite_names.append(self.__spritesheet.parse_sprite(name))

    def adjust_movement(self):
        self.__index = (self.__index + 1) % len(self.__sprite_names)
        self.sprite = self.__sprite_names[self.__index]

    def play_animation(self):
        for sprites in self.__sprite_names:
            self.adjust_movement()
