import pygame
from settings import WIDTH, HEIGHT, SCALE

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load('res/triangulo.png')
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.speed = 10


    def tick(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

        if self.y <= 0:
            self.y = 0
        if self.y >= HEIGHT * SCALE - self.rect.height:
            self.y = HEIGHT * SCALE - self.rect.height
        if self.x <= 0:
            self.x = 0
        if self.x >= WIDTH * SCALE - self.rect.width:
            self.x = WIDTH * SCALE - self.rect.width

        self.rect.x = self.x
        self.rect.y = self.y