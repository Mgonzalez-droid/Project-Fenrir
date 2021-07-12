"""
.. function:: combat_move_list
  :synopsis: used for building a list of tiles to move for each character
"""


def combat_move_list(startingX, startingY, endingX, endingY, nodeTree):
    moveList = []
    endNode = None
    for node in nodeTree:
        node.clear_data()
        if node.get_xPos() == endingX and node.get_yPos() == endingY:
            endNode = node

    return moveList
