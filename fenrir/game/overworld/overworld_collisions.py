import pygame


class Collision:
    def __init__(self):
        #self.__tolerance = 50
        self.__tolerance = 35
        self.entry_index = 0
        self.repulsion = 0

    @staticmethod
    def make_rect(npc):
        character = pygame.Rect(npc.x, npc.y, npc.sprite.get_width(), npc.sprite.get_height())
        return character

    @staticmethod
    def make_obstacle_rect(obstacle):
        obstacle = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
        return obstacle


    def npc_collision(self, hero, npc):
        hero_rect = self.make_rect(hero)
        npc_rect = self.make_rect(npc)

        self.repulsion = 0
        if hero_rect.colliderect(npc_rect):
            if abs(npc_rect.top - hero_rect.bottom) < self.__tolerance:
                return True
            if abs(npc_rect.bottom - hero_rect.top) < self.__tolerance:
                return True
            if abs(npc_rect.right - hero_rect.left) < self.__tolerance:
                return True
            if abs(npc_rect.left - hero_rect.right) < self.__tolerance:
                return True
        else:
            return False


    def barrier_collision(self, hero, obstacles):
        hero_rect = self.make_rect(hero)
        obstacle_rects = list()
        if obstacles:
            for obstacle in obstacles:
                obstacle_rects.append(self.make_obstacle_rect(obstacle))

        for obstacle_rect in obstacle_rects:
            if hero_rect.colliderect(obstacle_rect):
                if abs(obstacle_rect.top - hero_rect.bottom) < self.__tolerance:
                    # move opposite y direction
                    return True
                if abs(obstacle_rect.bottom - hero_rect.top) < self.__tolerance:
                    # move opposite y direction
                    return True
                if abs(obstacle_rect.right - hero_rect.left) < self.__tolerance:
                    # move opposite x direction
                    return True
                if abs(obstacle_rect.left - hero_rect.right) < self.__tolerance:
                    # move opposite x direction
                    return True
        return False

    def entry_collision(self, hero, entries):
        hero_rect = self.make_rect(hero)
        entry_rects = list()
        if entries:
            # There are obstacles to consider
            for entry in entries:
                entry_rects.append(self.make_obstacle_rect(entry))

        self.entry_index = 0
        for entry_rect in entry_rects:
            if hero_rect.colliderect(entry_rect):
                if abs(entry_rect.top - hero_rect.bottom) < self.__tolerance:
                    return True
                if abs(entry_rect.bottom - hero_rect.top) < self.__tolerance:
                    return True
                if abs(entry_rect.right - hero_rect.left) < self.__tolerance:
                    return True
                if abs(entry_rect.left - hero_rect.right) < self.__tolerance:
                    return True
            self.entry_index = self.entry_index + 1
        return False

    def get_collided_entry(self):
        return self.entry_index

    def get_barrier_repulsion(self):
        return self.repulsion

    # Deprecated code
    def check_collisions(self, hero, npc, obstacles=list()):
        hero_rect = self.make_rect(hero)
        npc_rect = self.make_rect(npc)
        obstacle_rects = list()
        if obstacles:
            # There are obstacles to consider
            for obstacle in obstacles:
                obstacle_rects.append(self.make_obstacle_rect(obstacle))

        if hero_rect.colliderect(npc_rect):
            if abs(npc_rect.top - hero_rect.bottom) < self.__tolerance:
                return True
            if abs(npc_rect.bottom - hero_rect.top) < self.__tolerance:
                return True
            if abs(npc_rect.right - hero_rect.left) < self.__tolerance:
                return True
            if abs(npc_rect.left - hero_rect.right) < self.__tolerance:
                return True

        for obstacle_rect in obstacle_rects:
            if hero_rect.colliderect(obstacle_rect):
                if abs(obstacle_rect.top - hero_rect.bottom) < self.__tolerance:
                    return True
                if abs(obstacle_rect.bottom - hero_rect.top) < self.__tolerance:
                    return True
                if abs(obstacle_rect.right - hero_rect.left) < self.__tolerance:
                    return True
                if abs(obstacle_rect.left - hero_rect.right) < self.__tolerance:
                    return True

        return False
