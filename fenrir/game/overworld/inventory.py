import os
import pygame
from fenrir.common.TextBox import TextBox


class Inventory:
    def __init__(self, textbox, current_party, all_heroes):
        self.textbox = textbox

        self.party = current_party
        self.party_displayed = [False, False, False, False]

        self.heroes = all_heroes
        self.heroes_displayed = [False, False, False, False, False, False, False, False, False, False]

        self.__inventory_tile_x = [332, 317]
        self.__inventory_tile_y = [187, 298]
        self.__inventory_tile_pos = [0, 0]
        self.swapping = False

    # Display inventory background image box, character tiles and instruction text
    def display_inventory(self):
        self.textbox.load_image(190, 60, 600, 400, "UI/hero_system_model.png")

        self.textbox.draw_dialogue("Current Party", 30, 305, 160)
        self.textbox.draw_dialogue("Heroes", 30, 450, 270)

        self.textbox.draw_dialogue("Press space bar to add/remove selected", 24, 260, 360)
        self.textbox.draw_dialogue(" hero from current party.", 24, 255, 390)

    def display_heroes(self, party, heroes):

        # Set position were characters sprite will be displayed for the party and heroes sections
        party_x = 160
        party_y = 95
        heroes_x = 142
        heroes_y = 206

        self.display_section(party_x, party_y, party, 0)
        self.display_section(heroes_x, heroes_y, heroes, 1)

    # Display heroes sprites inside inventory tiles
    def display_section(self, x, y, section, index):

        displayed = []

        # Display characters in the current party section
        for i in range(len(section)):
            self.textbox.load_image(x, y, 350, 250, section[i][1])
            x += 40
            displayed.append(True)

        # Set tiles with no characters to false
        if index == 0:  # Party section
            for i in range(len(section), len(self.party_displayed)):
                displayed.append(False)
            self.party_displayed = displayed

        else:  # Heroes section
            for i in range(len(section), len(self.heroes_displayed)):
                displayed.append(False)
            self.heroes_displayed = displayed

    # Change the position of the tile the user is selecting
    def character_selection(self, index, tiles_num):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.tile_pos[index] < tiles_num:
            self.tile_x[index] = 40 + self.tile_x[index]  # Distance between boxes x = 40
            self.tile_pos[index] += 1

        if keys[pygame.K_LEFT] and self.tile_pos[index] > 0:
            self.tile_x[index] -= 40
            self.tile_pos[index] -= 1

    # Displays tile the user is selecting
    def display_selection(self, index):
        self.textbox.load_image(self.tile_x[index], self.tile_y[index], 35, 39, "UI/generic-rpg-ui-inventario01.png")

    # Swap characters in current party to the one selected in the heroes section
    def swap_characters(self, party_index, hero_index):

        party_hero = self.heroes[int(hero_index)]
        return party_hero

    def add_to_party(self, hero):

        self.party.append(hero)
        # self.heroes.remove(hero)

        return self.party, self.heroes

    @property
    def tile_x(self):
        return self.__inventory_tile_x

    @tile_x.setter
    def tile_x(self, x):
        self.__inventory_tile_x = x

    @property
    def tile_y(self):
        return self.__inventory_tile_y

    @tile_y.setter
    def tile_y(self, y):
        self.__inventory_tile_y = y

    @property
    def tile_pos(self):
        return self.__inventory_tile_pos

    @tile_pos.setter
    def tile_pos(self, pos):
        self.__inventory_tile_pos = pos
