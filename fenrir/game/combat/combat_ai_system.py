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
    def __init__(self, participants, currentParticipant, tileMap):
        self._list_of_enemies = participants
        self._me = currentParticipant
        self._myXPos = self._me.xpos
        self._myYPos = self._me.ypos
        self._target = participants[0]
        self._opponentScore = 0
        self._targetDistance = 0
        self._targetNextToMe = False
        self._tileMap = tileMap

    def decide_who_to_attack(self):
        """Function to decide on what character to attack. Based on distance, hp, (type based considerations
        """
        for i in self._list_of_enemies:
            if not i.get_is_enemy() and i.hp > 0:
                tempScore = 0
                xDist = abs(self._myXPos - i.xpos)
                yDist = abs(self._myYPos - i.ypos)
                totalDist = xDist + yDist
                if totalDist == 1:
                    self._targetNextToMe = True
                    self._targetDistance = 1
                    self._target = i
                    break
                if totalDist <= self._me.attck_range:
                    tempScore += 10
                elif totalDist <= self._me.move_range + self._me.attck_range:
                    if totalDist < self._me.move_range:
                        tempScore += 8
                    else:
                        tempScore += 5
                if i.hp < self._me.attack or i.hp < self._me.magic_attack:
                    tempScore += 10
                elif i.hp <= self._me.hp:
                    tempScore += 8
                else:
                    tempScore += 5

                if tempScore >= self._opponentScore:
                    self._opponentScore = tempScore
                    self._target = i
                    self._targetDistance = totalDist


    def decide_where_to_move(self, numberOfTilesToMove):
        """Function to decide where to move the ai on the map. Returns x Coord to move to, y Coord to move to, target id
        to attack this turn
        """
        myX = self._myXPos
        myY = self._myYPos
        targetX = self._target.xpos
        targetY = self._target.ypos
        print("Where to move")

    def decide_ai_action(self):
        """Function decides if ai should only attack (next to enemy already), move twice (no enemy in range), or move then
        attack. Returns desired ai xcoord, ycoord, and target id"""
        self.decide_who_to_attack()
        if self.targetNextToMe:
            return self._myXPos, self._myYPos, self._target.get_id()
        elif self._targetDistance > (self._me.move_range + self._me.attck_range):
            self.decide_where_to_move(self._me.move_range + math.floor(self._me.move_range * .5))
            return self._myXPos, self._myYPos, None
        else:
            self.decide_where_to_move(self._me.move_range)
            return self._myXPos, self._myYPos, self._target.get_id()
