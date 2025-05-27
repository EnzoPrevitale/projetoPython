import pygame
from settings import WIDTH, HEIGHT, SCALE

class Camera:
    def __init__(self, map_width, map_height):
        self.offset = pygame.Vector2(0, 0)
        self.map_width = map_width
        self.map_heigth = map_height

    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)

    def update(self, player):
        self.offset.x = player.rect.centerx - WIDTH * SCALE // 2
        self.offset.y = player.rect.centery - HEIGHT * SCALE // 2

        self.offset.x = max(0, int(min(self.offset.x, self.map_width - WIDTH * SCALE)))
        self.offset.y = max(0, int(min(self.offset.y, self.map_heigth - HEIGHT * SCALE)))