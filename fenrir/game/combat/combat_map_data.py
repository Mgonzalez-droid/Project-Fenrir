"""
.. module:: combat_map_data
  :synopsis: module for creating tilesets and maps for combat scenes.
"""

import pygame
import configparser


MAP_TILE_W = 16
MAP_TILE_H = 16

class TileCache:
    """Class to allow slicing of tilesets into tiles in list of lists

        :param filename: (file) given tileset file to slice
        :param w: (int) individual tile width
        :param h: (int) individual tile height

        Other non-param values:
        :image: () loaded image from input file
        :image_w: (int) width of the image
        :image_h: (int) height of the image
        :tile_map: (list of line) a list containing a list of lines which contains each rect/tile
        :line: (list) a list containing each rect/tile in a row
        :rect: () a tile and its coordinates
        """

    """Load tilesets into our global cache"""

    def __init__(self, width=16, height=16):
        self.width = width
        self.height = height
        self.cache = {}

    def __get_item__(self, filename):
        """Returns table of tiles"""
        key = (filename, self.width, self.height)
        try:
            return self.cache[key]
        except KeyError:
            tile_map = self._load_tile_map(filename, self.width, self.height)
            self.cache[key] = tile_map
            return tile_map

    def _load_tile_map(self, filename, width, height):
        image = pygame.image.load(filename).convert()
        image_w, image_h = image.get_size()
        tile_map = []
        for c_tile in range(0, image_w / width):
            line = []
            tile_map.append(line)
            for r_tile in range(0, image_h / height):
                rect = (c_tile * width, r_tile * height, width, height)
                # subsurface returns tiles w/o creating copies in memory
                line.append(image.subsurface(rect))
        return tile_map

MAP_CACHE = TileCache(MAP_TILE_W, MAP_TILE_H)

class Level(object):
    def load_file(self, filename="level_001.map"):
        self.map = []
        self.key = {}
        parser = configparser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        for sec in parser.sections():
            if len(sec) == 1:
                desc = dict(parser.items(sec))
                self.key[sec] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)

    def get_tile(self, x, y):
        try:
            char = self.map[x][y]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_bool(self, x, y, name):
        val = self.get_tile(x, y).get(name)
        return val in (True, 1, "true", "True", "yes", "Yes", "on", "On", "1")

    def is_wall(self, x, y):
        return self.get_bool(x, y, "wall")

    def is_blocking(self, x, y):
        return self.get_bool(x, y, "block")

    def render(self):
        wall = self.is_wall
        tiles = MAP_CACHE[self.tileset]
        image = pygame.Surface((self.width * MAP_TILE_W, self.height * MAP_TILE_H))
        overlays = {}
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                if wall(map_x, map_y):
                    # Draw different tiles depending on neighbourhood
                    if not wall(map_x, map_y + 1):
                        if wall(map_x + 1, map_y) and wall(map_x - 1, map_y):
                            tile = 0, 5
                        elif wall(map_x + 1, map_y):
                            tile = 0, 0
                        elif wall(map_x - 1, map_y):
                            tile = 0, 1
                        else:
                            tile = 0, 2
                    else:
                        if wall(map_x + 1, map_y + 1) and wall(map_x - 1, map_y + 1):
                            tile = 0, 3
                        elif wall(map_x + 1, map_y + 1):
                            tile = 0, 11
                        elif wall(map_x - 1, map_y + 1):
                            tile = 0, 12
                        else:
                            tile = 0, 10
                    # Add overlays if the wall may be obscuring something
                    if not wall(map_x, map_y - 1):
                        if wall(map_x + 1, map_y) and wall(map_x - 1, map_y):
                            over = 1, 0
                        elif wall(map_x + 1, map_y):
                            over = 0, 0
                        elif wall(map_x - 1, map_y):
                            over = 2, 0
                        else:
                            over = 3, 0
                        overlays[(map_x, map_y)] = tiles[over[0]][over[1]]
                else:
                    try:
                        tile = self.key[c]['tile'].split(',')
                        tile = int(tile[0]), int(tile[1])
                    except (ValueError, KeyError):
                        # Default to ground tile
                        tile = 2, 2
                tile_image = tiles[tile[0]][tile[1]]
                image.blit(tile_image,
                           (map_x * MAP_TILE_W, map_y * MAP_TILE_H))
        return image, overlays


if __name__ == "__main__":
    pygame.init()

    game_over = False

    screen = pygame.display.set_mode((960, 540))
    level = Level()
    level.load_file("level_001.map")
    clock = pygame.time.Clock()

    background, overlay_dict = level.render()
    overlays = pygame.sprite.RenderUpdates()
    for (x, y), image in overlay_dict.iteritems():
        overlay = pygame.sprite.Sprite(overlays)
        overlay.image = image
        overlay.rect = image.get_rect().move(x * 16, y * 16 - 16)
    screen.blit(background, (0, 0))

    while not game_over:
        overlays.draw(screen)
        pygame.display.flip()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            elif event.type == pygame.locals.KEYDOWN:
                pressed_key = event.key

