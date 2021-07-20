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

<<<<<<< HEAD:fenrir/game/overworld/overworld_scene.py
        # new world objs
        self.hub_world = world_obj(
            obstacles=[
                obstacle(0, 0, 324, 234),  # Flower_Patch_Barrier
                obstacle(461, 0, 89, 260),  # Left_House_Barrier
                obstacle(550, 0, 88, 165),  # Center_house_Barrier
                obstacle(637, 0, 323, 246),  # House_River_Bridge_Barrier
                obstacle(736, 367, 224, 121),  # bottom_river_Barrier
                obstacle(604, 477, 133, 62),  # Bottom_River_Left_Barrier
                obstacle(0, 401, 200, 139)  # Pond_Barrier
            ],
            entries=[
                obstacle(939, 260, 21, 97),  # World_1_Entry
                obstacle(327, 0, 116, 18),  # World_3_Entry
            ],
            entry_dests=[],
            npc=character(880, 255, os.path.join("fenrir/resources/chars/sensei/sensei.png")),  # FILL in with npc
            npc_spawn=(100, 100),  # Fill in with npc
            hero_spawn=(self.game_state.game_state_location_x, self.game_state.game_state_location_y),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "Overworld_Correct_size.png")),
            music="fenrir/resources/soundtrack/Windless Slopes.mp3"
        )

        self.aquatic_world = world_obj(
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
                obstacle(397, 0, 146, 20) # world_1_entry
            ],
            entry_dests=[
                self.hub_world
            ],
            npc=character(880, 255, os.path.join("fenrir/resources/chars/sensei/sensei.png")),  # defaults to sensei
            npc_spawn=(100, 100),
            hero_spawn=(400, 25),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "aquatic-world.png")),
            music="fenrir/resources/soundtrack/Windless Slopes.mp3"
        )

        """
        self.dark_desert_world = world_obj(
            obstacles=[],
            entries=[],
            npc="",  # defaults to sensei
            npc_spawn=(100, 100),
            hero_spawn=(100, 100),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "Overworld_Correct_size.png")),
            music="fenrir/resources/soundtrack/Windless Slopes.mp3"
        )
        """

        self.end_world = world_obj(
            obstacles=[
                obstacle(0, 0, 416, 542),  # Main_barrier_left
                obstacle(555, 0, 404, 540)  # Main_barrier_right
            ],
            entries=[
                obstacle(443, 254, 87, 18),  # hub_exit
                obstacle(415, 523, 140, 15)  # boss_den_entry
            ],
            entry_dests=[],
            npc="",  # defaults to sensei
            npc_spawn=(100, 100),
            hero_spawn=(470, 350),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "dark-world-demo.png")),
            music="fenrir/resources/soundtrack/Windless Slopes.mp3"
        )

        self.boss_den = world_obj(
            obstacles=[
                obstacle(0, 0, 960, 359),  # Boss_den_barrier_0
                obstacle(0, 358, 401, 180),  # Boss_den_barrier_1
                obstacle(545, 358, 412, 180),  # Boss_den_barrier_2
            ],
            entries=[
                obstacle(401, 540, 144, 20)  # World exit
            ],
            entry_dests=[
                self.end_world
            ],
            npc="",  # defaults to sensei
            npc_spawn=(100, 100),
            hero_spawn=(406, 400),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "boss-den.png")),
            music="fenrir/resources/soundtrack/Windless Slopes.mp3"
        )

        self.hub_world.entry_dests = [self.aquatic_world, self.end_world]
        self.end_world.entry_dests = [self.boss_den, self.hub_world]

        # Defaults to hub world
        self.active_world = self.hub_world


        self.background = pygame.transform.scale(self.active_world.background, (960, 540))
=======
        original_background = pygame.image.load(os.path.join(PATH_TO_RESOURCES,
                                                             "overworld_maps/Overworld_Correct_size.png"))

        self.background = pygame.transform.scale(original_background, (960, 540))
>>>>>>> 7b0891459f64268697f0bccbfd9c3d182715a8ab:fenrir/game/overworld/overworld_scene_hub.py
        self.control_hud = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "controls_HUD.png"))
        self.textbox = TextBox(self.screen)
        self._quit_screen = False
        self.collision = Collision()

<<<<<<< HEAD:fenrir/game/overworld/overworld_scene.py
=======
        '''
        # Dark Desert 
        # Boundaries:
        obstacle(0, 0, 280, 170),  # Top left prompts
        obstacle(281, 0, 180, 70),  # Top left stone wall
        obstacle(650, 0, 250, 70),  # Top right stone wall
        obstacle(0, 410, 75, 70),  # Bottom left prompts
        obstacle(200, 410, 70, 1),  # Bottom left prompts (fallen tree)
        obstacle(760, 410, 1, 1),  # Bottom tombstone
        obstacle(740, 280, 1, 1),  # Middle tombstone
        obstacle(860, 160, 1, 1),  # Top tombstone (looks broken)
        
        # Entry points:
        obstacle(0, 260, 21, 60),  # World_1_Entry
        obstacle(462, 0, 187, 20),  # Dark_Desert_Boss
        '''

        # Define in world barriers
        self.obstacles = [
            obstacle(0, 0, 300, 190),  # Flower_Patch_Barrier
            obstacle(461, 0, 80, 220),  # Left_House_Barrier
            obstacle(550, 0, 88, 165),  # Center_house_Barrier
            obstacle(637, 0, 323, 220),  # House_River_Bridge_Barrier
            obstacle(736, 367, 224, 121),  # bottom_river_Barrier
            obstacle(604, 477, 133, 62),  # Bottom_River_Left_Barrier
            obstacle(0, 401, 200, 139)  # Pond_Barrier
        ]

        # Define in world entries
        self.entries = [
            obstacle(939, 260, 21, 97),  # World_1_Entry (Dark desert)
            obstacle(327, 0, 116, 18),  # World_3_Entry
        ]

        # TODO: Need to add secondary list and behavior for entries...
>>>>>>> 7b0891459f64268697f0bccbfd9c3d182715a8ab:fenrir/game/overworld/overworld_scene_hub.py

        self.level = self.game_state.player_level
        self.hero = character_animated(self.active_world.hero_spawn[0], self.active_world.hero_spawn[1],
                                       os.path.join(PATH_TO_RESOURCES, "gabe_best_resolution.png"))
        self.hero.sprite_names = ["gabe_stance_0.png", "gabe_stance_1.png", "gabe_stance_2.png", "gabe_stance_3.png",
                                  "gabe_stance_4.png", "gabe_stance_5.png", "gabe_stance_6.png"]

        pygame.mixer.init()
<<<<<<< HEAD:fenrir/game/overworld/overworld_scene.py
        pygame.mixer.music.load(self.active_world.music)
        #pygame.mixer.music.stop()
=======
        pygame.mixer.music.load("fenrir/resources/soundtrack/Windless Slopes.wav")
>>>>>>> 7b0891459f64268697f0bccbfd9c3d182715a8ab:fenrir/game/overworld/overworld_scene_hub.py
        pygame.mixer.music.play()
        
        self.npc = self.active_world.npc
        self.npc.sprite = pygame.transform.flip(self.npc.sprite, True, False)
        self.npc.sprite = pygame.transform.scale(self.npc.sprite, (75, 75))
        self.exclamation_mark = character(860, 170, os.path.join(PATH_TO_RESOURCES, "exclamation.png"))
        self.exclamation_mark.sprite = pygame.transform.scale(self.exclamation_mark.sprite, (100, 100))
        self.show_controls = False
        self.show_characters = True
        self.show_interaction = False
        self.show_hud = True
        self.show_textbox = False
        self.show_inventory = False

        # Inventory system
        self.current_party = [[self.hero, "chars/gabe/Gabe.png"]]
        self.all_heroes = [[self.hero, "chars/gabe/Gabe.png"], [self.npc, "chars/sensei/Sensei_menu.png"],
                           [self.hero, "UI/Girl.png"]]

        self.inventory = Inventory(self.textbox, self.current_party, self.all_heroes)
        self.party_section = True
        self.party_index = 0
        self.hero_index = 0


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

        if self.collision.npc_collision(self.hero, self.npc):
            # Show exclamation mark
            self.show_interaction = True
        else:
            self.show_interaction = False

        if self.collision.entry_collision(self.hero, self.active_world.entries):
            print(self.collision.get_collided_entry())
            self.active_world = self.active_world.entry_dests[self.collision.get_collided_entry()]
            self.background = pygame.transform.scale(self.active_world.background, (960, 540))
            self.hero.x = self.active_world.hero_spawn[0]
            self.hero.y = self.active_world.hero_spawn[1]


        # TRACK INTERACTION
        if event.type == pygame.KEYDOWN:  # Press Enter or Esc to go back to the Main Menu
            if event.key == pygame.K_ESCAPE and not self.show_controls and not self.show_textbox \
                    and not self.show_inventory:
                self._quit_screen = True

            if event.key == pygame.K_q:  # Press q to open/close controls menu
                if self.show_controls:
                    original_background = pygame.image.load(
                        os.path.join(PATH_TO_RESOURCES, "overworld_maps/Overworld_Correct_size.png"))
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
                            temp_party = self.inventory.swap_characters(self.party_index, self.hero_index)
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
                    and not self._quit_screen:
                # Check for collision
                if self.collision.check_collisions(self.hero, self.npc):
                    # if text box is displayed, stop characters movements
                    self.show_textbox = True

            # Select options from the text box
            if event.key == pygame.K_1 and self.show_textbox:
                self.update_game_state()
                self.switch_to_scene(combscene.CombatScene(self.screen, self.game_state, "combat_001"))
            if event.key == pygame.K_2 and self.show_textbox:
                self.show_textbox = False

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
            self.screen.blit(self.npc.sprite, (self.npc.x, self.npc.y))

        # Show if player can interact with npc displaying an exclamation mark
        if self.show_interaction and not self.show_controls:
            self.screen.blit(self.exclamation_mark.sprite, (self.exclamation_mark.x, self.exclamation_mark.y))

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

            options = ["[1] Yes, I am ready to go to the combat phase",
                       "[2] No, I want to keep walking here"]

            # Text box were the user must pick and option
            self.textbox.draw_options("Hello Gabe, do you wanna go to the combat phase?", options, 24, 200, 397)

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

    def quit_game(self, saving):
        # saves game progress to database and stops music

        if saving:
            self.update_game_state()
            save_game(self.game_state)

        Music.stop_song()
        self.switch_to_scene(menuscene.MainMenuScene(self.screen, self.game_state))
