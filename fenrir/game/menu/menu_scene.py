import pygame
from fenrir.common.scene import Scene
import fenrir.game.overworld.overworld_scene as oscene
from fenrir.common.config import *


class MenuScene(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        # default variables that will be implemented in subclasses
        self._menu_title = ""  # title attr
        self._menu_items = []  # menu items that work with cursor
        self.menu_item_rects = []  # used for cursor placement and possible collision detection for mouse events (todo)
        self.cursor_pos = 0  # initial pos of cursor on first menu option

        # default alignment values
        self.menu_item_spacer = 60
        self.starting_height = DisplaySettings.CENTER_HEIGHT.value - self.menu_item_spacer  # starting point for menu

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.move_cursor("DOWN")
            elif event.key == pygame.K_UP:
                self.move_cursor("UP")
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.select_menu_item(self.cursor_pos)

    def render(self):
        pass

    def draw_text_to_screen(self, text, size, x, y, rect_index=None):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, Colors.WHITE.value)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)

        # this will init the menu item rects if not done yet, only runs once
        if rect_index is not None and len(self.menu_item_rects) < len(self._menu_items):
            self.menu_item_rects.append(text_rect.copy())

        self.screen.blit(text_surface, text_rect)

    def draw_title(self):
        self.draw_text_to_screen(self._menu_title, 100, DisplaySettings.CENTER_WIDTH.value,
                                 DisplaySettings.CENTER_HEIGHT.value - (self.menu_item_spacer * 3))

    def draw_cursor(self):
        rect = self.menu_item_rects[self.cursor_pos]
        pos_left = rect.midleft
        self.draw_text_to_screen("X", 30, pos_left[0] - 35, pos_left[1])

    def display_menu_items(self, start_height):

        i = 0
        for item in self._menu_items:
            self.draw_text_to_screen(item, 50, DisplaySettings.CENTER_WIDTH.value,
                                     start_height + (i * self.menu_item_spacer), i)
            i += 1

    def move_cursor(self, direction):
        if direction == "DOWN":
            if self.cursor_pos != len(self.menu_item_rects) - 1:
                self.cursor_pos += 1
        elif direction == "UP":
            if self.cursor_pos != 0:
                self.cursor_pos -= 1


class MainMenuScene(MenuScene):

    def __init__(self, screen):
        super().__init__(screen)
        self._menu_title = "Project Fenrir"
        self._menu_items = ["New Game", "Load Game", "Credits", "Exit"]
        self._highlighted_items = [False for item in self._menu_items]


    def update(self):
        pass

    def render(self):
        self.screen.fill(Colors.BLACK.value)
        self.draw_title()
        self.display_menu_items(self.starting_height)
        self.draw_cursor()

    def select_menu_item(self, index):
        if index == 0:
            self.switch_to_scene(NewGameScene(self.screen))
        elif index == 1:
            self.switch_to_scene(LoadGameScene(self.screen))
        elif index == 2:
            self.switch_to_scene(CreditsScene(self.screen))
        elif index == 3:
            self.terminate()


class LoadGameScene(MenuScene):

    def __init__(self, screen):
        super().__init__(screen)
        self._menu_title = "Saved Games"
        self._saved_games = []
        self._menu_items = []
        self.populate_menu_items()

    def populate_menu_items(self):
        if self._saved_games:
            for save in self._saved_games:
                self._menu_items.append(save.title)
        else:
            self.starting_height = DisplaySettings.SCREEN_RESOLUTION.value[1] - 50
        self._menu_items.append("Main Menu")

    def update(self):
        pass

    def render(self):
        self.screen.fill(Colors.BLACK.value)
        self.draw_title()
        self.display_menu_items(self.starting_height)
        self.draw_cursor()

    def select_menu_item(self, index):
        if not self._saved_games:
            self.switch_to_scene(MainMenuScene(self.screen))
        else:
            if index == len(self._saved_games):
                self.switch_to_scene(MainMenuScene(self.screen))
            else:
                # this is where game will be loaded
                pass


class CreditsScene(MenuScene):

    def __init__(self, screen):
        super().__init__(screen)
        self._menu_title = "Credits"
        self._credit_names = ["Barry Congressi", "Bryan Kristofferson", "Michel Gonzalez",
                              "Roberto Rafael Edde Verde", "Victor Sotomayor"]
        self._menu_items = ["Main Menu"]
        self._menu_start_height = DisplaySettings.SCREEN_RESOLUTION.value[1] - 100  # bottom of screen

    def render(self):
        self.screen.fill(Colors.BLACK.value)
        self.draw_title()
        self.draw_names()
        self.display_menu_items(self._menu_start_height + 50)
        self.draw_cursor()

    def draw_names(self):
        starting_height = self.starting_height - self.menu_item_spacer

        i = 0
        for name in self._credit_names:
            self.draw_text_to_screen(name, 35, DisplaySettings.CENTER_WIDTH.value,
                                     starting_height + (i * self.menu_item_spacer))
            i += 1

    def update(self):
        pass

    def select_menu_item(self, index):
        if index == 0:
            self.switch_to_scene(MainMenuScene(self.screen))
            pass


class NewGameScene(MenuScene):

    def __init__(self, screen):
        super().__init__(screen)
        self._menu_title = " Choose Game Mode"
        self._menu_items = ["Overworld", "Combat", "Main Menu"]

    def render(self):
        self.screen.fill(Colors.BLACK.value)
        self.draw_title()
        self.display_menu_items(self.starting_height)
        self.draw_cursor()

    def update(self):
        pass

    def select_menu_item(self, index):

        if index == 0:
            self.switch_to_scene(oscene.OverworldScene(self.screen))
            pass
        elif index == 1:
            # switch to combat scene
            pass
        elif index == 2:
            self.switch_to_scene(MainMenuScene(self.screen))
