"""Common configurations for the game that can be reused throughout and changed in
central location
"""
import os
import sys
from enum import Enum

GAME_TITLE = "Project Fenrir"


def find_abs_file_path():
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.join(os.path.dirname(sys.executable), 'lib')
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return datadir


abs_path = find_abs_file_path()

PATH_TO_RESOURCES = os.path.join(abs_path, "fenrir", "resources")
PATH_TO_DATABASE = os.path.join(abs_path, "db", "fenrir.db")


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
    GREEN = (0, 128, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GRID_GRAY = (88, 88, 88)

    # add colors here with RGB values the list will lengthen as we go


class GameConstants(Enum):
    """Constant values for game play to be used throughout
    """

    # the current max level any player can reach in the game
    MAX_LEVEL = 6
