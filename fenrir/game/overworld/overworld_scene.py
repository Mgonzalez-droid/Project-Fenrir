"""Overworld module. Add class properties and args to constructor to change this to diff levels or starting points, etc

"""
import os

from fenrir.game.overworld.overworld_npc import overworld_npc as character

import pygame

import fenrir.game.menu.menu_scene as menuscene
from fenrir.common.scene import Scene
from fenrir.common.config import Colors, PATH_TO_RESOURCES


class OverworldScene(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.background = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "demo_overworld.png"))
        self.hero = character(0, 0, pygame.image.load(os.path.join(PATH_TO_RESOURCES, "gabe-idle-run 2.png")))
        self.npc = character(0, 0, pygame.image.load(os.path.join("fenrir/resources/chars/sensei/sensei.png")))

    def handle_event(self, event):
        """Example event handling. Will return to main menu if you

        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.switch_to_scene(menuscene.MainMenuScene(self.screen))
            if event.key == pygame.K_q:
                print("Entered menu")
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                #print("+10 in y direction")
                self.hero.y += 10
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                #print("-10 in y direction")
                self.hero.y -= 10
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                #print("-10 in x direction")
                self.hero.x -= 10
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                #print("+10 in x direction")
                self.hero.x += 10
            if event.key == pygame.K_SPACE:
                print("scan for interaction")
                # try to interact with object
                # if object.interactable
                # initiate_battle = load_dialogue()
                # if initiate_battle
                # self.switch_to_scene(CombatScene(self.screen))

    def render(self):
        print("hero coordinates: ", end='')
        print(self.hero.x, end='')
        print(self.hero.y)
        self.screen.fill(Colors.WHITE.value)
        self.screen.blit(self.background, (0, 0))
        #render character

    def update(self):
        pass

    """NOTE: To switch to another scene like main menu or combat scene you enter the following
        to combat: self.switch_to_scene(CombatScene(self.screen))
        to main menu: self.switch_to_scene(MainMenuScene(self.screen))
    
    """
