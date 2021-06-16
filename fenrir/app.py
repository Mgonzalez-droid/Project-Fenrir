# import the pygame module, so you can use it
import pygame
from fenrir.common.wsl import *


def run(scene):
    # this is required to set display for xserver and wsl
    set_display_to_host()

    # initialize the pygame module
    pygame.init()
    resolution = (960, 540)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Project Fenrir")

    current_scene = scene

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
        current_scene.render(screen)

        current_scene = current_scene.next

        pygame.display.flip()

