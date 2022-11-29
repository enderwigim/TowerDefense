import pygame
from pygame.locals import *
from config import *
from sprites import *
from map import *
from user import *
from shop import *
from weapons import *
from map import *
import sys
import random




class Game:
    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.Font('Arial', 32)
        self.running = True

        self.enemy_sprite_sheet = SpriteSheet("Assets/Enemies_Turrets", "enemy.png")
        self.terrain_sprite_sheet = SpriteSheet("Assets/Map", "Tiles.png")
        self.coin_sprite_sheet = SpriteSheet("Assets/Enemies_Turrets", "Coin.png")
        self.amount_of_enemies = 0
        self.last_time_stamp = 0
        self.timer = 0

    def create_tilemap(self):
        for i, row in enumerate(TILEMAP):
            for j, column in enumerate(row):
                if column == "1":
                    Wall(self, j, i)
                else:
                    Road(self, j, i)

    def create_enemies(self):
        Enemy(self, 1, 1)

    def new(self):
        # A new game starts
        self.playing = True

        self.mouse = MouseUser(self)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.all_blocks = pygame.sprite.LayeredUpdates()
        self.all_road = pygame.sprite.LayeredUpdates()
        self.all_enemies = pygame.sprite.LayeredUpdates()
        self.all_attacks = pygame.sprite.LayeredUpdates()
        self.town = pygame.sprite.LayeredUpdates()
        self.turrets = pygame.sprite.LayeredUpdates()
        self.crossbow = pygame.sprite.LayeredUpdates()
        self.weapons = pygame.sprite.LayeredUpdates()
        self.bullets = pygame.sprite.LayeredUpdates()
        self.shop = Shop(self)

        self.create_tilemap()
        self.all_sprites.add(Town(self, 27, 22))
        self.all_sprites.add(Turret(self, 3, 10))
        self.all_sprites.add(Crossbow(self, 27, 19))


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Right Click
                    mx = pygame.mouse.get_pos()[0]
                    my = pygame.mouse.get_pos()[1]
                    if mx in CROSSBOW_BUTTON_X and my in CROSSBOW_BUTTON_Y:
                        self.shop.cross_button.click_button()
                    elif mx in TURRET_BUTTON_X and my in TURRET_BUTTON_Y:
                        self.shop.turret_button.click_button()
                    else:
                        # They are divided by 32 because the object position is * 32 when you create it.
                        self.mouse.create_defense(mx//32, my//32)

    def update(self):
        self.all_sprites.update()
        self.shop.get_coins()
        for n in range(len(self.turrets)):
            print(f"Turret {n}: {self.turrets.get_sprite(n).timer}")

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        self.shop.draw_coins()
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            time_stamp_enemies = pygame.time.get_ticks()
            if (time_stamp_enemies - self.last_time_stamp) >= 1000 and self.amount_of_enemies <= 10:
                self.create_enemies()
                self.amount_of_enemies += 1
                self.last_time_stamp = time_stamp_enemies

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