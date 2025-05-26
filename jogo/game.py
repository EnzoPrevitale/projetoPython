import pygame
from camera_jogo import Camera

from jogo.world import World
from player import Player
from settings import HEIGHT, WIDTH, FPS, SCALE, tilemap


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
        pygame.display.set_caption("Loja de Games")
        self.clock = pygame.time.Clock()
        self.running = True
        self.sprites = pygame.sprite.Group()
        self.player = Player(500, 500)
        self.sprites.add(self.player)
        self.world = World(tilemap.get_width(), tilemap.get_height())
        self.camera = Camera(tilemap.get_width(), tilemap.get_height())


    def render(self):
        self.screen.fill("#ffffff")
        self.world.generate_world(tilemap, self.screen)
        self.sprites.draw(self.screen, Camera.apply())
        pygame.display.flip()


    def tick(self):
        self.render()
        self.camera.update(self.player)
        self.player.tick(pygame.key.get_pressed())


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.clock.tick(FPS)
            self.tick()
        pygame.quit()

game = Game()
game.run()