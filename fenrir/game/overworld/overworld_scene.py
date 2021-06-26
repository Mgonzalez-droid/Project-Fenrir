"""Overworld module. Add class properties and args to constructor to change this to diff levels or starting points, etc

"""
import os
import pygame
import fenrir.game.menu.menu_scene as menuscene
from fenrir.common.scene import Scene
from fenrir.common.config import Colors, PATH_TO_RESOURCES
from fenrir.common.TextBox import TextBox
from fenrir.game.overworld.overworld_npc import overworld_npc as character
from fenrir.game.overworld.overworld_npc_animated import overworld_npc_animated as character_animated
from fenrir.game.overworld.overworld_boundaries import Boundaries


class OverworldScene(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.background = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "overworld_resized_controls.png"))
        self.hero = character_animated(560, 170, os.path.join(PATH_TO_RESOURCES, "gabe_running.png"))
        self.hero.sprite_names = ["gabe_stance_1.png", "gabe_stance_2.png", "gabe_stance_3.png", "gabe_stance_4.png",
                                  "gabe_stance_5.png", "gabe_stance_6.png", "gabe_stance_7.png"]

        self.npc = character(890, 230, os.path.join(PATH_TO_RESOURCES, "Resized_Sensei.png"))
        self.exclamation_mark = character(860, 170, os.path.join(PATH_TO_RESOURCES, "exclamation.png"))
        self.exclamation_mark.sprite = pygame.transform.scale(self.exclamation_mark.sprite, (100, 100))
        self.show_controls = False
        self.show_characters = True
        self.combat_phase = False
        self.show_interaction = False
        self.show_textbox = False

    def handle_event(self, event):
        """Example event handling. Will return to main menu if you

        """
        # TRACK MOVEMENT
        # Boundaries class prevent the player character to move outside the current window
        boundaries = Boundaries(self.screen, self.hero)

        # Player check player movement for up (w), down (s), left (a), right (d)
        keys = pygame.key.get_pressed()
        if not self.show_controls and not self.show_textbox:
            if keys[pygame.K_w]:
                self.hero.y = boundaries.collision_up()  # Check if player hits top of window
                self.hero.adjust_movement()
            if keys[pygame.K_s]:
                self.hero.y = boundaries.collision_down()  # Check if player hits bottom of window
                self.hero.adjust_movement()
            if keys[pygame.K_a]:
                self.hero.x = boundaries.collision_left()  # Check if player hits left of window
                self.hero.adjust_movement()
            if keys[pygame.K_d]:
                self.hero.x = boundaries.collision_right()  # Check if player hits right of window
                self.hero.adjust_movement()

        # Check of collision
        if (820 <= self.hero.x <= 900) and (190 <= self.hero.y <= 250):
            # Show exclamation mark
            self.show_interaction = True

        # TRACK INTERACTION
        if event.type == pygame.KEYDOWN:  # Press Enter or Esc to go back to the Main Menu
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_ESCAPE:
                self.switch_to_scene(menuscene.MainMenuScene(self.screen))

            if event.key == pygame.K_q:  # Press q to open/close controls menu
                if self.show_controls:
                    self.background = pygame.image.load(
                        os.path.join(PATH_TO_RESOURCES, "overworld_resized_controls.png"))
                    self.show_controls = False
                    self.show_characters = True
                else:
                    self.background = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "Simple_Control_menu.png"))
                    self.show_controls = True
                    self.show_characters = False

            if event.key == pygame.K_SPACE and not self.show_controls:  # Checks if the space bar is pressed
                # Check for collision
                if (820 <= self.hero.x <= 900) and (190 <= self.hero.y <= 250):
                    # if text box is displayed, stop characters movements
                    self.show_textbox = True

            # Select options from the text box
            if event.key == pygame.K_1 and self.show_textbox:
                print("Going to combat phase")
            if event.key == pygame.K_2 and self.show_textbox:
                self.show_textbox = False

    def render(self):
        # print("hero coordinates: ", end='')
        # print(self.hero.x, end='')
        # print(self.hero.y)
        self.screen.fill(Colors.WHITE.value)
        self.screen.blit(self.background, (0, 0))
        self.hero.play_animation()

        if self.show_characters:  # Display hero and npcs
            self.screen.blit(self.hero.sprite, (self.hero.x, self.hero.y))
            self.screen.blit(self.npc.sprite, (self.npc.x, self.npc.y))

        if self.show_interaction:  # Show if you can interact with and npc
            self.screen.blit(self.exclamation_mark.sprite, (self.exclamation_mark.x, self.exclamation_mark.y))

        if self.show_textbox:  # Draw Text box
            textbox = TextBox(self.screen)
            TextBox.load_textbox(textbox)
            options = ["[1] Yes, I am ready to go to the combat phase",
                       "[2] No, I want to keep walking here"]
            size = 24
            x = 200
            y = 397
            # Text box were the user must pick and option
            TextBox.draw_options(textbox, "Hello Gabe, do you wanna go to the combat phase?", options, size, x, y)

    def update(self):
        pass

    """NOTE: To switch to another scene like main menu or combat scene you enter the following
        to combat: self.switch_to_scene(CombatScene(self.screen))
        to main menu: self.switch_to_scene(MainMenuScene(self.screen))
    
    """
