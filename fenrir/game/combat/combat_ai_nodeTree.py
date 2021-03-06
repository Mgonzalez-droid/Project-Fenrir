import math
"""
.. module:: combat_ai_NodeTree
  :synopsis: module for building a node version of the map for the AI to path
"""


class Node:
    """Class that is a single Node. Contains it's x, y, value, parent, and list of neighbor Nodes

    :param xPos: (int) x tile coordinate position of the Node in the battle scene
    :param xPos: (int) y tile coordinate position of the Node in the battle scene

    Other non-params:
    :distanceFromStart: (int) the value of all the nodes before this one summed
    :totalDistance: (int) the total distance from the starting node to the goal node through this node
    :neighbors: (list of Node objects) a list of the neighboring Node objects (max 4)
    :parent: (Node) the Node that the current Node was reached from
    """
    def __init__(self, x, y):
        self._xPos = x
        self._yPos = y
        self._nodeWeight = 1
        self._givenCost = 0
        self._distanceToGoal = 0
        self._finalCost = 0

        self._distanceFromStart = 0
        self._totalDistance = 0
        self._neighbors = []
        self._myParent = None

    def get_xPos(self):
        return self._xPos

    def get_yPos(self):
        return self._yPos

    def get_nodeWeight(self):
        return self._nodeWeight

    def get_givenCost(self):
        return self._givenCost

    def calculate_givenCost(self, parentGivenCost):
        return self._nodeWeight + parentGivenCost

    def set_givenCost(self, newGivenCost):
        self._givenCost = newGivenCost

    def get_distanceToGoal(self):
        return self._distanceToGoal

    def set_distanceToGoal(self, goalX, goalY):
        self._distanceToGoal = abs(goalX - self._xPos) + abs(goalY - self._yPos)

    def get_finalCost(self):
        return self._finalCost

    def set_finalCost(self):
        self._finalCost = self._givenCost + (self._distanceToGoal * 1.2)

    def get_distanceFromStart(self):
        return self._distanceFromStart

    def set_distanceFromStart(self, newValue):
        self._distanceFromStart = newValue

    def get_totalDistance(self):
        return self._totalDistance

    def set_totalDistance(self, newValue):
        self._totalDistance = newValue

    def get_parent(self):
        return self._myParent

    def set_parent(self, newParent):
        self._myParent = newParent

    def get_neighbors(self):
        return self._neighbors

    def set_neighbors(self, newNeighborNode):
        self._neighbors.append(newNeighborNode)

    def clear_data(self):
        self._distanceFromStart = 0
        self._totalDistance = 0
        self._givenCost = 0
        self._givenCost = 0
        self._distanceToGoal = 0
        self._finalCost = 0
        self._myParent = None


class CombatAINodeTree:
    """Class that holds and builds the AI NodeTree. Takes in the width and height of the battle map (tiles)

    :param widthInTiles: (int) the maximum number of tile across the map
    :param heightInTiles: (int) the maximum number of tiles down the map
    :param mapData: (obj) holds all the map information in the round

    Other non-param values:
    :AINodeTree: (list of Node objects) the NodeTree object that has all the Nodes for the battle scene
    """
    def __init__(self, widthInTiles, heightInTiles, mapData):
        self.AINodeTree = []
        self._copyOfMapData = mapData
        # create all the nodes that are accessible
        for x in range(widthInTiles):
            for y in range(heightInTiles):
                if self.is_tile_accessible(x, y):
                    newNode = Node(x, y)
                    self.AINodeTree.append(newNode)

        # set the neighbors for each node
        for node in self.AINodeTree:
            counter = 0
            for otherNode in self.AINodeTree:
                x = otherNode.get_xPos()
                y = otherNode.get_yPos()
                # if the 1 coordinate matches and the other is +-1 then it must be a neighbor
                if x == node.get_xPos() and (y == (node.get_yPos() - 1) or y == (node.get_yPos() + 1)):
                    node.set_neighbors(otherNode)
                    counter += 1
                elif y == node.get_yPos() and (x == (node.get_xPos() - 1) or x == (node.get_xPos() + 1)):
                    node.set_neighbors(otherNode)
                    counter += 1
                # max of 4 neighbors possible
                if counter == 4:
                    break

    def is_tile_accessible(self, x, y):
        if not self._copyOfMapData.tilemap[y][x].is_blocking and not self._copyOfMapData.tilemap[y][x].is_wall:
            return True
        return False

    def get_ai_node_tree(self):
        return self.AINodeTree
