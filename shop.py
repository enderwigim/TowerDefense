import pygame
from config import *
import math
import os
import numpy


class Shop:
    def __init__(self, game):
        self.game = game
        self.coins = 0
        self.last_time_stamp = 0

        self.defense_to_buy = None
        self.coin_sprite = Coin(self.game, 28, 1)
        self.turret_button = TurretButton(self.game, 28, 3)
        self.cross_button = CrossBowButton(self.game, 28, 5)

    def get_coins(self):
        time_stamp = pygame.time.get_ticks()
        if (time_stamp - self.last_time_stamp) >= TIME_TO_GET_COINS:
            self.coins += 10
            self.last_time_stamp = time_stamp
        else:
            pass

    def draw_coins(self):
        font_coins = FONT.render(f"{self.game.shop.coins}", True, WHITE)
        self.game.screen.blit(font_coins, (29 * 32, 26))
        self.turret_button.update()
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


class TurretButton(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = BULLET_LAYER
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join("Assets/Shop", "TurretButton.png")))
        self.sprites.append(pygame.image.load(os.path.join("Assets/Shop", "TurretButton2.png")))

        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.button_on_off = "off"

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.sprites[0]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.button_on_off == "off":
            self.image = self.sprites[0]
        elif self.button_on_off == "on":
            self.image = self.sprites[1]

    def click_button(self):
        if self.button_on_off == "off":
            self.button_on_off = "on"
        elif self.button_on_off == "on":
            self.button_on_off = "off"

        self.game.shop.defense_to_buy = "crossbow"

        self.game.shop.cross_button.button_on_off = "off"


class CrossBowButton(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = BULLET_LAYER
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join("Assets/Shop", "CrossButton.png")))
        self.sprites.append(pygame.image.load(os.path.join("Assets/Shop", "CrossPushed.png")))

        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.button_on_off = "off"

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.sprites[0]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.button_on_off == "off":
            self.image = self.sprites[0]
        elif self.button_on_off == "on":
            self.image = self.sprites[1]

    def click_button(self):
        if self.button_on_off == "off":
            self.button_on_off = "on"
        elif self.button_on_off == "on":
            self.button_on_off = "off"

        self.game.shop.defense_to_buy = "crossbow"

        self.game.shop.turret_button.button_on_off = "off"