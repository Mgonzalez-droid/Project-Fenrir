"""
.. function:: combat_move_list
  :synopsis: used for building a list of tiles to move for each character
"""


def combat_move_list(startingX, startingY, endingX, endingY, nodeTree, mapData):
    moveList = []
    openList = []
    closedList = []
    totalDist = abs(startingX - endingX) + abs(startingY - endingY)
    currentTile = None
    # Find the node with the coal position first and append it to the list
    for node in nodeTree:
        node.clear_data()
        if node.get_xPos() == startingX and node.get_yPos() == startingY:
            node.set_totalDistance(totalDist)
            openList.append(node)

    while len(openList) > 0:
        bestTile = openList[0]
        bestTileIndex = 0
        counter = 0
        for tile in openList:
            if tile.get_totalDistance() < bestTile.get_totalDistance():
                bestTile = tile
                bestTileIndex = counter
            counter += 1
        currentTile = bestTile

        openList.pop(bestTileIndex)
        closedList.append(currentTile)

        # if currentTile coords match ending coords, then you are finished
        if currentTile.get_xPos() == endingX and currentTile.get_yPos() == endingY:
            break

        # loop and add all of the current node's neighbors to the list to search if not occupied
        for neighbor in currentTile.get_neighbors():
            if mapData.tilemap[neighbor.get_yPos()][neighbor.get_xPos()].is_occupied:
                continue
            alreadySearched = False
            # loop through list of nodes we have searched to make sure we haven't seen this node before
            for tileWeHaveSeen in closedList:
                # if the node we want to add matches one in the already search list, then break
                if neighbor.get_xPos() == tileWeHaveSeen.get_xPos() and neighbor.get_yPos() == tileWeHaveSeen.get_yPos():
                    alreadySearched = True
                    break
            # if this node isn't new move to the next node in the list of neighbors
            if alreadySearched:
                continue

            # if node is new to search, calculate the length traveled so far, the distance to the end and set the node values
            totalDist = abs(neighbor.get_xPos() - endingX) + abs(neighbor.get_yPos() - endingY) + currentTile.get_distanceFromStart() + 1

            # check if the neighbor is in the open list. if so is this a better path?
            inOpenList = False
            for openNeighbor in openList:
                if openNeighbor.get_xPos() == neighbor.get_xPos() and openNeighbor.get_yPos() == neighbor.get_yPos():
                    inOpenList = True
                    if openNeighbor.get_totalDistance() > totalDist:
                        neighbor.set_distanceFromStart(currentTile.get_distanceFromStart() + 1)
                        neighbor.set_totalDistance(totalDist)
                        neighbor.set_parent(currentTile)
                    else:
                        break
            if not inOpenList:
                neighbor.set_distanceFromStart(currentTile.get_distanceFromStart() + 1)
                neighbor.set_totalDistance(totalDist)
                neighbor.set_parent(currentTile)
                openList.append(neighbor)

    # build the list of tiles to traverse in reverse order
    for _ in range(0, currentTile.get_totalDistance()):
        moveList.append(currentTile)
        currentTile = currentTile.get_parent()

    return moveList
