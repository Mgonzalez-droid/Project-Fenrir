import math


class CombatAISystem:
    def __init__(self, participants):
        self._list_of_enemies = participants
        self._target = participants[0]

    def decide_who_to_attack(self):
        for i in self._list_of_enemies:
            if i.get_is_enemy():
                self._target = i
                print("Potential Target")


    def decide_where_to_move(self):
        print("Where to move")
