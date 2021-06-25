"""
.. module:: combat_ai_NodeTree
  :synopsis: module for building a node version of the map for the AI to path
"""


class Node:
    """Class that is a single Node. Contains it's x, y, value, parent, and list of neighbor Nodes

    :param xPos: (int) x coordinate position of the Node in the battle scene
    :param xPos: (int) y coordinate position of the Node in the battle scene
    :param width: (int) the maximum number of tile across the map
    :param height: (int) the maximum number of tiles down the map

    Other non-params:
    :value: (float) the heuristic of this Node in the map.
    :neighbors: (list of tuples of int) a list of the neighboring Nodes by coordinates
    :parent: (Node) the Node that the current Node was reached from
    """
    def __init__(self, x, y):
        self._xPos = x
        self._yPos = y
        self._value = None
        self._neighbors = []
        self._myParent = None

    def get_xPos(self):
        return self._xPos

    def get_yPos(self):
        return self._yPos

    def get_value(self):
        return self._value

    def set_value(self, newValue):
        self._value = newValue

    def get_parent(self):
        return self._myParent

    def set_parent(self, newParent):
        self._myParent = newParent

    def get_neighbors(self):
        return self._neighbors

    def set_neighbors(self, newNeighborNode):
        self._neighbors.append(newNeighborNode)

    def clear_data(self):
        self._value = None
        self._myParent = None


class CombatAINodeTree:
    """Class that holds and builds the AI NodeTree. Takes in the width and height of the battle map

    :param width: (int) the maximum number of tile across the map
    :param height: (int) the maximum number of tiles down the map

    Other non-param values:
    :AINodeTree: (list of Node objects) the NodeTree object that has all the Nodes for the battle scene
    """
    def __init__(self, width, height):
        self.AINodeTree = {}
        # create all the nodes
        for x in range(width):
            for y in range(height):
                if FAKE_FUNCTION_IS_TILE_ACCESSABLE():
                    newNode = Node(x, y)
                    AINodeTree.append(newNode)

        # set all the neighbors for each node
        for node in self.AINodeTree:
            if (node.get_yPos() - 1) >= 0 and FAKE_FUNCTION_IS_TILE_ACCESSABLE():
                for otherNode in self.AINodeTree:
                    if otherNode.get_xPos() == node.get_xPos() and otherNode.get_yPos() == (node.get_yPos() - 1):
                        node.set_neighbor(otherNode)
                        break
            if (node.get_xPos() + 1) < width and FAKE_FUNCTION_IS_TILE_ACCESSABLE():
                for otherNode in self.AINodeTree:
                    if otherNode.get_xPos() == (node.get_xPos() + 1) and otherNode.get_yPos() == node.get_yPos():
                        node.set_neighbor(otherNode)
                        break
            if (node.get_yPos() + 1) < height and FAKE_FUNCTION_IS_TILE_ACCESSABLE():
                for otherNode in self.AINodeTree:
                    if otherNode.get_xPos() == node.get_xPos() and otherNode.get_yPos() == (node.get_yPos() + 1):
                        node.set_neighbor(otherNode)
                        break
            if (node.get_xPos() - 1) >= 0 and FAKE_FUNCTION_IS_TILE_ACCESSABLE():
                for otherNode in self.AINodeTree:
                    if otherNode.get_xPos() == (node.get_xPos() - 1) and otherNode.get_yPos() == node.get_yPos():
                        node.set_neighbor(otherNode)
                        break

    def get_ai_node_tree(self):
        return self.AINodeTree

    def clear_ai_node_tree_data(self):
        for i in self.AINodeTree:
            i.clear_data()
