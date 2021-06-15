# import the pygame module, so you can use it
import pygame
from common import wsl as wsl


def run():
    # this is required to set display for xserver and wsl
    wsl.set_display_to_host()

    # initialize the pygame module
    pygame.init()

    pygame.display.set_caption("minimal program")

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((960, 540))

    # define a variable to control the main loop
    running = True

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
