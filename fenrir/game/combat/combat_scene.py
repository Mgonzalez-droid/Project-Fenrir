""" .. module:: scene
    :synopsis: Module will load combat mode into game

"""
import os
import pygame
from fenrir.common.scene import Scene
import fenrir.game.menu.menu_scene as menuscene
import fenrir.game.combat.combat_map_data as md
from fenrir.common.config import Colors, PATH_TO_RESOURCES


class CombatScene(Scene):

    def __init__(self, screen, map_name):
        super().__init__(screen)
        self._map_name = map_name
        self._map = md.MapData(map_name, 20, 10)
        self._background = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "combat_maps", str(map_name + ".png")))

    def handle_event(self, event):
        """Example event handling. Will return to main menu if you

        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.switch_to_scene(menuscene.MainMenuScene(self.screen))

    def render(self):
        self.screen.fill(Colors.WHITE.value)
        self.screen.blit(self._background, (0, 0))

    def update(self):
        pass
