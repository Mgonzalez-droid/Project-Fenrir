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
        self.list_of_characters = participants
        self.me = currentParticipant
        self._nodeTree = nodeTree
        self._copyOfMapData = mapData
        self.myX = int((self.me.xpos - 30) / 60)
        self.myY = int((self.me.ypos - 30) / 60)
        self.enemy = None
        self.enemyValue = 0
        self.enemyX = 0
        self.enemyY = 0
        self.estimatedEnemyDistance = 0
        self.enemyPathDistance = 0
        self.enemyNextToMe = False
        self.startNode = None
        self.endNode = None
        self.closestNode = None
        self.listToSearch = None
        self._goalX = None
        self._goalY = None
        self.distanceToFar = False

    def decide_who_to_attack(self):
        """Uses distance from each target and type checking to decide which target should be the focus this turn.
        """
        for potentialTarget in self.list_of_characters:
            if not potentialTarget.get_is_enemy() and potentialTarget.hp > 0:
                # Estimate the distance to this target
                potentialTargetX = ((potentialTarget.xpos - 30) / 60)
                potentialTargetY = ((potentialTarget.ypos - 30) / 60)
                estimatedTotalDist = abs(self.myX - potentialTargetX) + abs(self.myY - potentialTargetY)

                # Check if enemy is next to me
                if estimatedTotalDist == 1:
                    self.enemyNextToMe = True
                    self.enemy = potentialTarget
                    return

                # The value of the target is measured in distance. Each point added increase the range the ai can look
                # for a better target in the list
                enemyTargetValue = estimatedTotalDist

                # If this target is like me then they aren't a great target so we give extra buffer to look elsewhere
                if potentialTarget.get_type() == self.me.get_type():
                    enemyTargetValue += 5

                # If this target is within range if I move first then they are a better target
                if estimatedTotalDist <= self.me.attack_range + self.me.move_range:
                    enemyTargetValue -= 2
                else:
                    # If this target is too far to attack this turn then they aren't a great target
                    enemyTargetValue += 2

                # If there is not a set target yet or if this target is better than the previous then set this as enemy
                if self.enemy is None or enemyTargetValue < self.enemyValue:
                    self.enemy = potentialTarget
                    self.enemyX = potentialTargetX
                    self.enemyY = potentialTargetY
                    self.estimatedEnemyDistance = estimatedTotalDist
                    self.enemyValue = enemyTargetValue

    def build_path_to_target(self):
        """Function to decide where to move the ai on the map. Returns x Coord to move to, y Coord to move to, target id
        to attack this turn. based on A*
        """
        self.listToSearch = []
        # Reset all the nodes and add the start node to the list
        for node in self._nodeTree:
            node.clear_data()
            if node.get_xPos() == self.myX and node.get_yPos() == self.myY:
                self.startNode = node
                self.startNode.set_distanceToGoal(self.enemyX, self.enemyY)
                self.listToSearch.append(node)

        self.closestNode = self.startNode

        while len(self.listToSearch) > 0:
            currentNode = self.listToSearch[0]
            currentNodeIndex = 0
            counter = 0

            # Find the node with the smallest distance to the goal
            for tile in self.listToSearch:
                if tile.get_finalCost() < currentNode.get_finalCost():
                    currentNode = tile
                    currentNodeIndex = counter
                counter += 1
            self.listToSearch.pop(currentNodeIndex)

            if currentNode.get_distanceToGoal() < self.closestNode.get_distanceToGoal():
                self.closestNode = currentNode

            # Found the enemy position in the nodeTree
            if currentNode.get_xPos() == self.enemyX and currentNode.get_yPos() == self.enemyY:
                self.endNode = currentNode
                self.set_enemy_path_distance()
                return

            if currentNode.get_distanceToGoal() <= self.me.attack_range:
                self.endNode = currentNode
                self.set_enemy_path_distance()
                return

            # check if the node neighbors have been seen before if so check best path, if not add to list
            for neighbor in currentNode.get_neighbors():
                # TODO determine what to do about occupied spaces
                if self._copyOfMapData.tilemap[neighbor.get_yPos()][neighbor.get_xPos()].is_occupied:
                    if neighbor.get_xPos() != self.enemyX and neighbor.get_yPos() != self.enemyY:
                        continue
                nodeGivenCost = neighbor.calculate_givenCost(currentNode.get_givenCost())
                if neighbor.get_parent() is None and neighbor != self.startNode:
                    neighbor.set_parent(currentNode)
                    neighbor.set_givenCost(nodeGivenCost)
                    neighbor.set_distanceToGoal(self.enemyX, self.enemyY)
                    neighbor.set_finalCost()
                    self.listToSearch.append(neighbor)
                elif neighbor.get_parent() is not None:
                    if nodeGivenCost < neighbor.get_givenCost():
                        neighbor.set_givenCost(nodeGivenCost)
                        neighbor.set_parent(currentNode)
                        neighbor.set_finalCost()

        if self.endNode is None:
            self.endNode = self.closestNode
            self.distanceToFar = True

    def set_enemy_path_distance(self):
        counter = 0
        currentNode = self.endNode
        while currentNode.get_parent() is not None:
            currentNode = currentNode.get_parent()
            counter += 1
        self.enemyPathDistance = counter

    def set_ai_goal_position(self, numberOfNodesToMove):
        currentNode = self.endNode
        if self.endNode.get_xPos() == self.enemyX and self.endNode.get_yPos() == self.enemyY:
            # Stop next to enemy
            numberOfNodesToMove -= 1
            for _ in range(self.enemyPathDistance - numberOfNodesToMove):
                currentNode = currentNode.get_parent()
            self._goalX = (currentNode.get_xPos() * 60) + 30
            self._goalY = (currentNode.get_yPos() * 60) + 30
        else:
            if self.enemyPathDistance < numberOfNodesToMove:
                self._goalX = (self.endNode.get_xPos() * 60) + 30
                self._goalY = (self.endNode.get_yPos() * 60) + 30
            else:
                for _ in range(self.enemyPathDistance - numberOfNodesToMove):
                    currentNode = currentNode.get_parent()
                self._goalX = (currentNode.get_xPos() * 60) + 30
                self._goalY = (currentNode.get_yPos() * 60) + 30

    def decide_ai_action(self):
        """Function decides if ai should only attack (next to enemy already), move twice (no enemy in range), or move then
        attack. Returns desired ai xcoord, ycoord, and target id"""
        self.decide_who_to_attack()

        # If no enemies left to attack return all None to end game
        if self.enemy is None:
            return None, None, None

        if self.enemyNextToMe or self.estimatedEnemyDistance <= self.me.attack_range:
            return None, None, self.enemy.get_id()
        else:
            self.build_path_to_target()
            if self.me.get_type() == 'knight':
                if self.enemyPathDistance >= (self.me.move_range + self.me.attack_range):
                    self.set_ai_goal_position(self.me.move_range + math.floor(self.me.move_range * .5))
                    return self._goalX, self._goalY, None
                else:
                    self.set_ai_goal_position(self.me.move_range)
                    if abs(self._goalX - self.enemyX) + abs(self._goalY - self.enemyY) > 1:
                        return self._goalX, self._goalY, None
                    else:
                        return self._goalX, self._goalY, self.enemy.get_id()
            else:
                if self.enemyPathDistance > self.me.move_range or self.distanceToFar:
                    self.set_ai_goal_position(self.me.move_range + math.floor(self.me.move_range * .5))
                    return self._goalX, self._goalY, None
                else:
                    self.set_ai_goal_position(self.me.move_range)
                    return self._goalX, self._goalY, self.enemy.get_id()
