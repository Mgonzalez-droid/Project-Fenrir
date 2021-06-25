"""
.. module:: combat_ai_system
  :synopsis: module for controlling ai attack and move choices
"""

import math


class CombatAISystem:
    """Class representing ai combat information and decisions.

    :param participants: (list of obj) list of all characters in the combat scene
    :param currentParticipant: (character obj) the character obj for the current ai that is making decisions

    Other non-param values:
    :list_of_enemies: (list of obj) local copy of the list of characters in the combat scene
    :me: (character obj) local copy of the character obj for the current ai that is making decisions
    :myXPos: (int) local x coord of the ai position
    :myYPos: (int) local y coord of the ai position
    :target: (character obj) the current best target for this ai to attack
    :opponentScore: (int) the value rating of the current best target
    :targetNextToMe: (boolean) true if any non-enemy is directly next to the ai
    """
    def __init__(self, participants, currentParticipant, nodeTree):
        self._list_of_enemies = participants
        self._me = currentParticipant
        self._myX = (self._me.xpos - 30) / 60
        self._myY = (self._me.ypos - 30) / 60
        self._goalX = None
        self._goalY = None
        self._targetX = None
        self._targetY = None
        self._target = None
        self._targetNode = None
        self._opponentScore = 0
        self._targetDistance = 0
        self._targetNextToMe = False
        self._openList = []
        self._closedList = []
        self._nodeTree = nodeTree

    def decide_who_to_attack(self):
        """Function to decide on what character to attack. Based on distance, hp, type.
        """
        for i in self._list_of_enemies:
            if not i.get_is_enemy() and i.hp > 0:
                enemyValue = 0
                distanceX = abs(self._myX - ((i.xpos - 30) / 60))
                distanceY = abs(self._myY - ((i.ypos - 30) / 60))
                totalDist = distanceX + distanceY

                if totalDist == 1:                                              # enemy is next to a AI!
                    self._targetNextToMe = True
                    self._target = i                                            # set target and return
                    return
                elif totalDist <= self._me.attck_range:                         # enemy is not next to AI but is in attack range
                    enemyValue += 10                                                # best option
                elif totalDist <= self._me.attck_range + self._me.move_range:   # enemy is in range if AI moves closer
                    enemyValue += 5                                                 # good option
                else:                                                           # enemy is out of range. AI will have to move only
                    enemyValue -= 2                                                 # poor option

                if i.hp < self._me.attack or i.hp < self._me.magic_attack:      # easy kill
                    enemyValue += 10
                elif i.hp < self._me.hp:                                        # good chance to kill
                    enemyValue += 5
                else:
                    enemyValue += 2

                if self._target is None or enemyValue > self._opponentScore:    # current best target for the AI
                    self._target = i
                    self._targetX = (i.xpos - 30) / 60
                    self._targetY = (i.ypos - 30) / 60
                    self._targetDistance = totalDist

    def decide_where_to_move(self):
        """Function to decide where to move the ai on the map. Returns x Coord to move to, y Coord to move to, target id
        to attack this turn. based on A*
        """
        # make list to search and list already searched
        openList = []
        closedList = []
        self._nodeTree.clear_ai_node_tree_data()

        # find the first node and add it to the list to search. Set node's value to hold the distance to target
        for node in self._nodeTree:
            if node.get_xPos() == self._myX and node.get_yPos() == self._myY:
                openList.append(node)
                node.set_value(self._targetDistance)
                break

        # as long as there are nodes to search keep looping
        while len(openList) > 0:
            # currently this takes the first tile off the list to search and makes it current/adds it to the searched list. This needs to be updated to pick based on distance
            currentTile = openList[0]
            openList.pop(0)
            closedList.append(currentTile)

            # check if the current tile is the goal
            if currentTile.get_xPos() == self._targetX and currentTile.get_yPos() == self._targetY:
                self._targetNode = currentTile
                return  # found the end

            # loop and add all of the current node's neighbors to the list to search
            for neighbor in currentTile.get_neighbors():
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
                totalDist = distanceX + distanceY + currentTile.get_pastValue() + 1

                # check if the neighbor is in the open list. if so is this a better path?
                inOpenList = False
                for openNeighbor in openList:
                    if openNeighbor.get_xPos() == neighbor.get_xPos() and openNeighbor.get_yPos() == neighbor.get_yPos():
                        inOpenList = True
                        if openNeighbor.get_total() > totalDist:
                            neighbor.set_pastValue(currentTile.get_pastValue() + 1)
                            neighbor.set_totalValue(totalDist)
                            neighbor.set_parent(currentTile)
                        else:
                            break
                if not inOpenList:
                    neighbor.set_pastValue(currentTile.get_pastValue() + 1)
                    neighbor.set_totalValue(totalDist)
                    neighbor.set_parent(currentTile)
                    openList.append(neighbor)

    def find_ai_goal_from_tree(self, numberOfTilesToMove):
        currentTile = self._targetNode
        for i in range(self._targetDistance - numberOfTilesToMove):
            currentTile = currentTile.get_parent()
        self._goalX = currentTile.get_xPos()
        self._goalY = currentTile.get_yPos()

    def decide_ai_action(self):
        """Function decides if ai should only attack (next to enemy already), move twice (no enemy in range), or move then
        attack. Returns desired ai xcoord, ycoord, and target id"""
        self.decide_who_to_attack()
        if self.targetNextToMe or self._targetDistance <= self._me.attck_range:
            return self._me.xpos, self._me.ypos, self._target.get_id()
        elif self._targetDistance > (self._me.move_range + self._me.attck_range):
            self.decide_where_to_move()
            self.find_ai_goal_from_tree(self._me.move_range + math.floor(self._me.move_range * .5))
            return self._goalX, self._goalY, None
        else:
            self.decide_where_to_move()
            self.find_ai_goal_from_tree(self._me.move_range)
            return self._goalX, self._goalY, self._target.get_id()
