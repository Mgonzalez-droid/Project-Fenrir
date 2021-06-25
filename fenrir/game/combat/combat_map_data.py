"""
.. module:: combat_map_data
  :synopsis: module for creating tilesets and reading maps for combat scenes.
"""

import os
from fenrir.common.config import PATH_TO_RESOURCES

"""
:MAP_TILE_W: (int) holds standard width of tiles
:MAP_TILE_H: (int) holds standard height of tiles
"""
MAP_TILE_W = 60
MAP_TILE_H = 60

class MapTile:
    """
    Class represents tiles that will be used to populate combat map lists

    :param t_type: (string) tells us what kind of tile it is, used to determine other attributes
    :param x_coord, y_coord: (int) tells us the top left corner of the tile in x and y coordinates

    :wall: (boolean) tells us if the tile is a wall, if true also sets blocking to true
    :blocking: (boolean) tells us if the tile blocks movement
    :occupied: (boolean) tells us if there is a unit on the tile
    :unit: (string) tells us the name/ID of the unit occupying the tile
    """

    def __init__(self, t_type, x_coord, y_coord):
        # Standard Types: ground, wall, blocking
        self._t_type = t_type
        # Coordinates are in increments of 60, top left corner of each tile
        self._x_coord = x_coord
        self._y_coord = y_coord
        self._id = str(x_coord) + str(y_coord)
        self._occupied = False
        self._unit = ""
        self._adjacent = []
        # Wall and blocking attributes to determine movement
        if self._t_type == "wall":
            self._wall = True
            self._blocking = True
        elif self._t_type == "blocking":
            self._wall = False
            self._blocking = True
        else:
            self._wall = False
            self._blocking = False

    @property
    def t_type(self):
        return self._t_type

    @property
    def id(self):
        return self._id

    @property
    def is_wall(self):
        return self._wall

    @property
    def is_blocking(self):
        return self._blocking

    @property
    def is_occupied(self):
        return self._occupied

    @property
    def adjacencies(self):
        return self._adjacent

    def set_adjacency(self, adjacency):
        self._adjacent.append(adjacency)

    def occupy(self, unit):
        self._occupied = True
        self._unit = unit

    def unoccupy(self):
        self._occupied = False
        self._unit = ""

    @property
    def x_coord(self):
        return self._x_coord

    @x_coord.setter
    def x_coord(self, value):
        self._x_coord = value

    @property
    def y_coord(self):
        return self._y_coord

    @y_coord.setter
    def y_coord(self, value):
        self._y_coord = value


class MapData:
    """
        Class represents the map that will be used in combat

        :param name: (string) file name associated with the map
                              used to load .png map images and .txt map data
        :param columns: (int) how many tiles in the vertical (height divided by 60)
        :param rows: (int) how many tiles in the horizontal (width divided by 60)
        :char_map: (string)  2D list of characters representing tiles, used to populate
                        and define tilemap
                        (we can use files associated with map images to populate this)

        :height: (int) height of the map .png (should be a multiple of 60)
        :width: (int) width of the map .png (should be a multiple of 60)
        :tilemap: (MapTile) 2D list of all the tiles on the map

        Note: Each map should not be edited after it is created. Tilemap data should be taken from the object
              and moved into a variable in the method that is running it so that the original map data isn't
              altered
    """

    def __init__(self, name, columns, rows):
        # Name will be used to append .png or .txt to pull data from
        self._name = name
        # Number of tiles horizontally and vertically respectively
        self._columns = columns
        self._rows = rows
        # Map should be a 2D List of strings (single chars)
        # Char map txt file MUST BE 23w x 13h!
        self._char_map = self.load_charmap()
        # Dimensions based off of tile numbers
        self._height = self._rows * MAP_TILE_H
        self._width = self._columns * MAP_TILE_W
        # Tilemap population and definition
        # Tilemap PNG MUST be 960 x 540!
        self._tilemap = []
        for i in range(self._rows):
            # Create a temp list to append to our first list so we can make it 2D
            _temp_list = []
            # Redundant, can be removed if necessary, but makes sure temp list is EMPTY before appending
            _temp_list.clear()
            for j in range(self._columns):
                if self._char_map[i][j] == ".":
                    _temp_list.append(MapTile("ground", i * MAP_TILE_W, j * MAP_TILE_H))
                elif self._char_map[i][j] == "#":
                    _temp_list.append(MapTile("wall", i * MAP_TILE_W, j * MAP_TILE_H))
                elif self._char_map[i][j] == "~":
                    _temp_list.append(MapTile("blocking", i * MAP_TILE_W, j * MAP_TILE_H))
                elif self._char_map[i][j] == "a":
                    _temp_list.append(MapTile("player_spawn", i * MAP_TILE_W, j * MAP_TILE_H))
                elif self._char_map[i][j] == "e":
                    _temp_list.append(MapTile("enemy_spawn", i * MAP_TILE_W, j * MAP_TILE_H))
            # Append our columns to each row
            self._tilemap.append(_temp_list)
        self.set_tile_adj()
        # Create spawn lists
        self._playerspawn = []
        self._enemyspawn = []
        for i in range(self._rows):
            for j in range(self._columns):
                if self._tilemap[i][j].t_type == "player_spawn":
                    self._playerspawn.append(self._tilemap[i][j])
                elif self._tilemap[i][j].t_type == "enemy_spawn":
                    self._enemyspawn.append(self._tilemap[i][j])

    @property
    def name(self):
        return self._name

    @property
    def columns(self):
        return self._columns

    @property
    def rows(self):
        return self._rows

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def tilemap(self):
        return self._tilemap

    def load_charmap(self):
        filename = os.path.join(PATH_TO_RESOURCES, "combat_maps", self._name)
        __in_file = open(filename + ".txt", "r")
        __char_map = []
        __in_lines = __in_file.readlines()
        for line in __in_lines:
            line_split = []
            line_split = line.split()
            __char_map.append(line_split)
        return __char_map

    def set_tile_adj(self):
        for i in range(self._rows):
            for j in range(self._columns):
                if i == 0:
                    if j == 0:
                        self._tilemap[i][j].set_adjacency(self._tilemap[i][j + 1])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i + 1][j])
                    elif j == len(self._tilemap[i]) - 1:
                        self._tilemap[i][j].set_adjacency(self._tilemap[i][j - 1])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i + 1][j])
                    else:
                        self._tilemap[i][j].set_adjacency(self._tilemap[i][j + 1])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i][j - 1])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i + 1][j])
                elif i == len(self._tilemap) - 1:
                    if j == 0:
                        self._tilemap[i][j].set_adjacency(self._tilemap[i][j + 1])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i - 1][j])
                    elif j == len(self._tilemap[i]) - 1:
                        self._tilemap[i][j].set_adjacency(self._tilemap[i][j - 1])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i - 1][j])
                    else:
                        self._tilemap[i][j].set_adjacency(self._tilemap[i][j + 1])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i][j - 1])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i - 1][j])
                else:
                    if j == 0:
                        self._tilemap[i][j].set_adjacency(self._tilemap[i][j + 1])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i - 1][j])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i + 1][j])
                    elif j == len(self._tilemap[i]) - 1:
                        self._tilemap[i][j].set_adjacency(self._tilemap[i][j - 1])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i - 1][j])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i + 1][j])
                    else:
                        self._tilemap[i][j].set_adjacency(self._tilemap[i][j + 1])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i][j - 1])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i - 1][j])
                        self._tilemap[i][j].set_adjacency(self._tilemap[i + 1][j])

    @property
    def enemyspawn(self):
        return self._enemyspawn

    @property
    def playerspawn(self):
        return self._playerspawn
