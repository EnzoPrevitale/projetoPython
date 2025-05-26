import pygame
from camera_jogo import Camera
from settings import WIDTH, HEIGHT, WORLD_TILE_SIZE, SCALE


def rgba_to_hex(rgba):
    return "#{:02x}{:02x}{:02x}".format(rgba[0], rgba[1], rgba[2])


class World:
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.tile_grass = pygame.image.load("res/grass.png")
        self.tile_wall = pygame.image.load("res/wall.png")
        self.tile_grass = pygame.transform.scale(self.tile_grass, (WORLD_TILE_SIZE * SCALE, WORLD_TILE_SIZE * SCALE))
        self.tile_wall = pygame.transform.scale(self.tile_wall, (WORLD_TILE_SIZE * SCALE, WORLD_TILE_SIZE * SCALE))
        self.tile_images = {
            "#000000": self.tile_grass,
            "#ffffff": self.tile_wall,
        }

    def generate_world(self, tilemap, scr):
        for row in range(tilemap.get_width()):
            for col in range(tilemap.get_height()):
                tile = rgba_to_hex(tilemap.get_at((row, col)))
                tile_image = self.tile_images[tile]
                x = col * WORLD_TILE_SIZE * SCALE - Camera.offset.x
                y = col * WORLD_TILE_SIZE * SCALE - Camera.offset.y

                scr.blit(tile_image, (x, y))
