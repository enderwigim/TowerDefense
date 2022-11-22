import pygame
from config import *
import math
import os
import numpy
# import random

class SpriteSheet:
    def __init__(self, directory, file):
        self.sheet = pygame.image.load(os.path.join(directory, file)).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class PlayerTest(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def collide_wall(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.all_blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.all_blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.collide_wall("x")
        self.rect.y += self.y_change
        self.collide_wall("y")

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = "left"
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = "right"
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = "up"
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = "down"


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.all_blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_sprite_sheet.get_sprite(130, 229, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Road(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.all_road
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_sprite_sheet.get_sprite(30, 387, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.health = 2
        self.game = game
        self._layer = ENEMIES_LAYER
        self.groups = self.game.all_sprites, self.game.all_enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.enemy_sprite_sheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.can_walk = False
        self.initial_position()

        self.x_change = 0
        self.y_change = 0
        self.facing = "right"

    def initial_position(self):
        # Won't appear on a Wall
        while not self.can_walk:
            hits = pygame.sprite.spritecollide(self, self.game.all_blocks, False)
            if hits:
                self.rect.y += TILESIZE
            else:
                self.rect.y += TILESIZE / 2
                self.can_walk = True

    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.collision("x")

        self.rect.y += self.y_change
        self.collision("y")

        self.x_change = 0
        self.y_change = 0

        self.attack_town()

        if self.health <= 0:
            self.kill()

    def collision(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.all_blocks, False)
            if hits:
                # Go right
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    self.facing = "down"
                # Go left
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    self.facing = "down"

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.all_blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    self.facing = "right"
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    self.facing = "left"

    def attack_town(self):
        town_attack = pygame.sprite.spritecollide(self, self.game.town, False)
        if town_attack:
            self.game.town.get_sprite(0).health -= 1
            print(self.game.town.get_sprite(0).health)
            self.kill()

    def movement(self):
        if self.facing == "right":
            self.x_change += ENEMIES_SPEED
        if self.facing == "left":
            self.x_change -= ENEMIES_SPEED
        if self.facing == "down":
            self.y_change += ENEMIES_SPEED
        if self.facing == "up":
            self.y_change -= ENEMIES_SPEED


class Town(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.health = 25
        self.game = game
        self._layer = TOWN_LAYER
        self.groups = self.game.town
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * 2
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.health == 0:
            self.kill()


class Turret(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
        self._layer = TURRET_LAYER
        self.groups = self.game.turrets
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        # self.in_the_road()
        self.create_bullets()

    def create_bullets(self):
        rand_num = numpy.random.uniform(0, 50)
        if int(rand_num) == 1:
            new_bullet = Bullets(self.game, self.rect.x, self.rect.y)
            self.game.all_sprites.add(new_bullet)

    def in_the_road(self):
        # Check if the turret is not stuck in the middle in the road.
        in_the_road = pygame.sprite.spritecollide(self, self.game.all_blocks, False)
        if not in_the_road:
            self.kill()


class Bullets(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = BULLET_LAYER
        self.groups = self.game.bullets, self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.move_to_enemy()
        self.attack_enemy()

    def move_to_enemy(self):
        # Find direction vector (dx, dy) between enemy and player.
        try:
            dx, dy = self.game.all_enemies.get_sprite(0).rect.x - self.rect.x, self.game.all_enemies.get_sprite(0).rect.y - self.rect.y
        except IndexError:
            # If enemy was killed, the bullets will disappear
            self.kill()
        else:
            dist = math.hypot(dx, dy)
            dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            self.rect.x += dx * BULLET_SPEED
            self.rect.y += dy * BULLET_SPEED

    def attack_enemy(self):
        hit_enemy = pygame.sprite.spritecollide(self, self.game.all_enemies, False)

        if hit_enemy:
            hit_enemy[0].health -= 1
            self.game.shop.coins += 50
            self.kill()


class MouseUser:
    def __init__(self, game):
        self.game = game

    def create_turrets(self, tx, ty):
        # Input mouse position as new Turret x and new Turret y. If it's in the road, in_the_road() kills it.
        if self.game.shop.coins >= 700:
            self.game.all_sprites.add(Turret(self.game, tx, ty))
            self.in_the_road()
            self.game.shop.coins -= 700
        else:
            print("Not enough coins!")

    def in_the_road(self):
        # Check if the turret has been created in the middle of the road, it kills it.
        last_turret = self.game.turrets.get_sprite(-1)
        in_the_road = pygame.sprite.spritecollide(last_turret, self.game.all_blocks, False)
        if not in_the_road:
            last_turret.kill()


class Shop:
    def __init__(self, game):
        self.game = game
        self.coins = 0
        self.last_time_stamp = 0
        self.coin_sprite = Coin(self.game, 28, 1)

    def get_coins(self):
        time_stamp = pygame.time.get_ticks()
        if (time_stamp - self.last_time_stamp) >= TIME_TO_GET_COINS:
            self.coins += 100
            self.last_time_stamp = time_stamp
        else:
            pass

    def draw_coins(self):
        font_coins = FONT.render(f"{self.game.shop.coins}", True, WHITE)
        self.game.screen.blit(font_coins, (29 * 32, 26))
        pygame.display.update()


class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = BULLET_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.coin_sprite_sheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
