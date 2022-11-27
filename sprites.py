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
            # self.kill()
            pass

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
        self.bullet_color = YELLOW
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

        self.enemies_in_range = []


    def update(self):
        # self.in_the_road()
        self.create_bullets()


    def create_bullets(self):

        for enemy in range(0, len(self.game.all_enemies)):

            enemy_x = self.game.all_enemies.get_sprite(enemy).rect.x
            enemy_y = self.game.all_enemies.get_sprite(enemy).rect.y

            if self.rect.x + TURRET_RANGE > enemy_x > self.rect.x - TURRET_RANGE and \
                    self.rect.y + TURRET_RANGE > enemy_y > self.rect.y - TURRET_RANGE:
                self.add_to_list(self.game.all_enemies.get_sprite(enemy))

            else:
                self.remove_from_list(self.game.all_enemies.get_sprite(enemy))

            if self.enemies_in_range:
                if self.game.all_enemies.get_sprite(enemy) == self.enemies_in_range[0]:
                    # First we need to check if the enemy was the first one to enter into our turrets range.
                    if self.game.all_enemies.get_sprite(enemy).health <= 0:
                        # We check it's health and if it's dead, we remove the enemy from our range list
                        # self.remove_from_list(self.game.all_enemies.get_sprite(enemy))
                        pass
                    # Shooting random sistem

                    # rand_num = numpy.random.uniform(0, 50)
                    # if int(rand_num) == 1:
                    enemy_to_follow = self.game.all_enemies.get_sprite(enemy)
                    new_bullet = Bullets(self.game, self.rect.x, self.rect.y, self.bullet_color, enemy_to_follow,
                                         self, enemy)
                    self.game.all_sprites.add(new_bullet)

    def add_to_list(self, enemy):
        if enemy not in self.enemies_in_range:
            self.enemies_in_range.append(enemy)

    def remove_from_list(self, enemy):
        if enemy in self.enemies_in_range:
            self.enemies_in_range.remove(enemy)




    def in_the_road(self):
        # Check if the turret is not stuck in the middle in the road.
        in_the_road = pygame.sprite.spritecollide(self, self.game.all_blocks, False)
        if not in_the_road:
            self.kill()


class Crossbow(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
        self._layer = TURRET_LAYER
        self.groups = self.game.crossbow, self.game.all_sprites
        self.bullet_color = BLACK
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * 2
        self.height = TILESIZE * 2

        self.image = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemies_Turrets", "CrossBow.png")),
                                            (64, 64))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.enemies_in_range = []


    def update(self):
        # self.in_the_road()

        self.create_bullets()

    def create_bullets(self):

        for enemy in range(0, len(self.game.all_enemies)):

            enemy_x = self.game.all_enemies.get_sprite(enemy).rect.x
            enemy_y = self.game.all_enemies.get_sprite(enemy).rect.y

            if self.rect.x + CROSSBOW_RANGE > enemy_x > self.rect.x - CROSSBOW_RANGE and \
                    self.rect.y + CROSSBOW_RANGE > enemy_y > self.rect.y - CROSSBOW_RANGE:
                self.add_to_list(self.game.all_enemies.get_sprite(enemy))

            else:
                self.remove_from_list(self.game.all_enemies.get_sprite(enemy))

            if self.enemies_in_range:
                if self.game.all_enemies.get_sprite(enemy) == self.enemies_in_range[0]:
                    # First we need to check if the enemy was the first one to enter into our turrets range.
                    if self.game.all_enemies.get_sprite(enemy).health <= 0:
                        # We check it's health and if it's dead, we remove the enemy from our range list
                        self.remove_from_list(self.game.all_enemies.get_sprite(enemy))
                    # Shooting random sistem
                    rand_num = numpy.random.uniform(0, 50)
                    if int(rand_num) == 1:
                        enemy_to_follow = self.game.all_enemies.get_sprite(enemy)
                        new_bullet = Bullets(self.game, self.rect.x, self.rect.y, self.bullet_color, enemy_to_follow,
                                             self, enemy)
                        self.game.all_sprites.add(new_bullet)

    def add_to_list(self, enemy):
        if enemy not in self.enemies_in_range:
            self.enemies_in_range.append(enemy)

    def remove_from_list(self, enemy):
        if enemy in self.enemies_in_range:
            self.enemies_in_range.remove(enemy)

    def in_the_road(self):
        # Check if the turret is not stuck in the middle in the road.
        in_the_road = pygame.sprite.spritecollide(self, self.game.all_blocks, False)
        if not in_the_road:
            self.kill()


class Bullets(pygame.sprite.Sprite):
    def __init__(self, game, x, y, color, enemy_to_follow, weapon_that_launched, enemy_index):
        super().__init__()
        self.game = game
        self._layer = BULLET_LAYER
        self.groups = self.game.bullets, self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = 5
        self.height = 10

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.enemy_to_follow = enemy_to_follow
        self.weapon_that_launched = weapon_that_launched
        self.enemy_index = enemy_index

    def update(self):
        self.move_to_enemy()
        self.attack_enemy()

    def move_to_enemy(self):
        # Find direction vector (dx, dy) between enemy and player.
        try:
            dx, dy = self.enemy_to_follow.rect.x - self.rect.x, self.enemy_to_follow.rect.y - self.rect.y
        except IndexError:
            # If enemy was killed, the bullets will disappear
            self.kill()

        else:
            if self.enemy_to_follow.health <= 0:
                self.kill()

            else:
                dist = math.hypot(dx, dy)
                try: dx, dy = dx / dist, dy / dist  # Normalize.
                except ZeroDivisionError:
                    pass
                # Move along this normalized vector towards the player at current speed.
                self.rect.x += dx * BULLET_SPEED
                self.rect.y += dy * BULLET_SPEED

    def attack_enemy(self):
        hit_enemy = self.enemy_to_follow.rect.colliderect(self)

        if hit_enemy:
            print("hit!")
            # self.enemy_to_follow.health -= 1
            self.game.shop.coins += 50
            self.kill()


class MouseUser:
    def __init__(self, game):
        self.game = game

    def create_turrets(self, tx, ty):
        # Input mouse position as new Turret x and new Turret y. If it's in the road, in_the_road() kills it.
        if self.game.shop.coins >= TURRET_COST and self.game.shop.turret_button.button_on_off == "on":
            new_turret = Turret(self.game, tx, ty)
            self.game.all_sprites.add(new_turret)
            self.turret_in_the_road()
            self.game.shop.coins -= TURRET_COST
        else:
            pass

    def create_crossbow(self, tx, ty):
        # Input mouse position as new Turret x and new Turret y. If it's in the road, in_the_road() kills it.
        if self.game.shop.coins >= CROSSBOW_COST and self.game.shop.cross_button.button_on_off == "on":
            self.game.all_sprites.add(Crossbow(self.game, tx, ty))
            self.crossbow_in_the_road()
            self.game.shop.coins -= CROSSBOW_RANGE
        else:
            pass

    def turret_in_the_road(self):
        # Check if the turret has been created in the middle of the road, it kills it.
        last_turret = self.game.turrets.get_sprite(-1)
        in_the_road = pygame.sprite.spritecollide(last_turret, self.game.all_blocks, False)
        if not in_the_road:
            last_turret.kill()

    def crossbow_in_the_road(self):
        # Check if the turret has been created in the middle of the road, it kills it.
        last_turret = self.game.crossbow.get_sprite(-1)
        in_the_road = pygame.sprite.spritecollide(last_turret, self.game.all_blocks, False)
        if not in_the_road:
            last_turret.kill()

    def create_defense(self, mx, my):
        self.create_turrets(mx, my)
        self.create_crossbow(mx, my)


class Shop:
    def __init__(self, game):
        self.game = game
        self.coins = 0
        self.last_time_stamp = 0

        self.defense_to_buy = None
        self.coin_sprite = Coin(self.game, 28, 1)
        self.turret_button = Turret_Button(self.game, 28, 3)
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


class Turret_Button(pygame.sprite.Sprite):
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

