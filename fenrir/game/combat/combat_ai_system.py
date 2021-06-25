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
        self.goalX = None
        self.goalY = None
        self._targetX = None
        self._targetY = None
        self._target = None
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

    def decide_where_to_move(self, numberOfTilesToMove, startX, startY):
        """Function to decide where to move the ai on the map. Returns x Coord to move to, y Coord to move to, target id
        to attack this turn
        """
        openList = []
        closedList = []
        for node in self._nodeTree:
            if node.get_xPos() == startX and node.get_yPos() == startY:
                openList.append(node)
                node.set_value(self._targetDistance)
                break

        while len(openList) > 0:
            currentTile = openList[0]
            openList.pop(0)
            closedList.append(currentTile)
            if currentTile.get_xPos() == self._targetX and currentTile.get_yPos() == self._targetY:
                return  # found the end

            for i in range(4):
                alreadySearched = False
                if i == 0:                          # tile above current
                    childTileX = currentTile[0]
                    childTileY = currentTile[1] - 1
                elif i == 1:                        # tile right of current
                    childTileX = currentTile[0] + 1
                    childTileY = currentTile[1]
                elif i == 2:                        # tile below current
                    childTileX = currentTile[0]
                    childTileY = currentTile[1] + 1
                else:                               # tile left of current
                    childTileX = currentTile[0] - 1
                    childTileY = currentTile[1]

                for pair in closedList:
                    if pair[0] == childTileX and pair[1] == childTileY:
                        alreadySearched = True
                        break
                if alreadySearched:
                    continue



                openList.append((childTileX, childTileY))



    def decide_ai_action(self):
        """Function decides if ai should only attack (next to enemy already), move twice (no enemy in range), or move then
        attack. Returns desired ai xcoord, ycoord, and target id"""
        self.decide_who_to_attack()
        if self.targetNextToMe or self._targetDistance <= self._me.attck_range:
            return self._me.xpos, self._me.ypos, self._target.get_id()
        elif self._targetDistance > (self._me.move_range + self._me.attck_range):
            self.decide_where_to_move(self._me.move_range + math.floor(self._me.move_range * .5))
            return self._myXPos, self._myYPos, None
        else:
            self.decide_where_to_move(self._me.move_range)
            return self._myXPos, self._myYPos, self._target.get_id()
