import pygame
from fenrir.common.scene import Scene
import fenrir.game.overworld.overworld_scene_hub as overscene
from fenrir.common.config import *
from fenrir.data.load_game_from_db import *
import time


##########################################################
#   ABSTRACT MENU SCENE - USED CREATE MENUS W/CURSORS    #
##########################################################
class MenuScene(Scene):

    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        # default variables that will be implemented in subclasses
        self._menu_title = ""  # title attr
        self._menu_items = []  # menu items that work with cursor
        self.menu_item_rects = []  # used for cursor placement and possible collision detection for mouse events TODO
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


##########################################################
#       MAIN MENU SCENE - LOADED WHEN GAME STARTS        #
##########################################################
class MainMenuScene(MenuScene):

    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
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
            self.switch_to_scene(NewGameScene(self.screen, self.game_state))
        elif index == 1:
            self.switch_to_scene(LoadGameScene(self.screen, self.game_state))
        elif index == 2:
            self.switch_to_scene(CreditsScene(self.screen, self.game_state))
        elif index == 3:
            self.terminate()


##########################################################
#       LOAD GAME SCENE - USED TO LOAD SAVED GAME        #
##########################################################
class LoadGameScene(MenuScene):

    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self._menu_title = "Saved Games"
        self._saved_games = sorted(load_game_save_titles(), key=lambda x: x[2], reverse=True)
        self._menu_items = []
        self._curr_page_num = 1
        self._pages = int(len(self._saved_games) / 4 if len(self._saved_games) % 4 == 0
                          else len(self._saved_games) // 4 + 1)
        self._prev_page = False
        self._next_page = False
        self.populate_menu_items()

    def populate_menu_items(self):

        if self._saved_games:
            self.starting_height = DisplaySettings.CENTER_HEIGHT.value - 100

            if self._curr_page_num == self._pages:
                if len(self._saved_games) % 4 == 0:
                    stopIndex = 4
                else:
                    stopIndex = len(self._saved_games) % 4
            else:
                stopIndex = 4

            for i in range(1, stopIndex + 1):
                save = self._saved_games[i * self._curr_page_num - 1]
                self._menu_items.append("Player Name: " + save[1] + "    Last Saved: " + save[2])
        else:
            self.starting_height = DisplaySettings.SCREEN_RESOLUTION.value[1] - 50

        if self._curr_page_num > 1:
            self._menu_items.append("Prev Page")
            self._prev_page = True

        if self._curr_page_num < self._pages:
            self._menu_items.append("Next Page")
            self._next_page = True

        self._menu_items.append("Main Menu")

    def update(self):
        pass

    def render(self):
        self.screen.fill(Colors.BLACK.value)
        self.draw_title()
        self.display_menu_items(self.starting_height)
        self.draw_cursor()

    def select_menu_item(self, index):

        if index == len(self._menu_items) - 1:
            self.switch_to_scene(MainMenuScene(self.screen, self.game_state))
        elif index == len(self._menu_items) - 2:
            if self._next_page:
                self.show_next_page()
            elif self._prev_page:
                self.show_prev_page()
            else:
                gameIndex = 4 * (self._curr_page_num - 1) + index
                self.game_state = load_game_save_by_id(self._saved_games[gameIndex][0])
                self.switch_to_scene(overscene.OverworldScene(self.screen, self.game_state))
        elif index == len(self._menu_items) - 3 and self._next_page:
            if self._prev_page:
                self.show_prev_page()
            else:
                gameIndex = 4 * (self._curr_page_num - 1) + index
                self.game_state = load_game_save_by_id(self._saved_games[gameIndex][0])
                self.switch_to_scene(overscene.OverworldScene(self.screen, self.game_state))
        else:
            gameIndex = 4 * (self._curr_page_num - 1) + index
            self.game_state = load_game_save_by_id(self._saved_games[gameIndex][0])
            self.switch_to_scene(overscene.OverworldScene(self.screen, self.game_state))

    def display_menu_items(self, start_height):
        i = 0
        for item in self._menu_items:
            self.draw_text_to_screen(item, 32, DisplaySettings.CENTER_WIDTH.value,
                                     start_height + (i * 40), i)
            i += 1

        if self._pages:
            self.draw_text_to_screen(f"Page {self._curr_page_num} / {self._pages}", 30, DisplaySettings.CENTER_WIDTH.value,
                                     DisplaySettings.SCREEN_RESOLUTION.value[1] - 40)
        else:
            self.draw_text_to_screen("No saved games yet!", 40, DisplaySettings.CENTER_WIDTH.value,
                                     DisplaySettings.CENTER_HEIGHT.value)

    def show_prev_page(self):
        self.cursor_pos = 0
        self._curr_page_num -= 1
        self.menu_item_rects = []
        self._menu_items = []
        self._next_page = False
        self._prev_page = False
        self.populate_menu_items()

    def show_next_page(self):
        self.cursor_pos = 0
        self._curr_page_num += 1
        self.menu_item_rects = []
        self._menu_items = []
        self._next_page = False
        self._prev_page = False
        self.populate_menu_items()


##########################################################
#          CREDITS SCENE - USED TO VIEW CREDITS          #
##########################################################
class CreditsScene(MenuScene):

    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self._menu_title = "Credits"
        self._credit_names = ["Victor Sotomayor - Team Lead, Combat Team", "Barry Congressi - Combat Team",
                              "Bryan Kristofferson - Combat Team", "Michel Gonzalez - Overworld Team",
                              "Roberto Rafael Edde Verde - Overworld Team"]
        self._menu_items = ["Main Menu"]
        self._menu_start_height = DisplaySettings.SCREEN_RESOLUTION.value[1] - 100  # bottom of screen

    def render(self):
        self.screen.fill(Colors.BLACK.value)
        self.draw_title()
        self.draw_names()
        self.display_menu_items(self._menu_start_height + 50)
        self.draw_cursor()

    def draw_names(self):
        starting_height = self.starting_height - 40

        i = 0
        for name in self._credit_names:
            self.draw_text_to_screen(name, 35, DisplaySettings.CENTER_WIDTH.value,
                                     starting_height + (i * self.menu_item_spacer))
            i += 1

    def update(self):
        pass

    def select_menu_item(self, index):
        if index == 0:
            self.switch_to_scene(MainMenuScene(self.screen, self.game_state))
            pass


##########################################################
#        NEW GAME SCENE - USED TO START NEW GAME         #
##########################################################
class NewGameScene(MenuScene):

    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self._menu_title = "New Game"
        self._menu_items = ["Start New Game", "Back"]
        self._inputting_name = False
        self._input_text = ""
        self._input_rect = pygame.Rect(0, 0, 400, 40)
        self._input_curs_rect = pygame.Rect(0, 0, 10, 30)
        self.game_state = GameState()

    def render(self):
        self.screen.fill(Colors.BLACK.value)
        self.draw_title()
        self.display_menu_items(self.starting_height)
        self.draw_cursor()

        if self._inputting_name:
            self.draw_input_box()

    def update(self):
        pass

    def select_menu_item(self, index):
        if self._inputting_name:
            if index == 0:
                self.game_state.player_name = self._input_text
                self.switch_to_scene(overscene.OverworldScene(self.screen, self.game_state))
            elif index == 1:
                self.switch_to_scene(NewGameScene(self.screen, self.game_state))
        else:
            if index == 0:
                self._inputting_name = True
                self._menu_items = ["Start Game", "Cancel"]
                self.starting_height += 120
                self.menu_item_rects = []
            elif index == 1:
                self.switch_to_scene(MainMenuScene(self.screen, self.game_state))

    def draw_input_box(self):
        self._input_rect.center = (DisplaySettings.CENTER_WIDTH.value, DisplaySettings.CENTER_HEIGHT.value)
        self.draw_text_to_screen("Enter Player Name", 50, DisplaySettings.CENTER_WIDTH.value,
                                 DisplaySettings.CENTER_HEIGHT.value - self.menu_item_spacer)
        font = pygame.font.SysFont(None, 40)
        txt_img = font.render(self._input_text, True, Colors.WHITE.value)
        rect = txt_img.get_rect()
        rect.size = txt_img.get_size()
        rect.center = self._input_rect.center
        self._input_curs_rect.midleft = rect.midright
        self.screen.blit(txt_img, rect)

        pygame.draw.rect(self.screen, Colors.WHITE.value, self._input_rect, 1)

        if time.time() % 1 > 0.5:
            pygame.draw.rect(self.screen, Colors.WHITE.value, self._input_curs_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.move_cursor("DOWN")
            elif event.key == pygame.K_UP:
                self.move_cursor("UP")
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.select_menu_item(self.cursor_pos)
            elif self._inputting_name:
                if event.key == pygame.K_BACKSPACE:
                    if len(self._input_text) > 0:
                        self._input_text = self._input_text[:-1]
                else:
                    self._input_text += event.unicode
