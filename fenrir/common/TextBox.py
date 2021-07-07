import pygame
import os
from fenrir.common.config import *
from fenrir.common.wsl import *


class TextBox:

    def __init__(self, screen):
        self.screen = screen

        # Default TextBox values
        self.text_box = " "

    # Load and scale Text box for dialogue
    def load_textbox(self, x_pos, y_pos, x_scale, y_scale):
        # Load text box png
        self.text_box = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "UI/generic-rpg-ui-text-box.png"))

        # Default Text box position on window
        if x_pos > self.text_box.get_width() and y_pos > self.text_box.get_height():
            textbox_x_pos = x_pos - self.text_box.get_width()
            textbox_y_pos = self.text_box.get_height() + y_pos
        else:
            textbox_x_pos = x_pos
            textbox_y_pos = y_pos

        # Scale image to a proper size
        if x_scale > 0 and y_scale > 0:
            self.text_box = pygame.transform.scale(self.text_box, (x_scale, y_scale))

        # Display on window
        self.screen.blit(self.text_box, (textbox_x_pos, textbox_y_pos))

    # Draw text
    def draw_dialogue(self, text, size, x, y):
        # The current text box can take 72 characters per line
        # keys = pygame.key.get_pressed()
        chars_per_line = 71
        lines = [text[i:i + chars_per_line] for i in range(0, len(text), chars_per_line)]
        font = pygame.font.Font(os.path.join(PATH_TO_RESOURCES, "fonts/Peepo.ttf"), size)

        # line_height is used to make sure the next line of text goes below the one before it
        line_height = 0

        for line in lines:
            dialogue = font.render(line, True, (0, 0, 0))
            self.screen.blit(dialogue, (x, y - line_height))
            # Next line of text will be below the line before it
            line_height = line_height - 16

    # Draws a questions and several choices for the player to pick
    def draw_options(self, question, options, size, x, y):

        # Draw question inside text box
        self.draw_dialogue(question, size, x, y)

        # Draw the available options in the screen
        x = x + 35
        y = y + 30
        line_height = 0
        for option in options:
            self.draw_dialogue(option, size, x, y - line_height)
            line_height = line_height - 25

    # Draws the current level of the player
    def draw_level(self, text, level, size, x, y):

        self.draw_dialogue(text + " " + str(level), size, x, y)
