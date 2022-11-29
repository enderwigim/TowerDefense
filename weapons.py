import pygame
from config import *
import math
import os
import numpy


class Turret(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
        self._layer = TURRET_LAYER
        self.groups = self.game.turrets, self.game.weapons
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
        self.timer = 0


    def update(self):
        # self.in_the_road()
        self.create_bullets()


    def create_bullets(self):

        for enemy in range(0, len(self.game.all_enemies)):

            enemy_x = self.game.all_enemies.get_sprite(enemy).rect.x
            enemy_y = self.game.all_enemies.get_sprite(enemy).rect.y

            if self.rect.x + TURRET_RANGE + self.width > enemy_x > self.rect.x - TURRET_RANGE and \
                    self.rect.y + TURRET_RANGE + self.height > enemy_y > self.rect.y - TURRET_RANGE:
                self.add_to_list(self.game.all_enemies.get_sprite(enemy))

            else:
                self.remove_from_list(self.game.all_enemies.get_sprite(enemy))

            if self.enemies_in_range:
                self.game.all_enemies.get_sprite(enemy)
                if self.game.all_enemies.get_sprite(enemy) == self.enemies_in_range[0]:
                    # First we need to check if the enemy was the first one to enter into our turrets range.
                    if self.game.all_enemies.get_sprite(enemy).health <= 0:
                        # We check it's health and if it's dead, we remove the enemy from our range list
                        self.remove_from_list(self.game.all_enemies.get_sprite(enemy))
                        pass
                    # Shooting random sistem

                    if pygame.time.get_ticks() - self.timer >= TURRET_TIME_FOR_BULLET:
                        enemy_to_follow = self.game.all_enemies.get_sprite(enemy)
                        new_bullet = Bullets(self.game, self.rect.x, self.rect.y, self.bullet_color, enemy_to_follow,
                                             self, enemy)
                        self.game.all_sprites.add(new_bullet)
                        self.timer = pygame.time.get_ticks()

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
        self.groups = self.game.crossbow, self.game.all_sprites, self.game.weapons
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
        self.timer = 0


    def update(self):
        # self.in_the_road()

        self.create_bullets()

    def create_bullets(self):

        for enemy in range(0, len(self.game.all_enemies)):

            enemy_x = self.game.all_enemies.get_sprite(enemy).rect.x
            enemy_y = self.game.all_enemies.get_sprite(enemy).rect.y

            if self.rect.x + CROSSBOW_RANGE + self.width > enemy_x > self.rect.x - CROSSBOW_RANGE and \
                    self.rect.y + CROSSBOW_RANGE + self.height > enemy_y > self.rect.y - CROSSBOW_RANGE:
                self.add_to_list(self.game.all_enemies.get_sprite(enemy))

            else:
                self.remove_from_list(self.game.all_enemies.get_sprite(enemy))

            if self.enemies_in_range:
                self.game.all_enemies.get_sprite(enemy)
                if self.game.all_enemies.get_sprite(enemy) == self.enemies_in_range[0]:
                    # First we need to check if the enemy was the first one to enter into our turrets range.
                    if self.game.all_enemies.get_sprite(enemy).health <= 0:
                        # We check it's health and if it's dead, we remove the enemy from our range list
                        self.remove_from_list(self.game.all_enemies.get_sprite(enemy))
                        pass
                    # Shooting random sistem

                    if pygame.time.get_ticks() - self.timer >= CROSSBOW_COST:
                        enemy_to_follow = self.game.all_enemies.get_sprite(enemy)
                        new_bullet = Bullets(self.game, self.rect.x, self.rect.y, self.bullet_color, enemy_to_follow,
                                             self, enemy)
                        self.game.all_sprites.add(new_bullet)
                        self.timer = pygame.time.get_ticks()


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
            self.enemy_to_follow.health -= 1
            self.game.shop.coins += 50
            self.kill()