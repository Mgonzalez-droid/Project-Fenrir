"""Overworld module. Add class properties and args to constructor to change this to diff levels or starting points, etc

"""
import os
import pygame
import fenrir.game.menu.menu_scene as menuscene
import fenrir.game.combat.combat_scene as combscene
from fenrir.common.scene import Scene
from fenrir.common.config import Colors, PATH_TO_RESOURCES
from fenrir.common.TextBox import TextBox
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
            # character(npc name, x, y, png name, level, party members[], can you interact with npc? (boolean 1),
            # is just text or a choice for the player? (boolean 2), dialogue[])
            npc=[character("Sensei", 220, 320, os.path.join(PATH_TO_RESOURCES, "chars", "sensei", "sensei.png"), 1,
                           [], False, False,
                           [
                               "Gabe, I if you want to defeat the evil lord for tak-ing over the world you will need to become stronger. In order to do that you need to learn how to fight.",
                               "You'll be giving commands to your party once com-   bat begins. Once it's their turn, choose a command  using the corresponding number."
                               ,
                               "Then, if you want them to act you'll have to tell   them which tile to attack or move to.",
                               "You can test your skill by challenging my apprenti- ces! I sent them all around the world to aid you in your journey. Good luck."]),

                 character("apprentice", 20, 255, os.path.join(PATH_TO_RESOURCES, "chars", "hat-guy", "hat-guy.png"), 1,
                           [["knight", "chars/knight/knight_menu.png"], ["mage", "chars/mage/mage_menu.png"],
                            ["archer", "chars/archer/archer_menu.png"], ["knight", "chars/knight/knight_menu.png"]],
                           False, True,
                           ["Try to defeat me if you can boy!",
                            "[1] I am ready!", "[2] J-Just wait a second! I am not ready"]),
                 character("Mani", 640, 380, os.path.join(PATH_TO_RESOURCES, "chars", "mani", "mani.png"), 1,
                           [], False, False,
                           [
                               "Hello Gabe, I will teach all you need to know about  this world. Press the [Spacebar] if you want me to go on",
                               "You can move by pressing the [WASD] keys, but you   probably already know that as you had to walk to ta-lk to me"
                               ,
                               "Pressing [i] will open the inventory. That is where you will be able to view and manage your party.",
                               "Your party and your ability to guide them will be   your strongest weapon in the coming trials.",
                               "If you want review the controls again you can either press [q] or talk to me again.",
                               "Okay! Now that I finish explaining things you should talk to sensei to learn about combat"]),

                 ],
            hero_spawn=(self.game_state.game_state_location_x, self.game_state.game_state_location_y),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "overworld_maps", "hub_world.png")),
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
                obstacle(860, 160, 1, 1)  # Top tombstone (looks broken)
            ],
            entries=[
                obstacle(1, 240, 1, 100),  # Hub Entry
                obstacle(490, 0, 120, 1),  # atlantis
            ],
            entry_dests=[],
            npc=[character("Twin Apprentice", 350, 430,
                           os.path.join(PATH_TO_RESOURCES, "chars", "hat-guy", "hat-guy.png"), 2,
                           [], False, False,
                           ["Oh Gabe! Good to see you here!",
                            "You can train with my twin brother over there if    you feel like it. "
                            "I am not much of a fighter myself.",
                            "I came here because I heard rumors of a mystical    creature living inside the ruins",
                            "If the rumors are true and something is there, I    am confident it will help you train to defeat the   demon lord.",
                            "I think it is worth giving it a try"]),

                 character("Apprentice", 850, 240,
                           os.path.join(PATH_TO_RESOURCES, "chars", "hat-guy", "hat-guy-left.png"), 2,
                           [["knight", "chars/knight/knight_menu.png"], ["mage", "chars/mage/mage_menu.png"],
                            ["archer", "chars/archer/archer_menu.png"], ["archer", "chars/archer/archer_menu.png"]],
                           False, True,
                           ["Gabe! Lets train for a bit, I am bored of been here doing nothing", "",
                            "[1] Lets do it!      [2] Sorry, I don't feel like it"])
                 ],
            hero_spawn=(self.game_state.game_state_location_x, self.game_state.game_state_location_y),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "overworld_maps", "ashlands.png")),
            music="Windless Slopes"
        )

        self.atlantis_world = world_obj(
            map_name="atlantis",
            obstacles=[
                obstacle(0, 0, 165, 170),  # Left_Column_Barrier
                obstacle(189, 0, 60, 60),  # left_Column_Rocks
                obstacle(350, 0, 20, 60),  # Left_Entry
                obstacle(560, 0, 50, 60),  # Right_Entry
                obstacle(860, 0, 110, 120),  # right_column
                obstacle(730, 0, 70, 20),  # right_column_pebbles
                obstacle(390, 191, 10, 90),  # left_barricade
                obstacle(401, 191, 120, 100),  # top_barricade
                obstacle(550, 191, 10, 90),  # right_barricade
                obstacle(766, 298, 87, 60),  # anchor_barrier
                obstacle(0, 350, 60, 40),  # pot_barrier
                obstacle(0, 430, 100, 20),  # half_column_barrier (bottom right)
                obstacle(0, 460, 960, 80),  # sea_wall_barrier
                obstacle(860, 430, 100, 20),  # half_column_barrier (bottom left)
            ],
            entries=[
                obstacle(430, 0, 100, 1)  # ashlands
            ],
            entry_dests=[
                self.ashlands
            ],
            npc=[character("Mermaid", 439, 230, os.path.join(PATH_TO_RESOURCES, "chars", "mermaid", "mermaid.png"), 3,
                           [["knight", "chars/knight/knight_menu.png"], ["knight", "chars/knight/knight_menu.png"],
                            ["archer", "chars/archer/archer_menu.png"], ["archer", "chars/archer/archer_menu.png"]],
                           False, True,
                           [
                               "I have heard of your mission human boy. If you      beat me you will have enough power to defeat evil.",
                               "", "[1] I will do my best!      [2] I am not ready yet"])
                 ],
            hero_spawn=(400, 25),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "overworld_maps", "atlantis.png")),
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
            npc="",
            hero_spawn=(self.game_state.game_state_location_x, self.game_state.game_state_location_y),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "overworld_maps", "dark_dimension.png")),
            music="Windless Slopes"
        )

        self.dark_dimension_boss = world_obj(
            map_name="dark_dimension_boss",
            obstacles=[
                obstacle(320, 0, 320, 285),  # Boss_den_top_barrier
                obstacle(0, 0, 330, 540),  # Boss_den_left_barrier
                obstacle(620, 0, 380, 540),  # Boss_den_right_barrier
            ],
            entries=[
                obstacle(410, 539, 130, 1)  # Dark dimension
            ],
            entry_dests=[self.dark_dimension
                         ],
            npc=[
                character("Gargoyle", 377, 100, os.path.join(PATH_TO_RESOURCES, "chars", "gargoyle", "gargoyle.png"), 5,
                          [["knight", "chars/knight/knight_menu.png"], ["archer", "chars/archer/archer_menu.png"],
                           ["mage", "chars/mage/mage_menu.png"], ["mage", "chars/mage/mage_menu.png"]], False, True,
                          ["Another fool who thinks that I can be defeated so   easily. "
                           "Come at me with all your power you human!",
                           "",
                           "       [1] (Fight)                     [2] (Retreat)"])
            ],
            hero_spawn=(406, 400),
            background=pygame.image.load(os.path.join(PATH_TO_RESOURCES, "overworld_maps", "dark_dimension_boss.png")),
            music="Windless Slopes"
        )

        self.hub_world.entry_dests = [self.ashlands, self.dark_dimension]
        self.dark_dimension.entry_dests = [self.dark_dimension_boss, self.hub_world]
        self.ashlands.entry_dests = [self.hub_world, self.atlantis_world]

        # Defaults to hub world and hero default position
        self.active_world = self.load_active_world()
        self.active_world.hero_spawn = [self.game_state.game_state_location_x, self.game_state.game_state_location_y]

        self.background = pygame.transform.scale(self.active_world.background, (960, 540))
        self.control_hud = pygame.image.load(os.path.join(PATH_TO_RESOURCES, "controls_HUD.png"))
        self.textbox = TextBox(self.screen)
        self._quit_screen = False
        self.collision = Collision()

        # used for sound effects
        self.hero_walking = False
        self.walk_sound_effect = self.get_walk_sound_effect()
        self.walk_sound_effect_started = False

        # TODO: Need to add secondary list and behavior for entries...

        self.level = self.game_state.player_level
        self.hero = character_animated("Gabe", self.active_world.hero_spawn[0], self.active_world.hero_spawn[1],
                                       os.path.join(PATH_TO_RESOURCES, "gabe_best_resolution.png"),
                                       self.game_state.player_level, [],
                                       False, False, [])

        self.hero.sprite_names = ["gabe_stance_0.png", "gabe_stance_1.png", "gabe_stance_2.png", "gabe_stance_3.png",
                                  "gabe_stance_4.png", "gabe_stance_5.png", "gabe_stance_6.png"]

        self.hero.party = self.formatted_hero_party()
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(PATH_TO_RESOURCES, "soundtrack", self.active_world.music + ".wav"))
        pygame.mixer.music.set_volume(.4)
        pygame.mixer.music.play(-1)
        self._sound_effects = {}

        # Default npc scale and position
        if self.active_world.npc:
            for i in range(len(self.active_world.npc)):
                if self.active_world == self.dark_dimension_boss:
                    for t in range(len(self.active_world.npc)):
                        self.active_world.npc[t].sprite = pygame.transform.scale(self.active_world.npc[t].sprite,
                                                                                 (200, 200))
                else:
                    # Set default size for all npcs
                    self.active_world.npc[i].sprite = pygame.transform.scale(self.active_world.npc[i].sprite, (75, 75))

        self.show_controls = False
        self.show_characters = True
        self.show_hud = True
        self.show_textbox = False
        self.show_inventory = False

        # Inventory system
        self.inventory = Inventory(self.textbox, self.hero.party, self.game_state.all_heroes)
        self.party_section = True
        self.hero_index = 0

        # Index for displaying npc test
        self.text_index = -1
        # Index for selecting enemy npc player will fight
        self.enemy_index = 0

        self.hero_left = False
        self.boss_closed = True

    def handle_event(self, event):

        # Check for victory
        if self.game_state.final_victory == 1:
            self.show_textbox = True

        # TRACK MOVEMENT
        # Boundaries class prevent the player character to move outside the current window
        boundaries = Boundaries(self.screen, self.hero)

        # Player check player movement for up (w), down (s), left (a), right (d)
        keys = pygame.key.get_pressed()

        if not self.show_controls and not self.show_textbox and not self.show_inventory \
                and not self._quit_screen and event.type != pygame.MOUSEMOTION:
            if keys[pygame.K_w]:
                self.hero.y = boundaries.collision_up()  # Check if player hits top of window
                self.hero_walking = True

                if self.collision.barrier_collision(self.hero, self.active_world.obstacles):
                    self.hero.y += 10

                self.hero.adjust_movement(self.hero_left)
            if keys[pygame.K_s]:
                self.hero_walking = True
                self.hero.y = boundaries.collision_down()  # Check if player hits bottom of window

                if self.collision.barrier_collision(self.hero, self.active_world.obstacles):
                    self.hero.y -= 10

                self.hero.adjust_movement(self.hero_left)
            if keys[pygame.K_a]:
                self.hero_left = True
                self.hero_walking = True
                self.hero.x = boundaries.collision_left()  # Check if player hits left of window

                if self.collision.barrier_collision(self.hero, self.active_world.obstacles):
                    self.hero.x += 10

                self.hero.adjust_movement(self.hero_left)
            if keys[pygame.K_d]:
                self.hero_left = False
                self.hero_walking = True
                self.hero.x = boundaries.collision_right()  # Check if player hits right of window

                if self.collision.barrier_collision(self.hero, self.active_world.obstacles):
                    self.hero.x -= 10

                self.hero.adjust_movement(self.hero_left)

            # if these are all
            if not (keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s]):
                self.hero_walking = False

        # If there is an npc in the world
        if self.active_world.npc:
            for i in range(len(self.active_world.npc)):
                if self.collision.npc_collision(self.hero, self.active_world.npc[i]):
                    # Show exclamation mark
                    self.active_world.npc[i].show_interaction = True
                    # self.show_interaction = True
                else:
                    self.active_world.npc[i].show_interaction = False
                    # self.show_interaction = False

        if self.collision.entry_collision(self.hero, self.active_world.entries):

            prev = self.active_world
            self.active_world = self.active_world.entry_dests[self.collision.get_collided_entry()]

            if self.active_world == self.dark_dimension_boss and self.hero.level < 4:
                self.active_world = prev
                self.show_textbox = True
            elif self.active_world == self.dark_dimension_boss and self.hero.level >= 4:
                self.boss_closed = False

            # Store the current map name in the game state
            self.game_state.game_state_current_map = self.active_world.map_name
            # Update background
            self.background = pygame.transform.scale(self.active_world.background, (960, 540))

            # Set size for npc and where it will face
            if self.active_world.npc:
                if self.active_world == self.dark_dimension_boss:
                    for i in range(len(self.active_world.npc)):
                        if self.active_world == self.dark_dimension_boss:
                            for t in range(len(self.active_world.npc)):
                                self.active_world.npc[t].sprite = pygame.transform.scale(
                                    self.active_world.npc[t].sprite, (200, 200))
                else:
                    for i in range(len(self.active_world.npc)):
                        self.active_world.npc[i].sprite = pygame.transform.scale(self.active_world.npc[i].sprite,
                                                                                 (75, 75))

            # Check current Map and which entry point was collided
            if self.active_world == self.ashlands:
                if self.collision.get_collided_entry() == 0 and prev == self.hub_world:  # From hub
                    self.active_world.hero_spawn = [10, 260]

                elif self.collision.get_collided_entry() == 0 and prev == self.atlantis_world:  # From atlantis
                    self.active_world.hero_spawn = [500, 100]

            elif self.active_world == self.hub_world:
                if self.collision.get_collided_entry() == 0:  # From ashland
                    self.active_world.hero_spawn = [875, 260]

                elif self.collision.get_collided_entry() == 1:  # From dark dimension
                    self.active_world.hero_spawn = [350, 20]

            elif self.active_world == self.dark_dimension:
                if self.collision.get_collided_entry() == 0:  # From boss den
                    self.active_world.hero_spawn = [450, 250]

                if self.collision.get_collided_entry() == 1:  # From hub
                    self.active_world.hero_spawn = [450, 450]

            elif self.active_world == self.dark_dimension_boss:
                if self.collision.get_collided_entry() == 0:  # From dark dimension
                    self.active_world.hero_spawn = [450, 450]

            elif self.active_world == self.atlantis_world:
                if self.collision.get_collided_entry() == 1:  # From ashlands
                    self.active_world.hero_spawn = [450, 30]

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
                    for i in range(len(self.active_world.npc)):
                        self.active_world.npc[i].show_interaction = False
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

                for i in range(len(self.active_world.npc)):
                    # Check for collision
                    if self.collision.check_collisions(self.hero, self.active_world.npc[i]):
                        # if text box is displayed, stop characters movements
                        self.show_textbox = True

            # Select options from the text box
            if self.show_textbox:
                # If game was won
                if self.boss_closed and self.active_world == self.dark_dimension:
                    if event.key == pygame.K_SPACE:
                        self.show_textbox = False

                elif self.game_state.final_victory == 1:
                    if event.key == pygame.K_SPACE:
                        self.show_textbox = False
                        self.game_state.final_victory = 0
                else:
                    for i in range(len(self.active_world.npc)):
                        if self.active_world.npc[i].show_interaction:
                            if self.active_world.npc[i].is_choice:
                                if event.key == pygame.K_1:
                                    self.enemy_index = i
                                    self.update_game_state()
                                    self.switch_to_scene(combscene.CombatScene(self.screen, self.game_state))
                                if event.key == pygame.K_2:
                                    self.show_textbox = False
                            else:
                                if event.key == pygame.K_SPACE and \
                                        self.text_index < len(self.active_world.npc[i].dialogue):
                                    self.text_index += 1

            if self._quit_screen:
                if event.key == pygame.K_b:
                    self._quit_screen = False
                if event.key == pygame.K_s:
                    self.quit_game(True)

    def render(self):
        self.screen.fill(Colors.WHITE.value)
        self.screen.blit(self.background, (0, 0))
        # self.hero.play_animation(self.hero_left)

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
                for i in range(len(self.active_world.npc)):
                    self.screen.blit(self.active_world.npc[i].sprite,
                                     (self.active_world.npc[i].x, self.active_world.npc[i].y))

            # Show if player can interact with npc displaying an exclamation mark

            # self.textbox.load_image(900, 170, 100, 100, "exclamation.png")
            for i in range(len(self.active_world.npc)):
                if self.active_world == self.dark_dimension_boss:
                    if self.active_world.npc[i].show_interaction and not self.show_controls:
                        self.textbox.load_image(self.active_world.npc[i].x + 90, self.active_world.npc[i].y - 40, 100,
                                                100,
                                                "exclamation.png")
                else:
                    if self.active_world.npc[i].show_interaction and not self.show_controls:
                        self.textbox.load_image(self.active_world.npc[i].x + 20, self.active_world.npc[i].y - 100, 100,
                                                100,
                                                "exclamation.png")

        if self._quit_screen:
            self.textbox.load_image(400, 150, 400, 150, "UI/generic-rpg-ui-text-box.png")
            options = ["[S]    Save and Quit", "[Q]    Quit", "[B]    Cancel"]
            size = 24
            x, y = 320, 200
            self.textbox.draw_options("Are you sure you want to quit?", options, size, x, y)

        # Draw Text box
        if self.show_textbox:

            # load_textbox(x, y, x_scale, y_scale)
            self.textbox.load_image(300, 370, 615, 100, "UI/generic-rpg-ui-text-box.png")

            if self.boss_closed and self.active_world == self.dark_dimension:
                self.textbox.draw_dialogue(
                    "You are not strong enough to even set a foot in     my domains. Come back with "
                    "at least level 4"
                    , 24, 200, 397)

            # If the game was won display victory message
            if self.game_state.final_victory == 1:
                self.textbox.draw_dialogue("Congratulations Gabe, you saved the world from       the forces of evil!"
                                           , 24, 200, 397)
            else:  # Display regular messages
                # If the npc need the player to take a choice
                for i in range(len(self.active_world.npc)):
                    if self.active_world.npc[i].show_interaction:
                        if self.active_world.npc[i].is_choice:
                            question = self.active_world.npc[i].dialogue[0]
                            options = self.active_world.npc[i].dialogue[1:]

                            # Text box were the user must pick and option
                            self.textbox.draw_options(question, options, 24, 200, 397)

                            # If the npc is just displaying some text
                        else:
                            if self.text_index < len(self.active_world.npc[i].dialogue):
                                text = self.active_world.npc[i].dialogue[self.text_index]
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
        if self.hero_walking and not self.walk_sound_effect_started:
            self.walk_sound_effect_started = True
            self.walk_sound_effect.play(-1)
        elif not self.hero_walking and self.walk_sound_effect_started:
            self.stop_walk_sound_effect()
        elif self.show_textbox or self.show_inventory or self.show_controls:
            self.stop_walk_sound_effect()

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

        if self.active_world.npc:
            # Save enemy name and level in game state
            self.game_state.enemy_name = self.active_world.npc[self.enemy_index].name
            self.game_state.enemy_level = self.active_world.npc[self.enemy_index].level
            # Save enemy party in game state
            for k in range(len(self.active_world.npc[self.enemy_index].party)):
                self.game_state.enemy_party.append(self.active_world.npc[self.enemy_index].party[k][0])

    def quit_game(self, saving):
        # saves game progress to database and stops music

        if saving:
            self.update_game_state()
            save_game(self.game_state)

        pygame.mixer.music.stop()
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

    def formatted_hero_party(self):
        party_list = []

        for unit in self.game_state.player_party:
            party_list.append([unit, f"chars/{unit}/{unit}_menu.png"])

        return party_list

    def get_walk_sound_effect(self):
        path = os.path.join(PATH_TO_RESOURCES, "soundtrack", "overworld_sounds", "walk" + ".wav")
        sound = pygame.mixer.Sound(path)
        sound.set_volume(.7)
        return sound

    def stop_walk_sound_effect(self):
        self.walk_sound_effect.stop()
        self.walk_sound_effect_started = False
        self.hero_walking = False
