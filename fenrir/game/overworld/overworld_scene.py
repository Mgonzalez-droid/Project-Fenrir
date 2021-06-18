""" Template module

"""
import os

import pygame
from fenrir.common.scene import Scene
from fenrir.common.config import Colors, PATH_TO_RESOURCES


class OverworldScene(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.background = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "demo_overworld.png"))

    def handle_event(self, event):
        """Example event handling. Will return to main menu if you

        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                from fenrir.game.menu.menu_scene import MainMenuScene
                self.switch_to_scene(MainMenuScene(self.screen))

    def render(self):
        self.screen.fill(Colors.WHITE.value)
        self.screen.blit(self.background, (0, 0))

    def update(self):
        pass

    """NOTE: To switch to another scene like main menu or combat scene you enter the following
        to combat: self.switch_to_scene(CombatScene(self.screen))
        to main menu: self.switch_to_scene(MainMenuScene(self.screen))
    
    """
