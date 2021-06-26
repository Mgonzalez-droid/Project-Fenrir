""" .. module:: scene
    :synopsis: Module will load combat mode into game

"""

import os
import pygame
from fenrir.common.scene import Scene
from fenrir.common.TextBox import TextBox
import fenrir.game.menu.menu_scene as menuscene
from fenrir.game.combat.combat_chars import MageChar, KnightChar
import fenrir.game.combat.combat_map_data as md
from fenrir.common.config import Colors, PATH_TO_RESOURCES
from fenrir.game.combat.combat_initiative_system import CombatInitiativeSystem

# Todo import ai node tree and instantiate it
from fenrir.game.combat.combat_ai_system import CombatAISystem
from fenrir.game.combat.combat_ai_nodeTree import CombatAINodeTree


class CombatScene(Scene):

    def __init__(self, screen, map_name):
        super().__init__(screen)
        self._map_name = map_name
        self._map = md.MapData(map_name, 16, 9)
        self._ai_Tree = CombatAINodeTree(16, 9, self._map)
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

        # key binding values
        self.key_dict = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False, 'SELECT': False, 'BACK': False,
                         '1': False, '2': False, '3': False, '4': False, '5': False}

        # spawn players to the map
        self.spawn_participants()

        # attrs used for text box
        self.show_text_box = False
        self.prompt = ""
        self.prompt_options = ""

        # used for keeping track of game turns and updating game
        self.turn_counter = 0
        self.enemy_turn = False
        self.player_turn = False

        # used for player choices
        self.player_attacking = False
        self.attack_complete = False
        self.player_moving = False
        self.move_complete = False
        self.movement_info = ""
        self.attack_info = ""

    def handle_event(self, event):
        """Example event handling. Will return to main menu if you press q
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                # currently the q button will quit and return to main menu
                # TODO make a dialogue with text box (Are you sure? Yes/No) ...
                self.switch_to_scene(menuscene.MainMenuScene)
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.key_dict['DOWN'] = True
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.key_dict['LEFT'] = True
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                self.key_dict['UP'] = True
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.key_dict['RIGHT'] = True
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.key_dict['SELECT'] = True
            elif event.key == pygame.K_b:
                self.key_dict['BACK'] = True
            elif event.key == pygame.K_1:
                self.key_dict['1'] = True
            elif event.key == pygame.K_2:
                self.key_dict['2'] = True
            elif event.key == pygame.K_3:
                self.key_dict['3'] = True
            elif event.key == pygame.K_4:
                self.key_dict['4'] = True
            elif event.key == pygame.K_5:
                self.key_dict['5'] = True

    def render(self):
        self.screen.fill(Colors.WHITE.value)
        self.screen.blit(self._background, (0, 0))
        self._player_list.draw(self.screen)

        if self.show_text_box:
            tb = TextBox(self.screen)
            tb.load_textbox()
            tb.draw_options(self.prompt, self.prompt_options, 24, 210, 400)

    def update(self):
        self.play_game()

        for player in self._player_list:
            player.update()

    #########################################
    # Helper functions for combat game play #
    #########################################

    def spawn_participants(self):
        for player in self._participants:
            if player.get_is_enemy():
                for tile in self._map.enemyspawn:
                    if not tile.is_occupied:
                        player.rect.center = (tile.x_coord + 30, tile.y_coord + 30)
                        tile.occupy(player.get_id())
                        break
            else:
                for tile in self._map.playerspawn:
                    if not tile.is_occupied:
                        player.rect.center = (tile.x_coord + 30, tile.y_coord + 30)
                        tile.occupy(player.get_id())
                        break

    def reset_keys(self):
        for key in self.key_dict:
            self.key_dict[key] = False

    def show_prompt(self, prompt, options):
        self.prompt = prompt
        self.prompt_options = options
        self.show_text_box = True

    def clear_prompt(self):
        self.show_text_box = False
        self.prompt = ""
        self.prompt_options = ""

    def update_initiative_system(self):
        self.initiative_system.update_system()
        self.curr_player = self.initiative_system.get_current_player()
        self.next_player = self.initiative_system.get_next_player_up()

    def next_move(self):
        # this function resets all the logic needed to move to next turn

        self.update_initiative_system()
        self.clear_prompt()
        self.reset_keys()
        self.turn_counter += 1
        self.player_attacking = False
        self.attack_complete = False
        self.player_moving = False
        self.move_complete = False
        self.attack_info = ""
        self.movement_info = ""
        self.get_prompt_directions()

    def get_prompt_directions(self):
        x, y = self.curr_player.get_tile_loc()

        # this logic should be handled in the tile map data but there is bugs with indexs
        # and return wrong results for adjacent tiles

        return ["[w] Up --- [s] Down --- [a] Left --- [d] Right", "[b] Cancel"]

    def process_player_move(self):
        self.player_moving = True

        if self.key_dict['BACK']:
            self.player_moving = False
            self.clear_prompt()
        elif self.key_dict['UP']:
            self.curr_player.move(0, -60)
            self.movement_info = "UP"
            self.move_complete = True
        elif self.key_dict['DOWN']:
            self.curr_player.move(0, 60)
            self.movement_info = "DOWN"
            self.move_complete = True
        elif self.key_dict['LEFT']:
            self.curr_player.move(-60, 0)
            self.movement_info = "LEFT"
            self.move_complete = True
        elif self.key_dict['RIGHT']:
            self.curr_player.move(60, 0)
            self.movement_info = "RIGHT"
            self.move_complete = True

        if self.move_complete:
            self.show_prompt(f"Player Moved {self.movement_info}!", [])
            if not self.curr_player.is_animating():
                self.next_move()

    def process_player_attack(self):
        self.player_attacking = True

        if self.key_dict['BACK']:
            self.player_attacking = False
            self.attack_complete = True
        elif self.key_dict['UP']:
            self.curr_player.attack_enemy()
            self.attack_info = "UP"
            self.attack_complete = True
        elif self.key_dict['DOWN']:
            self.curr_player.attack_enemy()
            self.attack_info = "DOWN"
            self.attack_complete = True
        elif self.key_dict['LEFT']:
            self.curr_player.attack_enemy(True)
            self.attack_info = "LEFT"
            self.attack_complete = True
        elif self.key_dict['RIGHT']:
            self.curr_player.attack_enemy(False)
            self.attack_info = "RIGHT"
            self.attack_complete = True

        if self.attack_complete:
            self.show_prompt(f"Player Attacked {self.attack_info}", [])
            if not self.curr_player.is_animating():
                self.next_move()

    ##########################################################################
    # Co Routine that is called each time in the loop and handles game logic #
    ##########################################################################

    def play_game(self):

        if self.turn_counter == 0:
            self.show_prompt("Welcome to combat", ["Press [Enter] to get started"])
            if self.key_dict['SELECT']:
                self.clear_prompt()
                self.turn_counter += 1
        else:
            if self.curr_player.get_is_enemy():
                self.show_prompt("Enemy Turn", ["Enemy is deciding...", "***Temporary*** Press [Enter] for next turn"])

                #####################
                # AI Turn  - Start  #
                #####################
                # Determines target, builds path to target
                ai_brain = CombatAISystem(self._participants, self.curr_player, self._ai_Tree, self._map)
                ai_new_x, ai_new_y, target_to_attack = ai_brain.decide_ai_action()
                if target_to_attack is None:
                    self.curr_player.move_to(ai_new_x, ai_new_y)
                else:
                    if self.curr_player.xpos != ai_new_x and self.curr_player.ypos != ai_new_y:
                        self.curr_player.move_to(0, 0)
                    for character in self._participants:
                        if character.get_id() == target_to_attack:
                            if self.curr_player.get_type() == 'mage':
                                character.take_damage(self.curr_player.magic_attack, 'magic')
                            else:
                                character.take_damage(self.curr_player.attack, 'physical')
                            break
                #####################
                # AI Turn  - Finish #
                #####################

                if self.key_dict["SELECT"]:
                    self.next_move()
            else:
                if not self.player_attacking and not self.player_moving:
                    self.show_prompt("Your turn!", ["[1] Attack", "[2] Move"])
                    if self.key_dict['1']:
                        self.player_attacking = True
                        self.clear_prompt()
                        self.reset_keys()
                    elif self.key_dict['2']:
                        self.player_moving = True
                        self.clear_prompt()
                        self.reset_keys()
                elif self.player_attacking:
                    self.show_prompt("Which direction do you want to attack?", self.get_prompt_directions())
                    self.process_player_attack()
                elif self.player_moving:
                    self.show_prompt("Which direction do you want to move?", self.get_prompt_directions())
                    self.process_player_move()

        self.reset_keys()
