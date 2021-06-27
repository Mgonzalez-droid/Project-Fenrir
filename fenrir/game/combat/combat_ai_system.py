"""
.. module:: combat_ai_system
  :synopsis: module for controlling ai attack and move choices
"""

import math


class CombatAISystem:
    """Class representing ai combat information and decisions.

    :param participants: (list of character objects) list of all characters in the combat scene.
    :param currentParticipant: (character object) the character object for the current ai that is making decisions.
    :param nodeTree: (list of Node objects) the list of all nodes for the battle scene.
    :param mapData: (obj) holds all the map information in the round

    Other non-param values:
    :list_of_enemies: (list of character objects) local copy of the list of characters in the combat scene.
    :me: (character object) local copy of the character object for the current ai that is making decisions.
    :myX: (int) local x coord of the ai position.
    :myY: (int) local y coord of the ai position.
    :goalX: (int) local x coord of the ai position goal.
    :goalY: (int) local y coord of the ai position goal.
    :targetX: (int) local x coord of the ai target.
    :targetY: (int) local y coord of the ai target.
    :target: (character obj) the current best target for this ai to attack.
    :targetNode: (Node object) the node the ai is moving towards.
    :opponentScore: (int) the value rating of the current best target.
    :targetDistance: (int) the distance from the ai to the targetNode.
    :targetNextToMe: (boolean) true if any non-enemy is directly next to the ai.
    :targetLessThanTheTargetPosition: (boolean) if the ai is moving to a node that is not next to the target character.
    :openList: (list of Node objects) list of Nodes to check for pathing
    :closedList: (list of Node objects) list of Nodes already checked for pathing
    """

    def __init__(self, participants, currentParticipant, nodeTree, mapData):
        self._list_of_enemies = participants
        self._me = currentParticipant
        self._nodeTree = nodeTree
        self._copyOfMapData = mapData
        self._myX = int((self._me.xpos - 30) / 60)
        self._myY = int((self._me.ypos - 30) / 60)
        self._goalX = None
        self._goalY = None
        self._targetX = None
        self._targetY = None
        self._target = None
        self._targetNode = None
        self._opponentScore = 0
        self._targetDistance = 0
        self._targetNextToMe = False
        self._targetNodeLessThanTargetPosition = False
        self._openList = []
        self._closedList = []

    def decide_who_to_attack(self):
        """A* based function to decide on what character to attack. Based on distance.
        """
        for i in self._list_of_enemies:
            if not i.get_is_enemy() and i.hp > 0:
                distanceX = abs(self._myX - ((i.xpos - 30) / 60))
                distanceY = abs(self._myY - ((i.ypos - 30) / 60))
                totalDist = distanceX + distanceY
                enemyValue = totalDist

                if totalDist == 1:  # an enemy is next to a AI!
                    self._targetNextToMe = True
                    self._target = i  # set target and return
                    return
                elif totalDist <= self._me.attack_range:  # enemy is not next to AI but is in attack range
                    enemyValue += 0  # best option
                elif totalDist <= self._me.attack_range + self._me.move_range:  # enemy is in range if AI moves closer
                    enemyValue -= (self._me.move_range - 1)  # good option
                else:  # enemy is out of range. AI will have to move only
                    enemyValue += 2  # poor option

                if self._target is None or enemyValue < self._opponentScore:  # current best target for the AI
                    self._target = i
                    self._targetX = int((i.xpos - 30) / 60)
                    self._targetY = int((i.ypos - 30) / 60)
                    self._targetDistance = totalDist
                    self._opponentScore = enemyValue

    def build_path_to_target(self):
        """Function to decide where to move the ai on the map. Returns x Coord to move to, y Coord to move to, target id
        to attack this turn. based on A*
        """
        # make list to search and list already searched
        openList = []
        closedList = []
        for node in self._nodeTree:
            node.clear_data()

        # find the first node and add it to the list to search. Set node's value to hold the distance to target
        for node in self._nodeTree:
            if node.get_xPos() == self._myX and node.get_yPos() == self._myY:
                openList.append(node)
                node.set_totalDistance(self._targetDistance)
                break

        # as long as there are nodes to search keep looping

        while len(openList) > 0:
            # pick the tile closest to the target from the openList
            bestTile = openList[0]
            bestTileIndex = 0
            counter = 0
            for tile in openList:
                if bestTile.get_totalDistance() > tile.get_totalDistance():
                    bestTile = tile
                    bestTileIndex = counter
                counter += 1
            currentTile = bestTile

            openList.pop(bestTileIndex)
            closedList.append(currentTile)

            # check if the current tile is the goal
            if currentTile.get_xPos() == self._targetX and currentTile.get_yPos() == self._targetY:
                self._targetNode = currentTile
                return  # found the end
            # check if the current tile is close enough to attack from
            if currentTile.get_totalDistance() - currentTile.get_distanceFromStart() <= self._me.attack_range:
                self._targetNode = currentTile
                self._targetNodeLessThanTargetPosition = True
                self._targetDistance = currentTile.get_distanceFromStart()
                return

            # loop and add all of the current node's neighbors to the list to search if not occupied
            for neighbor in currentTile.get_neighbors():
                if self._copyOfMapData.tilemap[neighbor.get_yPos()][neighbor.get_xPos()].is_occupied:
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
                distanceX = abs(neighbor.get_xPos() - self._targetX)
                distanceY = abs(neighbor.get_yPos() - self._targetY)
                totalDist = distanceX + distanceY + currentTile.get_distanceFromStart() + 1

                # check if the neighbor is in the open list. if so is this a better path?
                inOpenList = False
                for openNeighbor in openList:
                    if openNeighbor.get_xPos() == neighbor.get_xPos() and openNeighbor.get_yPos() == neighbor.get_yPos():
                        inOpenList = True
                        if openNeighbor.get_totalDistance() > totalDist:
                            neighbor.set_distanceFromStart(currentTile.get_pastValue() + 1)
                            neighbor.set_totalDistance(totalDist)
                            neighbor.set_parent(currentTile)
                        else:
                            break
                if not inOpenList:
                    neighbor.set_distanceFromStart(currentTile.get_distanceFromStart() + 1)
                    neighbor.set_totalDistance(totalDist)
                    neighbor.set_parent(currentTile)
                    openList.append(neighbor)

    def set_ai_goal_position(self, numberOfTilesToMove):
        currentTile = self._targetNode
        if self._targetNode.get_xPos() == self._targetX and self._targetNode.get_yPos() == self._targetY:
            numberOfTilesToMove -= 1
            for i in range(self._targetDistance - numberOfTilesToMove):
                currentTile = currentTile.get_parent()
            self._goalX = (currentTile.get_xPos() * 60) + 30
            self._goalY = (currentTile.get_yPos() * 60) + 30
        elif self._targetNodeLessThanTargetPosition:
            if self._targetDistance < numberOfTilesToMove:
                self._goalX = (self._targetNode.get_xPos() * 60) + 30
                self._goalY = (self._targetNode.get_yPos() * 60) + 30
            else:
                for i in range(self._targetDistance - numberOfTilesToMove):
                    currentTile = currentTile.get_parent()
                self._goalX = (currentTile.get_xPos() * 60) + 30
                self._goalY = (currentTile.get_yPos() * 60) + 30

    def decide_ai_action(self):
        """Function decides if ai should only attack (next to enemy already), move twice (no enemy in range), or move then
        attack. Returns desired ai xcoord, ycoord, and target id"""
        self.decide_who_to_attack()
        if self._target is None:
            return None, None, None
        if self._targetNextToMe or self._targetDistance <= self._me.attack_range:
            return self._me.xpos, self._me.ypos, self._target.get_id()
        elif self._targetDistance > (self._me.move_range + self._me.attack_range):
            self.build_path_to_target()
            self.set_ai_goal_position(self._me.move_range + math.floor(self._me.move_range * .5))
            return self._goalX, self._goalY, None
        else:
            self.build_path_to_target()
            self.set_ai_goal_position(self._me.move_range)
            return self._goalX, self._goalY, self._target.get_id()
