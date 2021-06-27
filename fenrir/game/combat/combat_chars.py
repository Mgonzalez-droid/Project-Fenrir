import os
import pygame
from fenrir.common.config import PATH_TO_RESOURCES, Colors
from fenrir.game.combat.combat_character_data import CombatCharacterData

""" Base class for combat char, functions will be implemented in sub class
"""


class CombatCharSprite(CombatCharacterData, pygame.sprite.Sprite):

    def __init__(self, char_id, char_type, level, hp, speed, attack, enemy):
        # attrs used for sprite and animation
        super().__init__(char_id, char_type, level, hp, speed, attack, enemy)
        pygame.sprite.Sprite.__init__(self)
        self._animation_state = "idle"  # default state of all chars
        self._move_x = 0  # amount char sprite needs to move on x-axis
        self._move_y = 0  # value char sprite needs to move on y-axis
        self._frame = 0  # value used for changing images in frames
        self._animation_speed = 3  # number of frames to show image
        self._face_left = False
        self._animating = False

    @property
    def animation_state(self):
        return self._animation_state

    @animation_state.setter
    def animation_state(self, value):
        self._animation_state = value

    @property
    def move_x(self):
        return self._move_x

    @move_x.setter
    def move_x(self, val):
        self._move_x = val

    @property
    def move_y(self):
        return self._move_y

    @move_y.setter
    def move_y(self, val):
        self._move_y = val

    def is_animating(self):
        return self._animating

    ###############################################
    # Abstract functions that must be implemented #
    ###############################################
    def update(self):
        raise NotImplementedError

    def animate(self, images):
        raise NotImplementedError

    def load_assets(self):
        raise NotImplementedError

    ###############################################
    #      Helper functions for char classes      #
    ###############################################
    def stop_movement(self):
        self.move_x = 0
        self.move_y = 0

    # function to move to a specified location on screen
    def move_to(self, x_target, y_target):
        delta_x = x_target - self.rect.centerx
        delta_y = y_target - self.rect.centery
        self.move(delta_x, delta_y)

    # function sets the movement amount and the subclass defines how it is animated
    def move(self, x, y):
        self.move_x = x
        self.move_y = y
        self._animating = True

    # return x,y tile location for combat map
    def get_tile_loc(self):
        x = int((self.xpos - 30) / 60)
        y = int((self.ypos - 30) / 60)
        return x, y


class MageChar(CombatCharSprite):

    def __init__(self, char_id, level, enemy):
        super().__init__(char_id, "mage", level, 50, 10, 40, enemy)

        # animation images
        self.attack_images = []
        self.idle_images = []
        self.run_images = []
        self.death_images = []
        self.damage_images = []

        self.load_assets()
        self.image = self.idle_images[0]
        self.rect = self.image.get_rect()

        self.teleporting = False
        self.attacking = False

        if enemy:
            self._face_left = True

        # default values that will need to be formulated with map tile data depending on tile location
        self.rect.center = (90, 90)

    def load_assets(self):
        # load idle images
        for i in range(1, 7):
            img = pygame.image.load(
                os.path.join(PATH_TO_RESOURCES, 'chars', 'mage', "idle (" + str(i) + ").png")).convert_alpha()
            img.set_colorkey(Colors.ALPHA.value)
            self.idle_images.append(img)

        # load attack images
        for i in range(1, 11):
            img = pygame.image.load(
                os.path.join(PATH_TO_RESOURCES, 'chars', 'mage', 'attack (' + str(i) + ').png')).convert_alpha()
            img.set_colorkey(Colors.ALPHA.value)
            self.attack_images.append(img)

        # load death images
        for i in range(1, 18):
            img = pygame.image.load(
                os.path.join(PATH_TO_RESOURCES, 'chars', 'mage', 'death (' + str(i) + ').png')).convert_alpha()
            img.set_colorkey(Colors.ALPHA.value)
            self.death_images.append(img)

        # load damage images
        for i in range(1, 6):
            img = pygame.image.load(
                os.path.join(PATH_TO_RESOURCES, 'chars', 'mage', 'damage (' + str(i) + ').png')).convert_alpha()
            img.set_colorkey(Colors.ALPHA.value)
            self.damage_images.append(img)

    def animate(self, images):

        if self._frame > (len(images) - 1) * self._animation_speed:  # num of animations in idle
            self._frame = 0  # reset to first frame
        else:
            self._frame += 1

        if self._face_left:
            self.image = pygame.transform.flip(images[self._frame // self._animation_speed], True, False)
        else:
            self.image = images[self._frame // self._animation_speed]

    def animate_teleport(self):
        if self._frame < len(self.death_images):
            self.animate(self.death_images)
            self._frame += 1
        else:
            self.rect.centerx += self.move_x
            self.rect.centery += self.move_y
            self.stop_movement()
            self.animation_state = "idle"
            self.teleporting = False
            self._animating = False

    def attack_enemy(self, left=None):

        if left is not None:
            self._face_left = left

        self._animating = True
        self.attacking = True
        self._frame = 0

    def animate_attack(self):
        if self._frame < (len(self.attack_images) - 1) * self._animation_speed:
            self.animate(self.attack_images)
        else:
            self.animation_state = "idle"
            self.attacking = False
            self._animating = False

    def update(self):
        if self.animation_state == "idle":
            images = self.idle_images
        elif self.animation_state == "attack":
            images = self.attack_images
        elif self.animation_state == "death":
            images = self.death_images
        elif self.animation_state == "damage":
            images = self.damage_images
        else:
            images = self.idle_images

        if self.move_x != 0 or self.move_y != 0:
            self.teleporting = True
            self._animating = True

            if self.move_x < 0:
                self._face_left = True
            elif self.move_x > 0:
                self._face_left = False

        if self.teleporting:
            self.animate_teleport()
        elif self.attacking:
            self.animate_attack()
        else:
            self.animate(images)


class KnightChar(CombatCharSprite):

    def __init__(self, char_id, level, enemy):
        super().__init__(char_id, "knight", level, 100, 2, 100, enemy)

        # animation images
        self.attack_images = []
        self.idle_images = []
        self.walk_images = []
        self.death_images = []
        self.attacking = False

        self.load_assets()
        self.image = self.idle_images[0]

        self.rect = self.image.get_rect()
        self.animation_state = "idle"

        if enemy:
            self._face_left = True

        # default values that will need to be formulated with map tile data depending on tile location
        self.rect.center = (90, 90)

    def load_assets(self):
        # load idle images
        for i in range(1, 12):
            img = pygame.image.load(
                os.path.join(PATH_TO_RESOURCES, 'chars', 'knight', "idle (" + str(i) + ").png")).convert_alpha()
            img.set_colorkey(Colors.ALPHA.value)
            self.idle_images.append(img)

        # load run images
        for i in range(1, 11):
            img = pygame.image.load(
                os.path.join(PATH_TO_RESOURCES, 'chars', 'knight', "walk (" + str(i) + ").png")).convert_alpha()
            img.set_colorkey(Colors.ALPHA.value)
            self.walk_images.append(img)

        # load attack images
        for i in range(1, 11):
            img = pygame.image.load(
                os.path.join(PATH_TO_RESOURCES, 'chars', 'knight', 'attack (' + str(i) + ').png')).convert_alpha()
            img.set_colorkey(Colors.ALPHA.value)
            self.attack_images.append(img)

        # load death images
        for i in range(1, 10):
            img = pygame.image.load(
                os.path.join(PATH_TO_RESOURCES, 'chars', 'knight', 'death (' + str(i) + ').png')).convert_alpha()
            img.set_colorkey(Colors.ALPHA.value)
            self.death_images.append(img)

    def animate(self, images):

        if self._frame > (len(images) - 1) * self._animation_speed:  # num of animations in idle
            self._frame = 0  # reset to first frame
        else:
            self._frame += 1

        if not self._face_left:
            self.image = pygame.transform.flip(images[self._frame // self._animation_speed], True, False)
        else:
            self.image = images[self._frame // self._animation_speed]

    def attack_enemy(self, left=None):

        if left is not None:
            self._face_left = left

        self.attacking = True
        self._animating = True
        # move rect to fix image shift in attack mode
        self.rect.centerx -= 5
        self.rect.centery -= 10
        self._frame = 0

    def animate_attack(self):
        if self._frame < (len(self.attack_images) - 1) * self._animation_speed:
            self.animate(self.attack_images)
        else:
            self.animation_state = "idle"
            self.rect.centerx += 5
            self.rect.centery += 10
            self.attacking = False
            self._animating = False

    # animates sprite while moving, returns to idle animation when complete
    def move_sprite(self):

        if self.move_x != 0 or self.move_y != 0:
            self.animation_state = "walk"
        else:
            self.animation_state = "idle"
            if not self.attacking:
                self._animating = False

        if self.move_x > 0:
            self._face_left = False
            if self.move_x < 2:
                self.rect += self.move_x
                self.move_x = 2
            else:
                self.rect.x += 2
                self.move_x -= 2
        elif self.move_x < 0:
            self._face_left = True
            if self.move_x > -2:
                self.rect += self.move_x
                self.move_x = 0
            else:
                self.rect.x += -2
                self.move_x -= -2

        # y axis movements will only start when x-movements are done
        if self.move_y > 0 and self.move_x == 0:
            if self.move_y < 2:
                self.rect += self.move_x
                self.move_y = 0
            else:
                self.rect.y += 2
                self.move_y -= 2
        elif self.move_y < 0 and self.move_x == 0:
            if self.move_y > -2:
                self.rect += self.move_y
                self.move_y = 0
            else:
                self.rect.y += -2
                self.move_y -= -2

    def update(self):
        if self.animation_state == "idle":
            images = self.idle_images
        elif self.animation_state == "walk":
            images = self.walk_images
        elif self.animation_state == "attack":
            images = self.attack_images
        elif self.animation_state == "death":
            images = self.death_images
        else:
            images = self.idle_images  # idle images as default

        self.move_sprite()

        if self.attacking:
            self.animate_attack()
        else:
            self.animate(images)
