import pygame


class Collision:
    def __init__(self):
        self.__tolerance = 50

    @staticmethod
    def make_rect(npc):
        character = pygame.Rect(npc.x, npc.y, npc.sprite.get_width(), npc.sprite.get_height())
        return character

    @staticmethod
    def make_obstacle_rect(obstacle):
        obstacle = pygame.Rect(obstacle.x, obstacle.y, obstacle.get_width(), obstacle.get_height())
        return obstacle

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
