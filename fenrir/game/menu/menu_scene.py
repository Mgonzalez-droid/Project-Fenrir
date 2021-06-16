import pygame

from fenrir.common.scene import Scene
from fenrir.common.config import *


class MainMenuScene(Scene):

    def __init__(self):
        Scene.__init__(self)
        self._mouse_location = (None, None)
        self._mouse_clicked = False
        self._mouse_click_location = (None, None)
        self._menu_items = ["New Game", "Load Game", "Credits", "Exit"]
        self._MENU_ITEM_SPACER = 60
        self._cursor_rect = pygame.Rect(CENTER_X - 120, CENTER_Y - 55, 50, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self._mouse_location = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_clicked = True
            self._mouse_click_location = pygame.mouse.get_pos()
            print("Mouse clicked at", self._mouse_click_location)

    def update(self):
        pass

    def render(self, screen):
        screen.fill(Colors.BLACK.value)
        self.draw_text(screen, "PROJECT FENRIR", 100, CENTER_X,
                       CENTER_Y - (self._MENU_ITEM_SPACER * 3))
        self.display_menu_items(screen)
        self.draw_cursor(screen)

    def draw_cursor(self, screen):
        self.draw_text(screen, "*", 50, self._cursor_rect.x, self._cursor_rect.y)

    def display_menu_items(self, screen):
        starting_height = CENTER_Y - self._MENU_ITEM_SPACER

        for item in self._menu_items:
            self.draw_text(screen, item, 50, CENTER_X, starting_height)
            starting_height += self._MENU_ITEM_SPACER

    def draw_text(self, screen, text, size, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, Colors.WHITE.value)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        screen.blit(text_surface, text_rect)
