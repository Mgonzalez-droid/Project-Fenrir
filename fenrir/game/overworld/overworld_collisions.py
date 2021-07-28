import pygame
from fenrir.game.overworld.overworld_hero_animated import overworld_hero_animated as spc_hero

class Collision:
    def __init__(self):
        self.__tolerance = 50
        # self.__tolerance = 35
        self.entry_index = 0
        self.repulsion = 0
        self.__hit_wall = ""

    @staticmethod
    def make_character_rect(npc):
        character = pygame.Rect(npc.x, npc.y, npc.sprite.get_width(), npc.sprite.get_height())
        return character

    @staticmethod
    def make_obstacle_rect(obstacle):
        obstacle = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
        return obstacle

    def npc_collision(self, hero, npc):
       # print("CHECKING IF PLAYER HIT NPC")
        '''
        if isinstance(hero, spc_hero):
            hero_rect = hero.rect
        else:
            hero_rect = self.make_character_rect(hero)
        '''
        hero_rect = self.make_character_rect(hero)
        #print("hero_rect: x: ", hero_rect.x, " y: ", hero_rect.y, " width: ", hero_rect.width, " height: ",
              #hero_rect.height)
        npc_rect = self.make_character_rect(npc)

        self.repulsion = 0

        if self.check_collision(hero_rect, npc_rect):
            #print("\n\n\nPLAYER * HIT * NPC")
            return True
        else:
            #print("\n\n\nPLAYER * DID NOT * HIT NPC")
            return False

    def barrier_collision(self, hero, obstacle):
        #
        #print("CHECKING IF PLAYER HIT OBSTACLE")
        hero_rect = self.make_character_rect(hero)
        #print("hero_rect: x: ", hero_rect.x, " y: ", hero_rect.y, " width: ", hero_rect.width, " height: ",
              #hero_rect.height)
        obstacle_rect = self.make_obstacle_rect(obstacle)
        if self.check_collision(hero_rect, obstacle_rect):
            print("\n\n\nPLAYER * HIT * OBSTACLE")
            return True
        else:
            #print("\n\n\nPLAYER * DID NOT * HIT OBSTACLE")
            return False

    '''
    def barrier_collision(self, hero, obstacles):
        ###############
        if isinstance(hero, spc_hero):
            hero_rect = hero.rect
        else:
            hero_rect = self.make_character_rect(hero)
        ###############
        hero_rect = self.make_character_rect(hero)
        print("hero_rect: x: ", hero_rect.x, " y: ", hero_rect.y, " width: ", hero_rect.width, " height: ",
              hero_rect.height)
        obstacle_rects = list()
        #if obstacles:
            #for obstacle in obstacles:
            #    obstacle_rects.append(self.make_obstacle_rect(obstacle))

        for obstacle_rect in obstacle_rects:
            if self.check_collision(hero_rect, obstacle_rect):
                return True
        return False
    '''
    def entry_collision(self, hero, entries):
        '''
        if isinstance(hero, spc_hero):
            hero_rect = hero.rect
        else:
            hero_rect = self.make_character_rect(hero)
        '''
        hero_rect = self.make_character_rect(hero)
        #print("hero_rect: x: ", hero_rect.x, " y: ", hero_rect.y, " width: ", hero_rect.width, " height: ",
              #hero_rect.height)
        entry_rects = list()
        if entries:
            # There are obstacles to consider
            for entry in entries:
                entry_rects.append(self.make_obstacle_rect(entry))

        self.entry_index = 0
        for entry_rect in entry_rects:
            if self.check_collision(hero_rect, entry_rect):
                return True
            self.entry_index = self.entry_index + 1
        return False

    def get_collided_entry(self):
        return self.entry_index

    def get_barrier_repulsion(self):
        return self.repulsion

    # This method determines where is the collision happening between two rects
    def check_collision(self, hero_rect, other_rect):

        if hero_rect.colliderect(other_rect):
            if abs(other_rect.top - hero_rect.bottom) < self.__tolerance:
                self.__hit_wall = "bottom"
                return True
            if abs(other_rect.bottom - hero_rect.top) < self.__tolerance:
                self.__hit_wall = "top"
                return True
            if abs(other_rect.right - hero_rect.left) < self.__tolerance:
                self.__hit_wall = "left"
                return True
            if abs(other_rect.left - hero_rect.right) < self.__tolerance:
                self.__hit_wall = "right"
                return True

        return False

    @property
    def hit_wall(self):
        return self.__hit_wall

    @hit_wall.setter
    def hit_wall(self, hit_wall):
        self.__hit_wall = hit_wall