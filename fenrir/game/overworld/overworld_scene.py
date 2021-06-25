"""Overworld module. Add class properties and args to constructor to change this to diff levels or starting points, etc

"""
import os

import pygame

import fenrir.game.menu.menu_scene as menuscene
from fenrir.common.scene import Scene
from fenrir.common.config import Colors, PATH_TO_RESOURCES
from fenrir.game.overworld.TextBox import TextBox


class OverworldScene(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.background = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "demo_overworld.png"))
        self.show_textbox = False

    def handle_event(self, event):
        """Example event handling. Will return to main menu if you

        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.switch_to_scene(menuscene.MainMenuScene(self.screen))
            if event.key == pygame.K_SPACE:
                self.show_textbox = True
            if event.key == pygame.K_1 and self.show_textbox:
                print("Going to combat phase")
            if event.key == pygame.K_2 and self.show_textbox:
                self.show_textbox = False

    def render(self):
        self.screen.fill(Colors.WHITE.value)
        self.screen.blit(self.background, (0, 0))

        if self.show_textbox:
            tb = TextBox(self.screen)
            TextBox.load_textbox(tb)
            options = ["[1] Yes, I want to enter to combat phase", "[2] No, I want to keep walking around"]
            size = 24
            x = 200
            y = 397
            TextBox.draw_options(tb, "Do you want to enter combat phase?", options, size, x, y)

    def update(self):
        pass

    """NOTE: To switch to another scene like main menu or combat scene you enter the following
        to combat: self.switch_to_scene(CombatScene(self.screen))
        to main menu: self.switch_to_scene(MainMenuScene(self.screen))
    
    """
