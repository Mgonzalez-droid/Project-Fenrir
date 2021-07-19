import pygame


class Collision:
    def __init__(self):
        # self.__tolerance = 50
        self.__tolerance = 35
        self.entry_index = 0
        self.repulsion = 0

    @staticmethod
    def make_character_rect(npc):
        character = pygame.Rect(npc.x, npc.y, npc.sprite.get_width(), npc.sprite.get_height())
        return character

    @staticmethod
    def make_obstacle_rect(obstacle):
        obstacle = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
        return obstacle

    def npc_collision(self, hero, npc):
        hero_rect = self.make_character_rect(hero)
        npc_rect = self.make_character_rect(npc)

        self.repulsion = 0

        if self.check_collision(hero_rect, npc_rect):
            return True
        else:
            return False

    def barrier_collision(self, hero, obstacles):
        hero_rect = self.make_character_rect(hero)
        obstacle_rects = list()
        if obstacles:
            for obstacle in obstacles:
                obstacle_rects.append(self.make_obstacle_rect(obstacle))

        for obstacle_rect in obstacle_rects:
            if self.check_collision(hero_rect, obstacle_rect):
                return True
        return False

    def entry_collision(self, hero, entries):
        hero_rect = self.make_character_rect(hero)
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

    # Deprecated code
    def check_collisions(self, hero, npc, obstacles=list()):
        hero_rect = self.make_character_rect(hero)
        npc_rect = self.make_character_rect(npc)
        obstacle_rects = list()
        if obstacles:
            # There are obstacles to consider
            for obstacle in obstacles:
                obstacle_rects.append(self.make_obstacle_rect(obstacle))

        if self.check_collision(hero_rect, npc_rect):
            return True

        for obstacle_rect in obstacle_rects:
            if self.check_collision(hero_rect, obstacle_rect):
                return True
        return False

    # This method determines where is the collision happening between two rects
    def check_collision(self, hero_rect, other_rect):

        if hero_rect.colliderect(other_rect):
            if abs(other_rect.top - hero_rect.bottom) < self.__tolerance:
                return True
            if abs(other_rect.bottom - hero_rect.top) < self.__tolerance:
                return True
            if abs(other_rect.right - hero_rect.left) < self.__tolerance:
                return True
            if abs(other_rect.left - hero_rect.right) < self.__tolerance:
                return True

        return False
