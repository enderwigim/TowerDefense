from weapons import *


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
