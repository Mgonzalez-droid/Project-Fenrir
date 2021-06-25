"""Overworld module. Add class properties and args to constructor to change this to diff levels or starting points, etc

"""
import os

from fenrir.game.overworld.overworld_npc import overworld_npc as character
from fenrir.game.overworld.overworld_npc_animated import  overworld_npc_animated as character_animated

import pygame

import fenrir.game.menu.menu_scene as menuscene
from fenrir.common.scene import Scene
from fenrir.common.config import Colors, PATH_TO_RESOURCES


class OverworldScene(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.background = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "overworld_resized_controls.png"))
        self.hero = character_animated(560, 170, os.path.join(PATH_TO_RESOURCES, "gabe_running.png"))
        self.hero.sprite_names = ["gabe_stance_1.png", "gabe_stance_2.png", "gabe_stance_3.png", "gabe_stance_4.png",
                                  "gabe_stance_5.png", "gabe_stance_6.png", "gabe_stance_7.png"]
        self.npc = character(890, 230, os.path.join(PATH_TO_RESOURCES, "Resized_Sensei.png"))
        self.in_controls = False
        self.show_characters = True

    def handle_event(self, event):
        """Example event handling. Will return to main menu if you

        """
        ## Track Movement ##
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.hero.y -= 10
            #self.hero.play_animation()
            self.hero.adjust_movement()
        if keys[pygame.K_s]:
            self.hero.y += 10
            #self.hero.play_animation()
            self.hero.adjust_movement()
        if keys[pygame.K_a]:
            self.hero.x -= 10
            #self.hero.play_animation()
            self.hero.adjust_movement()
        if keys[pygame.K_d]:
            self.hero.x += 10
            #self.hero.play_animation()
            self.hero.adjust_movement()

        ## Track Interaction ##
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.switch_to_scene(menuscene.MainMenuScene(self.screen))
            if event.key == pygame.K_q:
                if self.in_controls:
                    self.background = pygame.image.load(
                        os.path.join(PATH_TO_RESOURCES, "overworld_resized_controls.png"))
                    self.in_controls = False
                    self.show_characters = True
                else:
                    self.background = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "Simple_Control_menu.png"))
                    self.in_controls = True
                    self.show_characters = False

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
        if self.show_characters:
            self.screen.blit(self.hero.sprite, (self.hero.x, self.hero.y))
            self.screen.blit(self.npc.sprite, (self.npc.x, self.npc.y))

    def update(self):
        pass

    """NOTE: To switch to another scene like main menu or combat scene you enter the following
        to combat: self.switch_to_scene(CombatScene(self.screen))
        to main menu: self.switch_to_scene(MainMenuScene(self.screen))
    
    """
