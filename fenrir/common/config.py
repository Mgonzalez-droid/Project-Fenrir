"""Common configurations for the game that can be reused throughout and changed in
central location
"""

from enum import Enum

# screen resolution for game to be displayed, set in app.py
SCREEN_RESOLUTION = (960, 540)
CENTER_X = SCREEN_RESOLUTION[0] / 2  # center x value of screen
CENTER_Y = SCREEN_RESOLUTION[1] / 2  # center y value of screen


class Colors(Enum):
    """Returns common colors defined with RGB values. This will allow a central location to
    change game themes and color schemes. can add things like MENU_COLOR, BACKGROUND_COLOR
    and more to keep themes consistent.
    After import call with Colors.White.value or whatever color
    """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    # add colors here with RGB values the list will lengthen as we go
