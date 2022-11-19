import pygame
from config import *
from sprites import *
import sys

class Game:
    def __init__(self):
        self.player = None
        self.all_attacks = None
        self.all_enemies = None
        self.all_blocks = None
        self.playing = None
        self.all_sprites = None
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.Font('Arial', 32)
        self.running = True

    def create_tilemap(self):
        for i, row in enumerate(TILEMAP):
            for j, column in enumerate(row):
                if column == "1":
                    Wall(self, j, i)

    def create_enemies(self):
        Enemy(self, 1, 1)

    def new(self):
        # A new game starts
        self.playing = True
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.all_blocks = pygame.sprite.LayeredUpdates()
        self.all_enemies = pygame.sprite.LayeredUpdates()
        self.all_attacks = pygame.sprite.LayeredUpdates()
        self.create_tilemap()
        self.all_sprites.add(PlayerTest(self, 1, 2))
        self.create_enemies()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.draw()
            self.update()
        self.running = False
    def game_over(self):
        pass

    def intro_screen(self):
        pass

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()