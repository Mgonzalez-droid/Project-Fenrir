"""
.. module:: combat_grid_system
  :synopsis: grid system will display grid on combat screen and will hightlight
             specific tiles for moves, attacks and more.
"""

import pygame
from fenrir.common.config import Colors
import time


class CombatGridSystem:

    def __init__(self, rows, cols, screen):
        self._rows = rows
        self._cols = cols
        self._grid = []
        self._screen = screen
        self._create_grid_rects()
        self._highlight_color = Colors.BLUE.value
        self._highlighted_tiles = []

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def grid(self):
        return self._grid

    def _create_grid_rects(self):
        for i in range(0, self._rows):
            temp_list = []
            for j in range(0, self._cols):
                grid = pygame.Rect(j * 60, i * 60, (j * 60 + 60), (i * 60 + 60))
                temp_list.append(grid)
            self._grid.append(temp_list)

    def draw_grid(self, mouse_x, mouse_y, player_x, player_y, highlighting_player):
        for i in range(0, self._rows):
            for j in range(0, self.cols):
                pygame.draw.rect(self._screen, Colors.GRID_GRAY.value, self._grid[i][j], 1)

        for tile in self._highlighted_tiles:
            self._highlight_tile_by_index(tile, self._highlight_color)

        if self._highlighted_tiles:
            self.mouse_hover_highlight(mouse_x, mouse_y)
        if highlighting_player:
            self._highlight_current_player(player_x, player_y)

    def _highlight_tile_by_index(self, tile, color):
        shape_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        shape_surf.set_alpha(90)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        self._screen.blit(shape_surf, tile)

    def highlight_tiles(self, tile_list, color):
        self._highlighted_tiles = []
        self._highlight_color = color
        for row, col in tile_list:
            self._highlighted_tiles.append(self._grid[row][col])

    def clear_highlights(self):
        self._highlighted_tiles = []

    def mouse_hover_highlight(self, x, y):
        row = int(y // 60)
        col = int(x // 60)
        tile = self._grid[row][col]

        if tile in self._highlighted_tiles:
            color = Colors.GREEN.value
        else:
            color = Colors.RED.value

        shape_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        shape_surf.set_alpha(190)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        self._screen.blit(shape_surf, tile)

    def _highlight_current_player(self, x, y):
        tile = self._grid[int(y // 60)][int(x // 60)]
        shape_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        shape_surf.set_alpha(180)
        pygame.draw.rect(shape_surf, Colors.WHITE.value, shape_surf.get_rect())
        self._screen.blit(shape_surf, tile)
