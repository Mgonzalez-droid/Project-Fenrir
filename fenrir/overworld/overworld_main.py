import pygame
from pygame import mixer
import os

# this is required to set display for xserver and wsl
os.environ['DISPLAY'] = ': 0.0'

## Global Variables ##
pygame.init()
background = pygame.image.load("demo_overworld.png")
win = pygame.display.set_mode((960, 540))


## hero ##
xPos = 0
yPos = 0


def main():
    draw_overworld()

## Drawing Overworld ##
def draw_overworld():
    run = True
    while run:
        win.fill((0, 0, 0))

        for event in pygame.event.get():
            win.blit(background, (0, 0))

            if event.type == pygame.QUIT:
                run = False

            pygame.display.update()




if __name__ =='__main__':
    main()