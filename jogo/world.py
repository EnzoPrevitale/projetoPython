import pygame
from settings import WIDTH, HEIGHT, WORLD_TILE_SIZE

class World:
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.tile_grass = pygame.image.load("res/grass.png")
        self.tile_wall = pygame.image.load("res/wall.png")
        self.tile_grass = pygame.transform.scale(self.tile_grass, (32, 32))
        self.tile_wall = pygame.transform.scale(self.tile_wall, (32, 32))
        self.tile_images = {
            0: self.tile_grass,
            1: self.tile_wall,
        }

    def generate_world(self, tilemap, scr):
        for row in range(len(tilemap)):
            for col in range(len(tilemap[row])):
                tile = tilemap[row][col]
                tile_image = self.tile_images[tile]
                scr.blit(tile_image, (col * WORLD_TILE_SIZE, row * WORLD_TILE_SIZE))
