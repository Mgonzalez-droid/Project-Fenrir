""" .. module:: scene
    :synopsis: Module will load combat mode into game

"""

import os
import pygame
from fenrir.common.scene import Scene
import fenrir.game.menu.menu_scene as menuscene
from fenrir.game.combat.combat_chars import MageChar, KnightChar
import fenrir.game.combat.combat_map_data as md
from fenrir.common.config import Colors, PATH_TO_RESOURCES
from fenrir.game.combat.combat_initiative_system import CombatInitiativeSystem


class CombatScene(Scene):

    def __init__(self, screen, map_name):
        super().__init__(screen)
        self._map_name = map_name
        self._map = md.MapData(map_name, 23, 13)
        self._background = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "combat_maps", str(map_name + ".png")))
        self._participants = []
        self._player_list = pygame.sprite.Group()

        # Player char
        self._participants.append(KnightChar(0, 5, False))

        # Enemy char
        self._participants.append(MageChar(1, 10, True))

        # used for displaying on screen surface
        for player in self._participants:
            self._player_list.add(player)

        # starts initiative system and sets current player and next player up
        self.initiative_system = CombatInitiativeSystem(self._participants)
        self.curr_player = self.initiative_system.get_current_player()  # first player to go
        self.next_player = self.initiative_system.get_next_player_up()  # next player in the queue

        self.spawn_participants()

    def handle_event(self, event):
        """Example event handling. Will return to main menu if you press q
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.switch_to_scene(menuscene.MainMenuScene(self.screen))
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                # down key
                pass
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                # left key
                pass
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                # up key
                pass
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                # right key
                pass
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # example updating initiative system
                self.initiative_system.update_system()
                self.curr_player = self.initiative_system.get_current_player()
                self.next_player = self.initiative_system.get_next_player_up()

    def render(self):
        self.screen.fill(Colors.WHITE.value)
        self.screen.blit(self._background, (0, 0))
        self._player_list.draw(self.screen)

    def update(self):
        for player in self._player_list:
            player.update()

    def spawn_participants(self):
        for player in self._participants:
            if player.get_is_enemy():
                for tile in self._map.enemyspawn:
                    if not tile.is_occupied():
                        player.rect.center = (tile.x_coord + 30, tile.y_coord + 30)
                        break
            else:
                for tile in self._map.playerspawn:
                    if not tile.is_occupied():
                        player.rect.center = (tile.x_coord + 30, tile.y_coord + 30)
                        break
