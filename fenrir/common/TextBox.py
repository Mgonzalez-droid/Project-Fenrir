import pygame
import os
from fenrir.common.config import *


class TextBox:

    def __init__(self, screen):
        self.screen = screen

        # Default TextBox values
        self.text_box = " "
        self.text_box_x_scale = 600
        self.text_box_y_scale = 100

    # Load and scale Text box for dialogue
    def load_textbox(self):
        # Load text box png
        self.text_box = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "UI/generic-rpg-ui-text-box.png"))

        # Default Text box position on window
        text_box_x_pos = 300 - self.text_box.get_width()
        text_box_y_pos = self.text_box.get_height() + 370

        # Scale image to a proper size
        text_box = pygame.transform.scale(self.text_box, (self.text_box_x_scale, self.text_box_y_scale))

        # Display on window
        self.screen.blit(text_box, (text_box_x_pos, text_box_y_pos))

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
