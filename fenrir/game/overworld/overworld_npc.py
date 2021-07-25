import pygame
from fenrir.game.overworld.Spritesheet import Spritesheet


class overworld_npc:
    def __init__(self, x, y,  filename, level, party, is_choice, dialogue):
        self.__x = x
        self.__y = y
        self.__sprite = pygame.image.load(filename)
        self.__level = level
        self.__party = party
        self.__is_choice = is_choice
        self.__dialogue = dialogue

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def sprite(self):
        return self.__sprite

    @sprite.setter
    def sprite(self, sprite):
        self.__sprite = sprite

    def scale_sprite(self, x, y):
        self.sprite = pygame.transform.scale(self.sprite, (x, y))
        # self.sprite = pygame.transform.scale(self.sprite, (75, 75))

    def flip_sprite(self, left, flip):
        self.sprite = pygame.transform.flip(self.sprite, left, flip)
        # self.sprite = pygame.transform.flip(self.sprite, True, False)

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level):
        self.__level = level

    @property
    def party(self):
        return self.__party

    @party.setter
    def party(self, party):
        self.__party = party

    @property
    def is_choice(self):
        return self.__is_choice

    @is_choice.setter
    def is_choice(self, is_choice):
        self.__is_choice = is_choice

    @property
    def dialogue(self):
        return self.__dialogue

    @dialogue.setter
    def dialogue(self, dialogue):
        self.__dialogue = dialogue
