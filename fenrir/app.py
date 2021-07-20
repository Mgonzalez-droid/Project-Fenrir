# import the pygame module, so you can use it
import os

import pygame
from fenrir.common.config import *
from fenrir.game.menu.menu_scene import MainMenuScene
from fenrir.common.global_game_state import GameState
from fenrir.data.db_connection import initialize_db


def run():
    # this will initialize the database if not done
    initialize_db()

    # initialize the pygame module
    pygame.init()

    screen = pygame.display.set_mode(DisplaySettings.SCREEN_RESOLUTION.value, pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    pygame.display.set_caption(GAME_TITLE)

    current_scene = MainMenuScene(screen, GameState())

    # main loop
    while current_scene is not None:

        # event handling
        for event in pygame.event.get():

            #  if the event is of type QUIT terminate game
            if event.type == pygame.QUIT:
                current_scene.terminate()
            else:
                current_scene.handle_event(event)

        current_scene.update()
        current_scene.render()

        current_scene = current_scene.next

        pygame.display.flip()
        clock.tick(DisplaySettings.FPS.value)
