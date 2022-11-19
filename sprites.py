import pygame
from config import *
# import math
# import random


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

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
        self._layer = ENEMIES_LAYER
        self.groups = self.game.all_sprites, self.game.all_enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)

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
            self.x_change += PLAYER_SPEED
        if self.facing == "left":
            self.x_change -= PLAYER_SPEED
        if self.facing == "down":
            self.y_change += PLAYER_SPEED
        if self.facing == "up":
            self.y_change -= PLAYER_SPEED


class Town(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.health = 25
        self.game = game
        self._layer = ENEMIES_LAYER
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

