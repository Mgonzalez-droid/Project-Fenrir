"""Overworld module. Add class properties and args to constructor to change this to diff levels or starting points, etc

"""
import os
import pygame
import fenrir.game.menu.menu_scene as menuscene
import fenrir.game.combat.combat_scene as combscene
from fenrir.common.scene import Scene
from fenrir.common.config import Colors, PATH_TO_RESOURCES
from fenrir.common.TextBox import TextBox
from fenrir.common.music import Music
from fenrir.game.overworld.overworld_npc import overworld_npc as character
from fenrir.game.overworld.overworld_npc_animated import overworld_npc_animated as character_animated
from fenrir.game.overworld.overworld_boundaries import Boundaries
from fenrir.game.overworld.overworld_collisions import Collision
from fenrir.game.overworld.overworld_obstacle import overworld_obstacle as obstacle
from fenrir.data.save_game_to_db import save_game
from fenrir.game.overworld.inventory import Inventory
from fenrir.game.overworld.overworld_world_obj import overworld_world_obj as world_obj


class OverworldScene(Scene):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)

        # new world objs
        self.hub_world = world_obj(
            map_name="hub_world",
            obstacles=[
                obstacle(0, 0, 300, 180),  # Flower_Patch_Barrier
                obstacle(480, 0, 60, 200),  # Left_House_Barrier
                obstacle(550, 0, 88, 165),  # Center_house_Barrier
                obstacle(640, 0, 210, 200),  # House_River_Bridge_Barrier
                obstacle(736, 350, 130, 60),  # bottom_river_Barrier
                obstacle(634, 477, 326, 80),  # Bottom_River_Left_Barrier
                obstacle(0, 410, 180, 139),  # Pond_Barrier
            ],
            entries=[
                obstacle(959, 255, 1, 70),  # World_1_Entry (Dark Dessert/Right Path)
                obstacle(301, 1, 100, 1),  # World_3_Entry (Dark World/ Top Path)
            ],
            entry_dests=[],
            # FILL in with npc data:
            # (x, y, png name, level, party members[], is just text or a choice for the player? (boolean), dialogue[])
            npc=character(880, 255, os.path.join("fenrir/resources/chars/sensei/sensei.png"), 1,
                          [["knight", "chars/knight/knight_menu.png"]], True,
                          ["Hello Gabe, do you wanna go to the combat phase?",
                           "[1] Yes, I am ready to go to the combat phase", "[2] No, I want to keep walking here"]),
            hero_spawn=(self.game_state.game_state_location_x, self.game_state.game_state_location_y),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "overworld_maps/hub_world.png")),
            music="Windless Slopes"
        )

        self.atlantis_world = world_obj(
            map_name="atlantis",
            obstacles=[
                obstacle(0, 0, 189, 229),  # Left_Column_Barrier
                obstacle(189, 0, 208, 119),  # left_entry_Barrier
                obstacle(543, 0, 306, 119),  # Right_Entry
                obstacle(849, 0, 110, 192),  # right_column
                obstacle(378, 191, 30, 141),  # left_barricade
                obstacle(408, 191, 135, 24),  # top_barricade
                obstacle(543, 191, 23, 140),  # right_barricade
                obstacle(766, 298, 87, 84),  # anchor_barrier
                obstacle(0, 342, 69, 198),  # pot_barrier
                obstacle(69, 412, 43, 129),  # half_column_barrier
                obstacle(110, 449, 745, 90),  # sea_wall_barrier
                obstacle(856, 405, 104, 134)  # bottom_right_barrier
            ],
            entries=[
                obstacle(397, 0, 146, 20)  # world_1_entry
            ],
            entry_dests=[
                self.hub_world
            ],
            # FILL in with npc data:
            # (x, y, png name, level, party members[], is just text or a choice for the player? (boolean), dialogue[])
            npc="",
            hero_spawn=(400, 25),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "overworld_maps/atlantis.png")),
            music="Windless Slopes"
        )

        self.ashlands = world_obj(
            map_name="ashlands",
            obstacles=[
                obstacle(0, 0, 280, 170),  # Top left prompts
                obstacle(281, 0, 180, 70),  # Top left stone wall
                obstacle(650, 0, 250, 70),  # Top right stone wall
                obstacle(0, 410, 75, 70),  # Bottom left prompts
                obstacle(200, 410, 70, 1),  # Bottom left prompts (fallen tree)
                obstacle(760, 410, 1, 1),  # Bottom tombstone
                obstacle(740, 280, 1, 1),  # Middle tombstone
                obstacle(860, 160, 1, 1),  # Top tombstone (looks broken)
                obstacle(462, 0, 187, 20)

            ],
            entries=[
                obstacle(1, 240, 1, 100),  # Hub Entry
                obstacle(462, 0, 187, 20),  # Dark_Desert_Boss
            ],
            entry_dests=[],
            # FILL in with npc data:
            # (x, y, png name, level, party members[], is just text or a choice for the player? (boolean), dialogue[])
            npc=character(350, 430, os.path.join("fenrir/resources/chars/hat-guy/hat-guy.png"), 1,
                          [["knight", "chars/knight/knight_menu.png"]], False,
                          ["This is just a test to see if this is working", "And this one too"]),
            hero_spawn=(self.game_state.game_state_location_x, self.game_state.game_state_location_y),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "overworld_maps/ashlands.png")),
            music="Windless Slopes"
        )

        self.dark_dimension = world_obj(
            map_name="dark_dimension",
            obstacles=[
                obstacle(0, 0, 400, 542),  # Main_barrier_left
                obstacle(570, 0, 404, 540),  # Main_barrier_right

            ],
            entries=[
                obstacle(430, 215, 130, 1),  # boss_den_entry
                obstacle(417, 539, 138, 1)  # hub
            ],
            entry_dests=[],
            # FILL in with npc data:
            # (x, y, png name, level, party members[], is just text or a choice for the player? (boolean), dialogue[])
            npc="",
            hero_spawn=(self.game_state.game_state_location_x, self.game_state.game_state_location_y),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "overworld_maps/dark_dimension.png")),
            music="Windless Slopes"
        )

        self.dark_dimension_boss = world_obj(
            map_name="dark_dimension_boss",
            obstacles=[
                obstacle(0, 0, 960, 359),  # Boss_den_top_barrier
                obstacle(0, 358, 380, 180),  # Boss_den_left_barrier
                obstacle(580, 358, 380, 180),  # Boss_den_right_barrier
            ],
            entries=[
                obstacle(410, 539, 130, 1)  # World exit
            ],
            entry_dests=[self.dark_dimension
                         ],
            # FILL in with npc data:
            # (x, y, png name, level, party members[], is just text or a choice for the player? (boolean), dialogue[])
            npc="",
            hero_spawn=(406, 400),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "overworld_maps/dark_dimension_boss.png")),
            music="Windless Slopes"
        )

        self.hub_world.entry_dests = [self.ashlands, self.dark_dimension]
        self.dark_dimension.entry_dests = [self.dark_dimension_boss, self.hub_world]
        self.ashlands.entry_dests = [self.hub_world]

        # Defaults to hub world and hero default position
        self.active_world = self.load_active_world()
        self.active_world.hero_spawn = [self.game_state.game_state_location_x, self.game_state.game_state_location_y]

        self.background = pygame.transform.scale(self.active_world.background, (960, 540))
        self.control_hud = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "controls_HUD.png"))
        self.textbox = TextBox(self.screen)
        self._quit_screen = False
        self.collision = Collision()

        # TODO: Need to add secondary list and behavior for entries...

        self.level = self.game_state.player_level
        self.hero = character_animated(self.active_world.hero_spawn[0], self.active_world.hero_spawn[1],
                                       os.path.join(PATH_TO_RESOURCES, "gabe_best_resolution.png"),
                                       self.game_state.player_level, [["knight", "chars/knight/knight_menu.png"]],
                                       False, [])

        self.hero.sprite_names = ["gabe_stance_0.png", "gabe_stance_1.png", "gabe_stance_2.png", "gabe_stance_3.png",
                                  "gabe_stance_4.png", "gabe_stance_5.png", "gabe_stance_6.png"]

        # pygame.mixer.init()
        # pygame.mixer.music.load(self.active_world.music)
        # pygame.mixer.music.stop()
        # pygame.mixer.music.play()

        Music.play_song(self.active_world.music)

        # Default npc scale and position
        self.active_world.npc.sprite = pygame.transform.flip(self.active_world.npc.sprite, True, False)
        self.active_world.npc.sprite = pygame.transform.scale(self.active_world.npc.sprite, (75, 75))

        self.show_controls = False
        self.show_characters = True
        self.show_interaction = False
        self.show_hud = True
        self.show_textbox = False
        self.show_inventory = False

        # Inventory system
        self.inventory = Inventory(self.textbox, self.hero.party, self.game_state.all_heroes)
        self.party_section = True
        self.party_index = 0
        self.hero_index = 0
        self.text_index = -1

    def handle_event(self, event):

        # TRACK MOVEMENT
        # Boundaries class prevent the player character to move outside the current window
        boundaries = Boundaries(self.screen, self.hero)

        # Player check player movement for up (w), down (s), left (a), right (d)
        keys = pygame.key.get_pressed()

        if not self.show_controls and not self.show_textbox and not self.show_inventory and not self._quit_screen:
            if keys[pygame.K_w]:
                self.hero.y = boundaries.collision_up()  # Check if player hits top of window

                if self.collision.barrier_collision(self.hero, self.active_world.obstacles):
                    # For debugging purposes
                    print("player hit barrier up")
                    self.hero.y += 10

                self.hero.adjust_movement()
            if keys[pygame.K_s]:
                self.hero.y = boundaries.collision_down()  # Check if player hits bottom of window

                if self.collision.barrier_collision(self.hero, self.active_world.obstacles):
                    # For debugging purposes
                    print("player hit barrier down")
                    self.hero.y -= 10

                self.hero.adjust_movement()
            if keys[pygame.K_a]:
                self.hero.x = boundaries.collision_left()  # Check if player hits left of window
                if self.collision.barrier_collision(self.hero, self.active_world.obstacles):
                    # For debugging purposes
                    print("player hit barrier left")
                    self.hero.x += 10

                self.hero.adjust_movement()
            if keys[pygame.K_d]:
                self.hero.x = boundaries.collision_right()  # Check if player hits right of window

                if self.collision.barrier_collision(self.hero, self.active_world.obstacles):
                    # For debugging purposes
                    print("player hit barrier right")
                    self.hero.x -= 10

                self.hero.adjust_movement()

        # If there is an npc in the world
        if self.active_world.npc:
            if self.collision.npc_collision(self.hero, self.active_world.npc):
                # Show exclamation mark
                self.show_interaction = True
            else:
                self.show_interaction = False

        if self.collision.entry_collision(self.hero, self.active_world.entries):
            print(self.collision.get_collided_entry())

            self.active_world = self.active_world.entry_dests[self.collision.get_collided_entry()]
            # Store the current map name in the game state
            self.game_state.game_state_current_map = self.active_world.map_name
            self.background = pygame.transform.scale(self.active_world.background, (960, 540))

            # Check current Map and which entry point was collided
            if self.active_world == self.ashlands:
                # Set size for npc and where it will face
                if self.active_world.npc:
                    self.active_world.npc.scale_sprite(75, 75)
                    self.active_world.npc.flip_sprite(False, False)

                if self.collision.get_collided_entry() == 0:  # From hub
                    # print("You are in the ashlands")
                    print("You are in the", self.game_state.game_state_current_map)
                    self.active_world.hero_spawn = [10, 260]

            elif self.active_world == self.hub_world:

                if self.collision.get_collided_entry() == 0:  # From ashland
                    # print("You are in the hub")
                    print("You are in the", self.game_state.game_state_current_map)
                    self.active_world.hero_spawn = [875, 260]
                elif self.collision.get_collided_entry() == 1:  # From dark dimension
                    print("You are in the", self.game_state.game_state_current_map)
                    # print("You are in the hub")
                    self.active_world.hero_spawn = [350, 20]

            elif self.active_world == self.dark_dimension:
                if self.active_world.npc:
                    self.active_world.npc.scale_sprite(75, 75)
                    self.active_world.npc.flip_sprite(True, False)

                if self.collision.get_collided_entry() == 0:  # From boss den
                    print("You are in the", self.game_state.game_state_current_map)
                    # print("You are in the dark dimension")
                    self.active_world.hero_spawn = [450, 250]
                if self.collision.get_collided_entry() == 1:  # From hub
                    print("You are in the", self.game_state.game_state_current_map)
                    # print("You are in the dark dimension")
                    self.active_world.hero_spawn = [450, 450]

            elif self.active_world == self.dark_dimension_boss:
                if self.active_world.npc:
                    self.active_world.npc.scale_sprite(75, 75)
                    self.active_world.npc.flip_sprite(True, False)

                if self.collision.get_collided_entry() == 0:  # From dark dimension
                    print("You are in the", self.game_state.game_state_current_map)
                    # print("You are in the dark dimension boss den")
                    self.active_world.hero_spawn = [450, 450]

            self.hero.x = self.active_world.hero_spawn[0]
            self.hero.y = self.active_world.hero_spawn[1]

        # TRACK INTERACTION
        if event.type == pygame.KEYDOWN:  # Press Enter or Esc to go back to the Main Menu
            if event.key == pygame.K_ESCAPE and not self.show_controls and not self.show_textbox \
                    and not self.show_inventory:
                self._quit_screen = True

            if event.key == pygame.K_q:  # Press q to open/close controls menu
                if self.show_controls:
                    original_background = self.active_world.background
                    self.background = pygame.transform.scale(original_background, (960, 540))
                    self.show_controls = False
                    self.show_characters = True
                    self.show_hud = True

                elif self._quit_screen:
                    self.quit_game(False)
                elif not self.show_controls and not self.show_textbox and not self.show_inventory:
                    self.background = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "Simple_Control_menu.png"))
                    self.show_controls = True
                    self.show_characters = False
                    self.show_interaction = False
                    self.show_hud = False

            # Press i to open/close inventory system
            if event.key == pygame.K_i and not self.show_controls and not self.show_textbox and not self._quit_screen:
                self.show_inventory = not self.show_inventory

            if self.show_inventory:  # If the inventory is being displayed on screen

                # Check in which section the user is at the moment
                if self.party_section:
                    self.inventory.character_selection(0, 3)  # Movement boundaries for tile in current party section
                else:
                    self.inventory.character_selection(1, 9)  # Movement boundaries for tile in current heroes section

                # If the user selects a hero in the current party section
                if event.key == pygame.K_SPACE and self.party_section and self.inventory.heroes:

                    # If the tile is not empty and the heroes list has heroes available it will swap them
                    if self.inventory.party_displayed[self.inventory.tile_pos[0]]:
                        self.party_index = self.inventory.tile_pos[0]
                        self.party_section = False
                        self.inventory.swapping = True

                    # If tile is empty is will add a hero from the heroes section to current party
                    elif not self.inventory.party_displayed[self.inventory.tile_pos[0]]:
                        self.inventory.swapping = False
                        self.party_section = False

                # Select hero to swap/add/remove from heroes section
                elif event.key == pygame.K_SPACE and not self.party_section:
                    if self.inventory.heroes_displayed[self.inventory.tile_pos[1]]:
                        self.hero_index = self.inventory.tile_pos[1]
                        self.party_section = True

                        if self.inventory.swapping:  # Swap hero between the 2 sections
                            temp_party = self.inventory.swap_characters(self.hero_index)
                            self.inventory.party[self.inventory.tile_pos[0]] = temp_party

                        else:  # Add hero to current party from heroes section
                            self.inventory.party, self.inventory.heroes = self.inventory.add_to_party(
                                self.inventory.heroes[self.hero_index])

            else:  # Restart selection tile to original position
                self.inventory.tile_x = [332, 317]
                self.inventory.tile_y = [187, 298]
                self.inventory.tile_pos = [0, 0]
                self.party_section = True

            # Checks if the space bar is pressed
            if event.key == pygame.K_SPACE and not self.show_controls and not self.show_inventory \
                    and not self._quit_screen and not self.show_textbox:
                # Check for collision
                if self.collision.check_collisions(self.hero, self.active_world.npc):
                    # if text box is displayed, stop characters movements
                    self.show_textbox = True

            # Select options from the text box
            if self.show_textbox:
                if self.active_world.npc.is_choice:
                    if event.key == pygame.K_1:
                        self.update_game_state()
                        self.switch_to_scene(combscene.CombatScene(self.screen, self.game_state, "combat_001"))
                    if event.key == pygame.K_2:
                        self.show_textbox = False
                else:
                    if event.key == pygame.K_SPACE and self.text_index < len(self.active_world.npc.dialogue):
                        self.text_index += 1

            if self._quit_screen:
                if event.key == pygame.K_b:
                    self._quit_screen = False
                if event.key == pygame.K_s:
                    self.quit_game(True)

    def render(self):
        self.screen.fill(Colors.WHITE.value)
        self.screen.blit(self.background, (0, 0))
        self.hero.play_animation()

        if self.show_hud:
            self.screen.blit(self.control_hud, (733, 0))

            # Show level hud
            self.textbox.load_image(27, 3, 0, 0, "UI/generic-rpg-ui-text-box.png")
            self.textbox.draw_level("Level:", self.level, 28, 34, -6)

        # Display hero and npcs
        if self.show_characters:
            self.screen.blit(self.hero.sprite, (self.hero.x, self.hero.y))
            # If there is an npc on the map
            if self.active_world.npc:
                self.screen.blit(self.active_world.npc.sprite, (self.active_world.npc.x, self.active_world.npc.y))

        # Show if player can interact with npc displaying an exclamation mark
        if self.show_interaction and not self.show_controls:
            # self.textbox.load_image(900, 170, 100, 100, "exclamation.png")
            self.textbox.load_image(self.active_world.npc.x + 15, self.active_world.npc.y - 100, 100, 100,
                                    "exclamation.png")
        # self.screen.blit(self.exclamation_mark.sprite, (self.exclamation_mark.x, self.exclamation_mark.y))

        if self._quit_screen:
            self.textbox.load_image(400, 150, 400, 150, "UI/generic-rpg-ui-text-box.png")
            options = ["[S]    Save and Quit", "[Q]    Quit", "[B]    Cancel"]
            size = 24
            x, y = 320, 200
            self.textbox.draw_options("Are you sure you want to quit?", options, size, x, y)

        # Draw Text box
        if self.show_textbox:
            # load_textbox(x, y, x_scale, y_scale)
            self.textbox.load_image(300, 370, 600, 100, "UI/generic-rpg-ui-text-box.png")

            # draw_options(question, options, size, x, y)

            # If the npc need the player to take a choice
            if self.active_world.npc.is_choice:
                question = self.active_world.npc.dialogue[0]
                options = self.active_world.npc.dialogue[1:]

                # Text box were the user must pick and option
                self.textbox.draw_options(question, options, 24, 200, 397)

                # If the npc is just displaying some text
            else:
                if self.text_index < len(self.active_world.npc.dialogue):
                    text = self.active_world.npc.dialogue[self.text_index]
                    self.textbox.draw_dialogue(text, 24, 200, 397)
                else:
                    self.text_index = -1
                    self.show_textbox = False

        # Display inventory box
        if self.show_inventory:
            self.inventory.display_inventory()
            if self.party_section:
                self.inventory.display_selection(0)
            else:
                self.inventory.display_selection(1)

            # Display character sprites in the inventory menu
            self.inventory.display_heroes(self.inventory.party, self.inventory.heroes)

    def update(self):
        pass

    """NOTE: To switch to another scene like main menu or combat scene you enter the following
        to combat: self.switch_to_scene(CombatScene(self.screen))
        to main menu: self.switch_to_scene(MainMenuScene(self.screen))

    """

    def update_game_state(self):
        self.game_state.game_state_location_x = self.hero.x
        self.game_state.game_state_location_y = self.hero.y

        self.game_state.player_party.clear()
        self.game_state.enemy_party.clear()

        for i in range(len(self.hero.party)):
            self.game_state.player_party.append(self.hero.party[i][0])

        for i in range(len(self.active_world.npc.party)):
            self.game_state.enemy_party.append(self.active_world.npc.party[i][0])

        print("My party: ", self.game_state.player_party)
        print("Enemy Party: ", self.game_state.enemy_party)

    def quit_game(self, saving):
        # saves game progress to database and stops music

        if saving:
            self.update_game_state()
            save_game(self.game_state)

        Music.stop_song()
        self.switch_to_scene(menuscene.MainMenuScene(self.screen, self.game_state))

    def load_active_world(self):
        map_name = self.game_state.game_state_current_map

        if map_name == "hub_world":
            return self.hub_world
        elif map_name == "atlantis":
            return self.atlantis_world
        elif map_name == "ashlands":
            return self.ashlands
        elif map_name == "dark_dimension":
            return self.dark_dimension
        elif map_name == "dark_dimension_boss":
            return self.dark_dimension_boss
