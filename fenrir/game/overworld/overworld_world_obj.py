import os
import pygame
from fenrir.common.config import Colors, PATH_TO_RESOURCES
from fenrir.game.overworld.overworld_obstacle import overworld_obstacle as obstacle
from fenrir.game.overworld.overworld_npc import overworld_npc as character


class overworld_world_obj:
    def __init__(self, obstacles, entries, entry_dests, npc, hero_spawn, background, music, visited=False):
        self.__obstacles = obstacles
        self.__entries = entries
        self.__entry_dests = entry_dests
        self.__npc = npc
        self.__hero_spawn = hero_spawn
        self.__background = background
        self.__music = music
        self.__visited = visited

    @property
    def obstacles(self):
        return self.__obstacles

    @obstacles.setter
    def obstacles(self, obstacles):
        self.__obstacles = obstacles

    @property
    def entries(self):
        return self.__entries

    @entries.setter
    def entries(self, entries):
        self.__entries = entries

    @property
    def entry_dests(self):
        return self.__entry_dests

    @entry_dests.setter
    def entry_dests(self, entry_dests):
        self.__entry_dests = entry_dests

    @property
    def npc(self):
        return self.__npc

    @npc.setter
    def npc(self, npc):
        self.__npc = npc

    @property
    def hero_spawn(self):
        return self.__hero_spawn

    @hero_spawn.setter
    def hero_spawn(self, hero_spawn):
        self.__hero_spawn = hero_spawn

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, background):
        self.__background = background

    @property
    def music(self):
        return self.__music

    @music.setter
    def music(self, music):
        self.__music = music

    @property
    def visited(self):
        return self.__visited

    @visited.setter
    def visited(self, visited):
        self.__visited = visited
