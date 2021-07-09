"""Common configurations for the game that can be reused throughout and changed in
central location
"""
import os
from enum import Enum

GAME_TITLE = "Project Fenrir"

PATH_TO_RESOURCES = os.path.join("fenrir", "resources")


# screen resolution for game to be displayed, set in app.py
class DisplaySettings(Enum):
    """Returns common colors defined with RGB values. This will allow a central location to
        change game themes and color schemes. can add things like MENU_COLOR, BACKGROUND_COLOR
        and more to keep themes consistent.
        After import call with Colors.White.value or whatever color
    """

    SCREEN_RESOLUTION = (960, 540)
    FPS = 30
    CENTER_WIDTH = SCREEN_RESOLUTION[0] / 2  # center x value of screen
    CENTER_HEIGHT = SCREEN_RESOLUTION[1] / 2  # center y value of screen


class Colors(Enum):
    """Returns common colors defined with RGB values. This will allow a central location to
    change game themes and color schemes. can add things like MENU_COLOR, BACKGROUND_COLOR
    and more to keep themes consistent.
    After import call with Colors.White.value or whatever color
    """

    ALPHA = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # add colors here with RGB values the list will lengthen as we go
