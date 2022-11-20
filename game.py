import pygame
from pygame.locals import *
from config import *
from sprites import *
import sys
import random

class Game:
    def __init__(self):
        self.mouse = None
        self.bullets = None
        self.town = None
        self.player = None
        self.all_attacks = None
        self.all_enemies = None
        self.all_blocks = None
        self.playing = None
        self.all_sprites = None
        self.turrets = None
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.Font('Arial', 32)
        self.running = True
        self.amount_of_enemies = 0
        self.last_time_stamp = 0

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

        self.mouse = MouseUser(self)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.all_blocks = pygame.sprite.LayeredUpdates()
        self.all_enemies = pygame.sprite.LayeredUpdates()
        self.all_attacks = pygame.sprite.LayeredUpdates()
        self.town = pygame.sprite.LayeredUpdates()
        self.turrets = pygame.sprite.LayeredUpdates()
        self.bullets = pygame.sprite.LayeredUpdates()

        self.create_tilemap()
        self.all_sprites.add(PlayerTest(self, 1, 2))
        self.all_sprites.add(Town(self, 27, 22))
        self.all_sprites.add(Turret(self, 22, 22))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Right Click
                    mx = pygame.mouse.get_pos()[0]
                    my = pygame.mouse.get_pos()[1]
                    # They are divided by 32 because the object position is * 32 when you create it.
                    self.mouse.create_turrets(tx=mx//32, ty=my//32)

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
            time_stamp = pygame.time.get_ticks()
            if (time_stamp - self.last_time_stamp) >= 500 and self.amount_of_enemies <= 10:
                self.create_enemies()
                self.last_time_stamp = time_stamp
                self.amount_of_enemies += 1
            else:
                pass

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