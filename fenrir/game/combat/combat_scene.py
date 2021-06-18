""" Template module

"""


from fenrir.common.scene import Scene
from fenrir.game.combat.combat_map_data import *


class CombatScene(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.level = Level()

    def handle_event(self, event):
        pass

    def render(self):
        pass

    def update(self):
        pass

