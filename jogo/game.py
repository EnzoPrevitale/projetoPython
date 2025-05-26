import pygame

from jogo.world import World
from player import Player
from settings import HEIGHT, WIDTH, FPS

tilemap = [
    [1, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
]

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Loja de Games")
        self.clock = pygame.time.Clock()
        self.running = True
        self.sprites = pygame.sprite.Group()
        self.player = Player(500, 500)
        self.sprites.add(self.player)
        self.world = World(len(tilemap[0]), len(tilemap))


    def render(self):
        self.world.generate_world(tilemap, self.screen)
        self.screen.fill("#ffffff")
        self.sprites.draw(self.screen)
        pygame.display.flip()


    def tick(self):
        self.render()
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