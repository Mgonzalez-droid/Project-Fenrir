import pygame


class Collision:
    def __init__(self):
        self.__tolerance = 50

    @staticmethod
    def make_rect(npc):
        character = pygame.Rect(npc.x, npc.y, npc.sprite.get_width(), npc.sprite.get_height())
        return character

    def check_collisions(self, hero, npc):
        hero_rect = self.make_rect(hero)
        npc_rect = self.make_rect(npc)

        if hero_rect.colliderect(npc_rect):
            if abs(npc_rect.top - hero_rect.bottom) < self.__tolerance:
                return True
            if abs(npc_rect.bottom - hero_rect.top) < self.__tolerance:
                return True
            if abs(npc_rect.right - hero_rect.left) < self.__tolerance:
                return True
            if abs(npc_rect.left - hero_rect.right) < self.__tolerance:
                return True

        return False
