# import the pygame module, so you can use it
import pygame
import os


def run():
    # this is required to set display for xserver and wsl
    os.environ['DISPLAY'] = ': 0.0'

    # initialize the pygame module
    pygame.init()

    pygame.display.set_caption("minimal program")

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((400, 400))

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
