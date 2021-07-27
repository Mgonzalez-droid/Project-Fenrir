""" .. module:: scene
    :synopsis: Module will load combat mode into game
"""

import os
import pygame
from fenrir.common.scene import Scene
from fenrir.common.TextBox import TextBox
import fenrir.game.overworld.overworld_scene_hub as overscene
from fenrir.game.combat.combat_chars import ArcherChar, KnightChar, MageChar
import fenrir.game.combat.combat_map_data as md
from fenrir.common.config import Colors, DisplaySettings, PATH_TO_RESOURCES, GameConstants
from fenrir.game.combat.combat_initiative_system import CombatInitiativeSystem
from fenrir.game.combat.combat_grid_system import CombatGridSystem
from fenrir.game.combat.combat_move_list import combat_move_list

# Todo import ai node tree and instantiate it
from fenrir.game.combat.combat_ai_system import CombatAISystem
from fenrir.game.combat.combat_ai_nodeTree import CombatAINodeTree


class CombatScene(Scene):

    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self._map_name = "combat_" + self.game_state.game_state_current_map
        self._map = md.MapData(self._map_name, 16, 9)
        self._ai_Tree_init = CombatAINodeTree(16, 9, self._map)
        self._ai_Tree = self._ai_Tree_init.get_ai_node_tree()
        self._background = pygame.image.load(
            os.path.join(PATH_TO_RESOURCES, "combat_maps", str(self._map_name + ".png")))
        self._participants = self.add_participants()
        self._player_list = pygame.sprite.Group()
        self._combat_grid_system = CombatGridSystem(9, 16, self.screen)

        self._textbox = TextBox(self.screen)
        # used to hide large prompt in middle of screen
        self._hide_prompt = False

        # Play Music
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(PATH_TO_RESOURCES, "soundtrack", "The Arrival (BATTLE II).wav"))
        pygame.mixer.music.set_volume(.4)
        pygame.mixer.music.play(-1)
        self._sound_effects = {}

        # used for displaying on screen surface
        for player in self._participants:
            self._player_list.add(player)

        # starts initiative system and sets current player and next player up
        self.initiative_system = CombatInitiativeSystem(self._participants)
        self.curr_player = self.initiative_system.get_current_player()  # first player to go
        self.next_player = self.initiative_system.get_next_player_up()  # next player in the queue

        # key binding values
        self.key_dict = {'SELECT': False, 'BACK': False, '1': False, '2': False,
                         '3': False, 'L_CLICK': False, 'R_CLICK': False, 'SPACE': False}
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

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
        self.wait_for_action = False  # This flag will prevent multiple inputs while an action is being animated
        self.player_attacking = False
        self.attack_complete = False
        self.player_moving = False
        self.move_complete = False
        self.move_counter = 2
        self.player_used_attack = False
        self.ai_thinking = False
        self.ai_completed_decision = True  # this flag will be set when AI is thinking and True when not thinking
        self.enemy_attack_after_move = False

        # used for enemy choices
        self.enemy_attacked = False
        self.enemy_moved = False

        # ai values
        self.ai_new_x = None
        self.ai_new_y = None
        self.target_to_attack = None
        self.ai_brain = None
        self.ai_first_pass = False
        self.ai_turn_finished = False
        self.ai_movement_finished = False
        self.ai_attack_finished = False

        # game won info
        self.game_over = False
        self.player_won = False
        # used to only play victory sound once
        self.played_victory_sound = False

        # used for killing players
        self.dead_player = None

        # quitting combat screen
        self._quit_screen = False

        # used for highlighting current player
        self._highlight_curr_player = False
        self._move_list = []
        self._move_selected = False
        self._attack_selected = False

    def handle_event(self, event):
        """Example event handling. Will return to main menu if you press q
        """

        if event.type == pygame.KEYDOWN:
            if self._quit_screen:
                if event.key == pygame.K_y:
                    self.switch_to_scene(overscene.OverworldScene(self.screen, self.game_state))
                elif event.key == pygame.K_n:
                    self._quit_screen = False
            elif event.key == pygame.K_ESCAPE:
                self._quit_screen = True
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
            elif event.key == pygame.K_SPACE:
                self._hide_prompt = not self._hide_prompt
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.key_dict['L_CLICK'] = True
            if event.button == 3:
                self.key_dict['R_CLICK'] = True

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def render(self):
        self.screen.fill(Colors.WHITE.value)
        self.screen.blit(self._background, (0, 0))
        self._combat_grid_system.draw_grid(self.mouse_x, self.mouse_y, self.curr_player.xpos, self.curr_player.ypos,
                                           self._highlight_curr_player)
        self._player_list.draw(self.screen)

        for player in self._participants:
            player.draw_health_bar(self.screen)

        self._combat_grid_system.clear_highlights()

        if (self.player_attacking or self.player_moving) and (not self._move_selected and not self._attack_selected) \
                and not self._quit_screen:
            self._textbox.load_image(10, DisplaySettings.SCREEN_RESOLUTION.value[1] - 45, 360, 40,
                                     "UI/generic-rpg-ui-text-box.png")
            option = "Attack" if self.player_attacking else "Move"
            self._textbox.draw_dialogue(f"Click tile to {option} or press [b] to cancel", 18, 20,
                                        DisplaySettings.SCREEN_RESOLUTION.value[1] - 42)
        elif self.show_text_box and not self._quit_screen:
            if not self._hide_prompt:
                text_box_height = 40 + 30 * len(self.prompt_options)
                self._textbox.load_image(400, 370, 430, text_box_height, "UI/generic-rpg-ui-text-box.png")
                self._textbox.draw_options(self.prompt, self.prompt_options, 24, 300, 400)
            else:
                self._textbox.load_image(DisplaySettings.SCREEN_RESOLUTION.value[0] - 200,
                                         DisplaySettings.SCREEN_RESOLUTION.value[1] - 75, 290, 40,
                                         "UI/generic-rpg-ui-text-box.png")
                self._textbox.draw_dialogue(f"Press [SPACE] to show prompt.", 18,
                                            DisplaySettings.SCREEN_RESOLUTION.value[0] - 300,
                                            DisplaySettings.SCREEN_RESOLUTION.value[1] - 40)
        elif self._quit_screen:
            self._textbox.load_image(400, 150, 400, 150, "UI/generic-rpg-ui-text-box.png")
            options = ["[Y]    YES", "[N]    NO"]
            size = 24
            x, y = 320, 200
            self._textbox.draw_options("Are you sure you want to quit?", options, size, x, y)

    def update(self):
        self.play_game()
        self._player_list.update()

    #########################################
    # Helper functions for combat game play #
    #########################################
    def add_participants(self):
        participants = []
        unit_id = 0
        player_level = self.game_state.player_level
        for unit in self.game_state.player_party:
            if unit == "knight":
                participants.append(KnightChar(unit_id, player_level, False))
            elif unit == "archer":
                participants.append(ArcherChar(unit_id, player_level, False))
            elif unit == "mage":
                participants.append(MageChar(unit_id, player_level, False))
            unit_id += 1

        enemy_level = self.game_state.enemy_level
        for unit in self.game_state.enemy_party:
            if unit == "knight":
                participants.append(KnightChar(unit_id, enemy_level, True))
            elif unit == "archer":
                participants.append(ArcherChar(unit_id, enemy_level, True))
            elif unit == "mage":
                participants.append(MageChar(unit_id, enemy_level, True))
            unit_id += 1

        return participants

    def spawn_participants(self):
        for player in self._participants:
            if player.get_is_enemy():
                for tile in self._map.enemyspawn:
                    if not tile.is_occupied:
                        player.set_player_loc(tile.x_coord + 30, tile.y_coord + 30)
                        tile.occupy(player.get_id())
                        break
            else:
                for tile in self._map.playerspawn:
                    if not tile.is_occupied:
                        player.set_player_loc(tile.x_coord + 30, tile.y_coord + 30)
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
        # will update initiative system with new list if player was removed
        self.initiative_system.update_system()
        self.curr_player = self.initiative_system.get_current_player()
        self.next_player = self.initiative_system.get_next_player_up()

    def next_move(self):
        # this function resets all the logic needed to move to next turn
        self.clear_prompt()
        self.reset_keys()
        self.turn_counter += 1
        self.player_attacking = False
        self.attack_complete = False
        self.player_moving = False
        self.move_complete = False
        self._move_selected = False
        self.move_counter = 2
        self.player_used_attack = False
        self._hide_prompt = False
        self.ai_first_pass = False
        self.ai_turn_finished = False
        self.ai_movement_finished = False
        self.ai_attack_finished = False
        self.update_initiative_system()

    def remove_dead_players(self):
        index = 0
        for player in self._participants:
            if player.hp <= 0:
                self._map.tilemap[(player.ypos - 30) // 60][
                    (player.xpos - 30) // 60].unoccupy()
                self.play_death_sound()
                player.kill_player()
                self.dead_player = player
                self._participants.pop(index)
                self.initiative_system.remove_player(player.get_id())
                return True
            else:
                index += 1

        return False

    def process_player_move(self):
        self.player_moving = True

        movable_tiles = self.find_tiles_in_range(int(self.curr_player.xpos / 60), int(self.curr_player.ypos / 60),
                                                 self.curr_player.move_range, self._map.tilemap, "movement")
        highlight_tiles = []
        for tile in movable_tiles:
            x = int(tile.id[0] / 60)
            y = int(tile.id[1] / 60)
            highlight_tiles.append((y, x))

        if not self._move_selected:
            self._combat_grid_system.highlight_tiles(highlight_tiles, Colors.BLUE.value)
        else:
            self.show_prompt(f"{self.game_state.player_name}'s choice",
                             [f"{self.curr_player.get_type().capitalize()} Moved!"])

        if self.key_dict['BACK']:
            self.player_moving = False
            self.clear_prompt()
        elif self.key_dict['L_CLICK']:
            # Need to have unit object
            # selectable_tiles needs to be created upon a player selecting they want to move and cleared after
            if not self.wait_for_action:
                end_tile = self.select_tile()
                selectable = False
                for tile in movable_tiles:
                    if tile.id == end_tile:
                        selectable = True
                if selectable:
                    startingX = int((self.curr_player.xpos - 30) // 60)
                    startingY = int((self.curr_player.ypos - 30) // 60)
                    endingX = int((end_tile[0]) // 60)
                    endingY = int((end_tile[1]) // 60)
                    self._move_list = combat_move_list(startingX, startingY, endingX, endingY, self._ai_Tree, self._map)

                    # initial move starts here
                    self._map.tilemap[(self.curr_player.ypos - 30) // 60][
                        (self.curr_player.xpos - 30) // 60].unoccupy()
                    self._map.tilemap[endingY][endingX].occupy(self.curr_player.get_id)
                    self.curr_player.move_to((self._move_list[-1].get_xPos() * 60) + 30,
                                             (self._move_list[-1].get_yPos() * 60) + 30)

                    self.play_movement_sound()
                    self._move_list.pop()
                    self._highlight_curr_player = False
                    self._move_selected = True
                    self.wait_for_action = True

                    self._combat_grid_system.clear_highlights()

        if self.move_complete:
            # need to clear highlights after move complete
            if not self.curr_player.is_animating():
                self.player_moving = False
                self._move_selected = False
                self.move_complete = False
                self.wait_for_action = False
                self.move_counter -= 1
        elif self._move_list:
            if not self.curr_player.is_animating():
                self.curr_player.move_to((self._move_list[-1].get_xPos() * 60) + 30,
                                         (self._move_list[-1].get_yPos() * 60) + 30)

                self.play_movement_sound()
                self._move_list.pop()

            if not self._move_list:
                self.move_complete = True
        elif self._move_selected:
            self.move_complete = True

    def process_player_attack(self):
        self.player_attacking = True

        attack_tiles = self.find_tiles_in_range(int(self.curr_player.xpos / 60), int(self.curr_player.ypos / 60),
                                                self.curr_player.attack_range, self._map.tilemap, "attack")
        highlight_tiles = []
        for tile in attack_tiles:
            x = int(tile.id[0] / 60)
            y = int(tile.id[1] / 60)
            highlight_tiles.append((y, x))

        self._combat_grid_system.highlight_tiles(highlight_tiles, Colors.BLUE.value)

        self.show_prompt("Click a tile to attack!",
                         ["[b] Cancel"])

        if self.key_dict['BACK']:
            self.player_attacking = False
            self.clear_prompt()
        elif self.key_dict['L_CLICK']:
            # Need to have unit object
            # selectable_tiles needs to be created upon a player selecting they want to move and cleared after
            if not self.wait_for_action:
                end_tile = self.select_tile()
                selectable = False
                for tile in attack_tiles:
                    if tile.id == end_tile:
                        selectable = True
                if selectable:
                    # will be used to get player on tile to attack
                    x = int(end_tile[0] / 60)
                    y = int(end_tile[1] / 60)
                    enemy_id = self._map.tilemap[y][x].unit
                    for character in self._participants:
                        if character.get_id() == enemy_id:
                            if self.curr_player.get_type() == 'mage':
                                character.take_damage(self.curr_player.magic_attack, 'magic')
                                character.animate_damage()
                            else:
                                character.take_damage(self.curr_player.attack, 'physical')
                                character.animate_damage()
                            break
                    if self.curr_player.xpos == end_tile[0] + 30:
                        left = None
                    else:
                        if self.curr_player.xpos < end_tile[0]:
                            left = False
                        else:
                            left = True
                    self.play_attack_sound()
                    self.curr_player.attack_enemy(left)
                    self.attack_complete = True
                    self.wait_for_action = True

        if self.attack_complete:
            self._highlight_curr_player = False
            self.show_prompt(f"{self.game_state.player_name}'s Turn",
                             [f"{self.curr_player.get_type().capitalize()} attacked!"])
            # need to clear highlights after move complete
            self._combat_grid_system.clear_highlights()
            if not self.curr_player.is_animating():
                self.player_attacking = False
                self.player_used_attack = True
                self.wait_for_action = False
                self.move_counter -= 1

    def check_for_winner(self):
        player_alive = False
        enemy_alive = False

        for player in self._participants:
            if player.get_is_enemy():
                enemy_alive = True
            else:
                player_alive = True

        if not player_alive:
            self.player_won = False
            self.game_over = True
        elif not enemy_alive:
            self.player_won = True
            self.game_over = True

    ##########################################################################
    # Co Routine that is called each time in the loop and handles game logic #
    ##########################################################################

    def play_game(self):

        if self.remove_dead_players():
            self.check_for_winner()
            if self.game_over:
                self.next_move()

        if self.game_over:
            # Need data to show who one ect...
            pygame.mixer.music.stop()
            if self.player_won:
                if self.game_state.player_level == GameConstants.MAX_LEVEL.value:
                    statement = "You are already at the maximum level!"
                else:
                    statement = f"You leveled up to level {self.game_state.player_level + 1}!"

                if not self.played_victory_sound:
                    self.play_sound_effect("victory")
                self.show_prompt("Battle Complete",
                                 [f"You won the battle!",
                                  statement,
                                  "Press [enter] to exit."])
            else:
                if not self.played_victory_sound:
                    self.play_sound_effect("lose")
                self.show_prompt("Battle Complete",
                                 ["Enemy won the battle!",
                                  "Press [enter] to exit."])

            self.played_victory_sound = True

            if self.key_dict['SELECT']:
                self.game_state.increase_player_level()
                pygame.mixer.stop()
                self.switch_to_scene(overscene.OverworldScene(self.screen, self.game_state))

        elif self.turn_counter == 0:
            self.show_prompt("Welcome to combat", ["Press [Enter] to get started!",
                                                   "[Space] will hide prompt."])
            if self.key_dict['SELECT']:
                self.clear_prompt()
                self.turn_counter += 1
        else:
            if self.curr_player.get_is_enemy():
                # if the ai not done with the turn enter
                if not self.ai_turn_finished:
                    self.ai_completed_decision = False

                    #####################
                    # AI Turn  - Start  #
                    #####################

                    # Determines target, builds path to target
                    # Sets up all the flags for the ai turn
                    # Occurs on the first entry into the ai for the turn
                    if not self.ai_first_pass:
                        self.show_prompt("Sensei's Turn", ["Sensei is deciding..."])
                        self.ai_brain = CombatAISystem(self._participants, self.curr_player, self._ai_Tree, self._map)
                        self.ai_new_x, self.ai_new_y, self.target_to_attack = self.ai_brain.decide_ai_action()

                        if self.ai_new_x is not None and self.ai_new_y is not None:
                            self.ai_movement_finished = False
                            self.enemy_moved = True
                        else:
                            self.ai_movement_finished = True
                            self.enemy_moved = False

                        if self.target_to_attack is not None:
                            self.ai_attack_finished = False
                            self.enemy_attacked = True
                        else:
                            self.ai_attack_finished = True
                            self.enemy_attacked = False

                    # if there is no movement and no target then game is over
                    if self.ai_new_x is None and self.ai_new_y is None and self.target_to_attack is None:
                        self.ai_turn_finished = True
                        self.ai_completed_decision = True
                        self.game_over = True

                    # if there is a movement that needs to be made
                    if not self.ai_movement_finished:
                        # if this is a mage they teleport
                        if self.curr_player.get_type() == "mage":
                            self._map.tilemap[(self.curr_player.ypos - 30) // 60][
                                (self.curr_player.xpos - 30) // 60].unoccupy()
                            self._map.tilemap[(self.ai_new_y - 30) // 60][(self.ai_new_x - 30) // 60].occupy(
                                self.curr_player.get_id())
                            self.curr_player.move_to(self.ai_new_x, self.ai_new_y)
                            self._highlight_curr_player = False
                            self.play_movement_sound()
                            self.ai_first_pass = True
                            self.ai_movement_finished = True
                        elif self.curr_player.get_type() != "mage":
                            if not self.ai_first_pass:
                                # set parameters for building the list of tiles to move through (for knight and archer)
                                self._map.tilemap[(self.curr_player.ypos - 30) // 60][
                                    (self.curr_player.xpos - 30) // 60].unoccupy()
                                startingX = int((self.curr_player.xpos - 30) / 60)
                                startingY = int((self.curr_player.ypos - 30) / 60)
                                endingX = int((self.ai_new_x - 30) / 60)
                                endingY = int((self.ai_new_y - 30) / 60)
                                self._move_list = combat_move_list(startingX, startingY, endingX, endingY,
                                                                   self._ai_Tree, self._map)
                                if len(self._move_list) > 0:
                                    self._map.tilemap[(self.curr_player.ypos - 30) // 60][
                                        (self.curr_player.xpos - 30) // 60].unoccupy()
                                    self.curr_player.move_to((self._move_list[-1].get_xPos() * 60) + 30,
                                                             (self._move_list[-1].get_yPos() * 60) + 30)
                                    self._map.tilemap[(self.ai_new_y - 30) // 60][(self.ai_new_x - 30) // 60].occupy(
                                        self.curr_player.get_id())
                                    self._highlight_curr_player = False
                                    self.play_movement_sound()
                                    self.ai_first_pass = True
                                    self._move_list.pop()
                                else:
                                    self.ai_movement_finished = True
                                    self.enemy_moved = False
                                    self.ai_attack_finished = True
                                    self.enemy_attacked = False

                            if self._move_list:
                                if not self.curr_player.is_animating():
                                    self.curr_player.move_to((self._move_list[-1].get_xPos() * 60) + 30,
                                                             (self._move_list[-1].get_yPos() * 60) + 30)
                                    self.play_movement_sound()
                                    self._move_list.pop()
                            else:
                                if not self.curr_player.is_animating():
                                    self.ai_movement_finished = True

                    if self.ai_movement_finished and not self.ai_attack_finished:
                        for character in self._participants:
                            if character.get_id() == self.target_to_attack:
                                if self.curr_player.get_type() == 'mage':
                                    character.take_damage(self.curr_player.magic_attack, 'magic')
                                    character.animate_damage()
                                else:
                                    character.take_damage(self.curr_player.attack, 'physical')
                                    character.animate_damage()
                                self.curr_player.attack_enemy()
                                self.play_attack_sound()
                                self.ai_attack_finished = True
                                break

                    if self.ai_attack_finished and self.ai_movement_finished:
                        self.ai_turn_finished = True
                        self.ai_completed_decision = True
                        if self.enemy_moved and self.enemy_attacked:
                            self.enemy_attack_after_move = True

                    #####################
                    # AI Turn  - Finish #
                    #####################

                elif self.enemy_attack_after_move and not self.curr_player.is_animating():
                    self.enemy_attack_after_move = False

                elif not self.curr_player.is_animating() and self.ai_completed_decision:
                    self.clear_prompt()
                    if self.enemy_moved and self.enemy_attacked:
                        enemy_choice = "moved and attacked!"
                    elif self.enemy_moved:
                        enemy_choice = "moved!"
                    elif self.enemy_attacked:
                        enemy_choice = "attacked!"
                    else:
                        enemy_choice = "skipped Turn!"

                    if self.game_over:
                        self.enemy_moved = False
                        self.enemy_attacked = False
                        self.next_move()
                    else:
                        self.show_prompt("Sensei's turn", [f"Sensei {enemy_choice}!", "[Right Click] to continue..."])
                        if self.key_dict['R_CLICK']:
                            self.enemy_moved = False
                            self.enemy_attacked = False
                            self.next_move()
            else:
                if not self.player_attacking and not self.player_moving:
                    if self.move_counter:
                        # highlights current player on board
                        self._highlight_curr_player = True

                        # options depending on possible moves left
                        choices = ["[1] Move", "[2] Skip Turn"] if self.player_used_attack else ["[1] Move",
                                                                                                 "[2] Attack",
                                                                                                 "[3] Skip Turn"]
                        prompt_text = f"You have {self.move_counter}"
                        if self.move_counter == 2:
                            prompt_text += " choices left"
                        else:
                            prompt_text += " choice left"

                        prompt_text += f" for {self.curr_player.get_type().capitalize()}!"
                        self.show_prompt(prompt_text, choices)

                        # keys depending on choices available
                        if self.key_dict['1']:
                            self.player_moving = True
                            self.clear_prompt()
                            self.reset_keys()
                        elif self.key_dict['2']:
                            if len(choices) == 2:
                                self.next_move()
                            else:
                                self.player_attacking = True
                                self.clear_prompt()
                                self.reset_keys()
                        elif self.key_dict['3']:
                            if len(choices) == 3:
                                self.next_move()
                    else:
                        self.next_move()
                elif self.player_attacking:
                    self.process_player_attack()
                elif self.player_moving:
                    self.process_player_move()

        self.reset_keys()

    def select_tile(self):
        # Checks where the mouse is on screen and returns x, y of a tile when called
        # Should only be called on left click when player move or player attack
        mouse_pos = pygame.mouse.get_pos()
        x_pos = int(mouse_pos[0] / 60) * 60
        y_pos = int(mouse_pos[1] / 60) * 60
        return x_pos, y_pos

    def find_tiles_in_range(self, x_pos, y_pos, input_range, combat_map, select_type):
        selectable_tiles = []
        for tile in combat_map[y_pos][x_pos].adjacencies:
            if select_type == "movement":
                if not tile.is_wall and not tile.is_blocking and not tile.is_occupied:
                    selectable_tiles.append(tile)
            elif select_type == "attack":
                if not tile.is_wall:
                    selectable_tiles.append(tile)
        input_range -= 1
        while input_range > 0:
            new_tiles = []
            for i in range(len(selectable_tiles)):
                for tile in selectable_tiles[i].adjacencies:
                    _unique = True
                    for s_tile in selectable_tiles:
                        if tile.id == s_tile.id:
                            _unique = False
                    if _unique:
                        if select_type == "movement":
                            if not tile.is_wall and not tile.is_blocking and not tile.is_occupied:
                                new_tiles.append(tile)
                        elif select_type == "attack":
                            if not tile.is_wall:
                                new_tiles.append(tile)
            selectable_tiles.extend(new_tiles)
            input_range -= 1
        s_tile_ids = []
        semi_selectable_tiles = []
        final_selectable_tiles = []
        for tile in selectable_tiles:
            if tile.id not in s_tile_ids:
                s_tile_ids.append(tile.id)
        for tile_id in s_tile_ids:
            semi_selectable_tiles.append(combat_map[int(tile_id[1] / 60)][int(tile_id[0] / 60)])
        for tile in semi_selectable_tiles:
            if select_type == "movement":
                final_selectable_tiles = semi_selectable_tiles
            elif select_type == "attack":
                if not tile.is_occupied:
                    final_selectable_tiles.append(tile)
                elif tile.is_occupied:
                    occ = "player"
                    occ_id = tile.unit
                    for units in self._participants:
                        if occ_id == units.get_id() and not units.get_is_enemy():
                            occ = "player"
                        elif occ_id == units.get_id() and units.get_is_enemy():
                            occ = "enemy"
                    if occ == "enemy":
                        final_selectable_tiles.append(tile)
        return final_selectable_tiles

    def play_sound_effect(self, sound_name, time_lim=None):
        # function play sound from library or load it if not there yet

        if sound_name in self._sound_effects.keys():
            sound = self._sound_effects[sound_name]
        else:
            path = os.path.join(PATH_TO_RESOURCES, "soundtrack", "combat_char_sounds", sound_name + ".wav")
            sound = pygame.mixer.Sound(path)
            self._sound_effects[sound_name] = sound
        sound.set_volume(.7)

        # optional time limit for sound effect, currently used for walking to match char pace
        if time_lim:
            sound.play(maxtime=time_lim)
        else:
            sound.play()

    def play_movement_sound(self):
        if self.curr_player.get_type() == "mage":
            self.play_sound_effect("teleport")
        else:
            self.play_sound_effect("walk", 900)

    def play_attack_sound(self):
        self.play_sound_effect("attack_" + self.curr_player.get_type())

    def play_death_sound(self):
        self.play_sound_effect("death")
