""" .. module:: scene
    :synopsis: Module will load combat mode into game
"""

import os
import pygame
from fenrir.common.scene import Scene
from fenrir.common.TextBox import TextBox
import fenrir.game.overworld.overworld_scene as overscene
from fenrir.common.music import Music
from fenrir.game.combat.combat_chars import MageChar, KnightChar
import fenrir.game.combat.combat_map_data as md
from fenrir.common.config import Colors, PATH_TO_RESOURCES
from fenrir.game.combat.combat_initiative_system import CombatInitiativeSystem
from fenrir.game.combat.combat_grid_system import CombatGridSystem
from fenrir.game.combat.combat_move_list import combat_move_list

# Todo import ai node tree and instantiate it
from fenrir.game.combat.combat_ai_system import CombatAISystem
from fenrir.game.combat.combat_ai_nodeTree import CombatAINodeTree


class CombatScene(Scene):

    def __init__(self, screen, game_state, map_name):
        super().__init__(screen, game_state)
        self._map_name = map_name
        self._map = md.MapData(map_name, 16, 9)
        self._ai_Tree_init = CombatAINodeTree(16, 9, self._map)
        self._ai_Tree = self._ai_Tree_init.get_ai_node_tree()
        self._background = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "combat_maps", str(map_name + ".png")))
        self._participants = []
        self._player_list = pygame.sprite.Group()
        self._combat_grid_system = CombatGridSystem(9, 16, self.screen)

        self._textbox = TextBox(self.screen)

        # Play Music
        Music.play_song("The Arrival (BATTLE II)")

        # Player char
        self._participants.append(KnightChar(0, 1, False))

        # Enemy char
        self._participants.append(MageChar(1, 1, True))

        # used for displaying on screen surface
        for player in self._participants:
            self._player_list.add(player)

        # starts initiative system and sets current player and next player up
        self.initiative_system = CombatInitiativeSystem(self._participants)
        self.curr_player = self.initiative_system.get_current_player()  # first player to go
        self.next_player = self.initiative_system.get_next_player_up()  # next player in the queue

        # key binding values
        self.key_dict = {'SELECT': False, 'BACK': False, '1': False, '2': False, '3': False, 'L_CLICK': False}
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
        self.player_attacking = False
        self.attack_complete = False
        self.player_moving = False
        self.move_complete = False
        self.ai_thinking = False
        self.ai_completed_decision = True  # this flag will be set when AI is thinking and True when not thinking
        self.enemy_attack_after_move = False
        self.movement_info = ""
        self.attack_info = ""

        # used for enemy choices
        self.enemy_attacked = False
        self.enemy_moved = False

        # game won info
        self.game_over = False
        self.player_won = False

        # quitting combat screen
        self._quit_screen = False

        # used for highlighting current player
        self._highlight_curr_player = False
        self._move_list = []
        self._move_selected = False

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.key_dict['L_CLICK'] = True

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def render(self):
        self.screen.fill(Colors.WHITE.value)
        self.screen.blit(self._background, (0, 0))
        self._combat_grid_system.draw_grid(self.mouse_x, self.mouse_y, self.curr_player.xpos, self.curr_player.ypos,
                                           self._highlight_curr_player)
        self._player_list.draw(self.screen)
        self._combat_grid_system.clear_highlights()
        if self.show_text_box:
            tb = TextBox(self.screen)
            tb.load_textbox(300, 370, 600, 100)
            tb.draw_options(self.prompt, self.prompt_options, 24, 210, 400)

        if self.show_text_box and not self._quit_screen:
            self._textbox.load_textbox(300, 370, 600, 100)
            self._textbox.draw_options(self.prompt, self.prompt_options, 24, 210, 400)

        if self._quit_screen:
            self._textbox.load_textbox(400, 150, 400, 150)
            options = ["[Y]    YES", "[N]    NO"]
            size = 24
            x, y = 320, 200
            self._textbox.draw_options("Are you sure you want to quit?", options, size, x, y)

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
        self._move_selected = False
        self.attack_info = ""
        self.movement_info = ""

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

        self.show_prompt("Click tile to move to!", ["[b] Cancel"])

        if self.key_dict['BACK']:
            self.player_moving = False
            self.clear_prompt()
        elif self.key_dict['L_CLICK']:
            # Need to have unit object
            # selectable_tiles needs to be created upon a player selecting they want to move and cleared after
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
                self.curr_player.move_to((self._move_list[-1].get_xPos() * 60) + 30,
                                         (self._move_list[-1].get_yPos() * 60) + 30)
                self._move_list.pop()
                self._highlight_curr_player = False
                self._move_selected = True
                self._combat_grid_system.clear_highlights()

        if self.move_complete:
            self.show_prompt(f"{self.game_state.player_name}'s Turn", [f"You Moved!"])
            # need to clear highlights after move complete
            if not self.curr_player.is_animating():
                self.next_move()
        elif self._move_list:
            if not self.curr_player.is_animating():
                self.curr_player.move_to((self._move_list[-1].get_xPos() * 60) + 30,
                                         (self._move_list[-1].get_yPos() * 60) + 30)
                self._move_list.pop()

            if not self._move_list:
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
            end_tile = self.select_tile()
            selectable = False
            for tile in attack_tiles:
                if tile.id == end_tile:
                    selectable = True
            if selectable:
                # will be used to get player on tile to attack
                x = int(end_tile[0] // 60) * 60 + 30
                y = int(end_tile[1] // 60) * 60 + 30
                self.curr_player.attack_enemy()
                self.attack_complete = True

        if self.attack_complete:
            self._highlight_curr_player = False
            self.show_prompt(f"{self.game_state.player_name}'s Turn", [f"You attacked {self.attack_info}!"])
            # need to clear highlights after move complete
            self._combat_grid_system.clear_highlights()
            if not self.curr_player.is_animating():
                self.next_move()

    def check_for_winner(self):
        player = False
        enemy = False

        for player in self._participants:
            if player.alive:
                if player.get_is_enemy():
                    enemy = True
                else:
                    player = True

        if not player:
            self.player_won = False
            self.game_over = True
        elif not enemy:
            self.player_won = False
            self.game_over = True

    ##########################################################################
    # Co Routine that is called each time in the loop and handles game logic #
    ##########################################################################

    def play_game(self):
        self.check_for_winner()

        if self.game_over:
            self.clear_prompt()
            # Need data to show who one ect...
            if self.player_won:
                winner = self.game_state.player_name
            else:
                winner = "Sensei"

            self.show_prompt("Battle Complete",
                             [f"{winner} won the battle!", "Press [enter] to return to overworld"])

            if self.key_dict['SELECT']:
                # Todo this will increase player level now regardless of victory or not. Need to update this later
                self.game_state.increase_player_level()
                self.switch_to_scene(overscene.OverworldScene(self.screen, self.game_state))

        elif self.turn_counter == 0:
            self.show_prompt("Welcome to combat", ["Press [Enter] to get started"])
            if self.key_dict['SELECT']:
                self.clear_prompt()
                self.turn_counter += 1
        else:
            if self.curr_player.get_is_enemy():
                if not self.ai_thinking:
                    self.show_prompt("Sensei's Turn", ["Sensei is deciding..."])
                    self.ai_thinking = True
                    self.ai_completed_decision = False

                    #####################
                    # AI Turn  - Start  #
                    #####################

                    # Determines target, builds path to target
                    ai_brain = CombatAISystem(self._participants, self.curr_player, self._ai_Tree, self._map)
                    ai_new_x, ai_new_y, target_to_attack = ai_brain.decide_ai_action()

                    # if there is no movement and no target then game is over
                    if ai_new_x is None and ai_new_y is None and target_to_attack is None:
                        self.ai_thinking = True
                        self.game_over = True

                    # if there is a movement that needs to be made
                    elif self.curr_player.xpos != ai_new_x or self.curr_player.ypos != ai_new_y:
                        self._map.tilemap[(self.curr_player.ypos - 30) // 60][
                            (self.curr_player.xpos - 30) // 60].unoccupy()
                        # if this is a mage they teleport
                        if self.curr_player.get_type() == "mage":
                            self.curr_player.move_to(ai_new_x, ai_new_y)
                        else:
                            # set parameters for building the list of tiles to move through (for knight and archer)
                            startingX = int((self.curr_player.xpos - 30) / 60)
                            startingY = int((self.curr_player.ypos - 30) / 60)
                            endingX = int((ai_new_x - 30) / 60)
                            endingY = int((ai_new_y - 30) / 60)
                            moveList = combat_move_list(startingX, startingY, endingX, endingY, self._ai_Tree,
                                                        self._map)
                            # move animation loop
                            # TODO add a wait function so the animation can complete
                            while len(moveList) > 0:
                                self.curr_player.move_to((moveList[-1].get_xPos() * 60) + 30,
                                                         (moveList[-1].get_yPos() * 60) + 30)
                                moveList.pop()

                        # update map file to unoccupy the current tile and occupy the new tile
                        self._map.tilemap[(ai_new_y - 30) // 60][(ai_new_x - 30) // 60].occupy(
                            self.curr_player.get_id())
                        self.enemy_moved = True

                    # if there is a target to attack this turn
                    if target_to_attack is not None:
                        for character in self._participants:
                            if character.get_id() == target_to_attack:
                                if self.curr_player.get_type() == 'mage':
                                    character.take_damage(self.curr_player.magic_attack, 'magic')
                                    self.enemy_attacked = True,
                                    self.curr_player.attack_enemy()
                                    self.ai_completed_decision = True
                                else:
                                    character.take_damage(self.curr_player.attack, 'physical')
                                    self.enemy_attacked = True
                                    self.enemy_attack_after_move = True
                                    self.ai_completed_decision = True
                                break
                    else:
                        self.ai_completed_decision = True

                    #####################
                    # AI Turn  - Finish #
                    #####################

                elif self.enemy_attack_after_move and not self.curr_player.is_animating():

                    self.curr_player.attack_enemy()
                    self.enemy_attack_after_move = False
                    self.ai_thinking = False

                elif not self.curr_player.is_animating() and self.ai_completed_decision:
                    self.clear_prompt()
                    if self.enemy_moved and self.enemy_attacked:
                        enemy_choice = "moved and attacked!"
                    elif self.enemy_moved:
                        enemy_choice = "moved!"
                    else:
                        enemy_choice = "attacked!"

                    self.show_prompt("Sensei's turn", [f"Sensei {enemy_choice}!", "Press [Enter] to continue..."])
                    if self.key_dict['SELECT']:
                        self.ai_thinking = False
                        self.enemy_moved = False
                        self.enemy_attacked = False
                        self.next_move()
            else:
                if not self.player_attacking and not self.player_moving:
                    self._highlight_curr_player = True
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
                if not tile.is_occupied and not tile.is_wall and not tile.is_blocking:
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
                            if not tile.is_occupied and not tile.is_wall and not tile.is_blocking:
                                new_tiles.append(tile)
                        elif select_type == "attack":
                            if not tile.is_wall:
                                new_tiles.append(tile)
            selectable_tiles.extend(new_tiles)
            input_range -= 1
        s_tile_ids = []
        final_selectable_tiles = []
        for tile in selectable_tiles:
            if tile.id not in s_tile_ids:
                s_tile_ids.append(tile.id)
        for tile_id in s_tile_ids:
            final_selectable_tiles.append(combat_map[int(tile_id[1] / 60)][int(tile_id[0] / 60)])
        return final_selectable_tiles
