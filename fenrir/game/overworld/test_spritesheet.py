import pygame
from Spritesheet import Spritesheet

################################# LOAD UP A BASIC WINDOW #################################
pygame.init()
DISPLAY_W, DISPLAY_H = 480, 270
canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)))
running = True
###########################################################################################

my_spritesheet = Spritesheet('gabe-idle-run 2.png')
# gabe1 = my_spritesheet.get_sprite(0,0,25,25) #get metadata, in video: (x : 0, y: 0, w: 128, h: 128)
gabe = [my_spritesheet.parse_sprite('gabe1.png'), my_spritesheet.parse_sprite('gabe2.png'),
        my_spritesheet.parse_sprite('gabe3.png'), my_spritesheet.parse_sprite('gabe4.png'),
        my_spritesheet.parse_sprite('gabe5.png'), my_spritesheet.parse_sprite('gabe6.png'),
        my_spritesheet.parse_sprite('gabe7.png')]  # makes a list of sprite images

index = 0

while running:
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ############### UPDATE SPRITE IF SPACE IS PRESSED #################################
            if event.key == pygame.K_SPACE:
                index = (index + 1) % len(gabe)

    ################################# UPDATE WINDOW AND DISPLAY #################################
    canvas.fill((255, 255, 255))
    canvas.blit(gabe[index], (0, DISPLAY_H - 128))
    window.blit(canvas, (0, 0))
    pygame.display.update()
