import pygame
from fenrir.common.config import *
from fenrir.common.wsl import *


class TextBox:
    show_box = False

    # Load and scale Text box for dialogue
    @staticmethod
    def load_textbox():
        # Load text box png
        text_box = pygame.image.load("../resources/UI/generic-rpg-ui-text-box.png")
        # Scale image to a proper size
        # For now, the text box width is 600 and the height 100
        text_box = pygame.transform.scale(text_box, (600, 100))
        return text_box

    @staticmethod
    def display_textbox(screen, text_box):
        # Print text box
        screen.blit(text_box, (790 - text_box.get_width(), text_box.get_height() + 300))

    # Draw text
    @staticmethod
    def draw_dialogue(screen, text, text_box):
        # text = "This is all the dialogue that I want to display for now so that I can make sure it works"

        # The current text box can take 72 characters per line
        # keys = pygame.key.get_pressed()
        chars_per_line = 71
        lines = [text[i:i + chars_per_line] for i in range(0, len(text), chars_per_line)]
        font = pygame.font.Font(None, 24)
        # line_height is used to make sure the next line of text goes below the one before it
        line_height = 0

        for line in lines:
            dialogue = font.render(line, True, (0, 0, 0))
            screen.blit(dialogue, (200, 407 - line_height))
            # Next line of text will be below the line before it
            line_height = line_height - 16

