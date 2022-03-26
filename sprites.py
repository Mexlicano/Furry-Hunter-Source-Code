import pygame as pg
from random import uniform, choice, randint, random
from pygame import transform
from pygame.locals import *
from settings import *
from definitions import *

vec = pg.math.Vector2


class Marine(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MARINE_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.original_image = game.marine_img
        self.image = self.original_image
        self.rect = self.original_image.get_rect(center=(x, y))
        self.rect.center = (x, y)
        self.hit_rect = MARINE_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        
    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[K_a]:
            self.vel = vec(0, -MARINE_SPEED).rotate(-self.rot)
        if keys[K_d]:
            self.vel = vec(0, MARINE_SPEED).rotate(-self.rot)
        if keys[K_w]:
            self.vel = vec(MARINE_SPEED, 0).rotate(-self.rot)
        if keys[K_s]:
            self.vel = vec(-MARINE_SPEED / 2, 0).rotate(-self.rot)

        if keys[K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-(self.rot + 10))
                pos_BT = self.pos + BARREL_OFFSET.rotate(-self.rot)
                pos_MF = self.pos + MUZZLE_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos_BT, dir, (self.rot + 10))
                self.vel = vec(-KICKBACk, 0).rotate(-self.rot)
                choice(self.game.weapon_sounds['gun']).play()
                Muzzle_Flash(self.game, pos_MF, (self.rot + 50))

    def update(self):
        direction = self.game.mouse_pos - self.pos
        angle = direction.as_polar()[1]
        corrected_angle = -(angle - 50)
        self.image = transform_rotozoom(self.original_image, corrected_angle)
        self.rot = -angle
        self.rect = self.image.get_rect(center=self.rect.center)

        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


class Furry(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        """

        :param game:
        :param x:
        :param y:
        """
        self._layer = FURRY_LAYER
        self.groups = game.all_sprites, game.furries
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.furry = choice(game.furry_img_list)
        self.image = self.furry.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = FURRY_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = FURRY_HEALTH
        self.speed = choice(FURRY_SPEED)
        self.target = game.marine

    def avoid_furries(self):
        for furry in self.game.furries:
            if furry != self:
                dist = self.pos - furry.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        try:
            target_dist = self.game.marine.pos - self.pos
            if target_dist.length_squared() < DETECT_RADIUS**2:
                # if random() < 0.002:
                    # choice(self.game.furry_moan_sounds).play()
                self.rot = target_dist.angle_to(vec(1, 0))
                self.image = transform.rotozoom(self.furry, self.rot, 1)
                self.rect.center = self.pos
                self.acc = vec(1, 0).rotate(-self.rot)
                self.avoid_furries()
                self.acc.scale_to_length(self.speed)
                self.acc += self.vel * -1
                self.vel += self.acc * self.game.dt
                self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
                self.hit_rect.centerx = self.pos.x
                collide_with_walls(self, self.game.walls, 'x')
                self.hit_rect.centery = self.pos.y
                collide_with_walls(self, self.game.walls, 'y')
                self.rect.center = self.hit_rect.center
            if self.health <= 0:
                choice(self.game.furry_hit_sounds).play()
                self.kill()
                self.game.map_img.blit(self.game.furry_corpse, self.pos - vec(32, 32))
        except ValueError:
            pass

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / 100)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < 100:
            pg.draw.rect(self.image, col, self.health_bar)


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, angle):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets 
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = transform.rotozoom(self.game.bullet_img, angle, 1)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()


class HealthBar(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.current_health = MARINE_CURRENT_HEALTH
        self.target_health = MARINE_TARGET_HEALTH
        self.maximum_health = MARINE_MAX_HEALTH
        self.health_bar_length = 400
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_change_speed = 5
    
    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount * self.game.dt
        if self.target_health <= 0:
            self.target_health = 0
    
    def get_health(self, amount):
        if self.target_health < self.maximum_health:
            self.target_health += amount * self.game.dt
        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health

    def update(self):
        self.draw()    
    
    def health_color(self):
        if self.target_health / self.maximum_health >= 0.76:    # Aqua-Blue / Azul
            return [(0, 138, 216), (5, 195, 221)]
        if self.target_health / self.maximum_health >= 0.51:    # Green / Verde
            return [(0, 154, 23), (0, 177, 64)]
        if self.target_health / self.maximum_health >= 0.26:    # Yellow / Amarillo
            return [(246, 190, 0), (255, 233, 0)]
        else:   # Red / Rojo
            return [(187, 0, 0), (225, 6, 0)]

    def draw(self):
        color = self.health_color()
        transition_width = 0
        health_bar_width = self.current_health / self.health_ratio
        transition_color = color[1]

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = color[1]
        
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            health_bar_width = self.target_health / self.health_ratio
            transition_width = abs((self.target_health - self.current_health) / self.health_ratio)
            transition_color = color[1]
        
        health_bar_rect = pg.Rect(10, 60, health_bar_width, 25)
        transition_bar_rect = pg.Rect(health_bar_rect.right, 60, transition_width, 25)

        pg.draw.rect(self.game.screen, (99, 102, 106), (10, 60, self.health_bar_length, 25))
        pg.draw.rect(self.game.screen, color[0], health_bar_rect)
        pg.draw.rect(self.game.screen, transition_color, transition_bar_rect)
        pg.draw.rect(self.game.screen, (255, 255, 255), (10, 60, self.health_bar_length, 25), 4)


class Medkit(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.current_energy = CURRENT_ENERGY
        self.maximum_energy = MAX_ENERGY
        self.energy_length = ENERGY_LENGTH
        self.energy_ratio = self.maximum_energy / self.energy_length
        self.amount = REGENERATING_AMOUNT

    def healing(self):
        if self.current_energy > 0:
            self.current_energy -= MAX_ENERGY
        if self.current_energy <= 0:
            self.current_energy = 0
    
    def regenerate(self):
        if self.current_energy < self.maximum_energy:
            self.current_energy += self.amount * self.game.dt
        if self.current_energy >= self.maximum_energy:
            self.current_energy = self.maximum_energy

    def update(self):
        self.draw()

    def draw(self):
        pg.draw.rect(self.game.screen, (0, 0, 255), (10, 90, self.current_energy / self.energy_ratio, 25))
        pg.draw.rect(self.game.screen, (255, 255, 255), (10, 90, self.energy_length, 25), 4)


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Muzzle_Flash(pg.sprite.Sprite):
    def __init__(self, game, pos, angle):
        self._layer = EFFECT_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(70, 100)
        self.image = transform_rotozoom(choice(game.gun_flashes), angle)
        self.image = transform_scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        self.spawn_time = pg.time.get_ticks()
    
    def update(self):
        if pg.time.get_ticks() - self.spawn_time > MUZZLE_DURATION:
            self.kill()


class Crosshair(pg.sprite.Sprite):
    def __init__(self, picture_path):
        self._layer = CROSSHAIR_LAYER
        super().__init__()
        self.image = picture_path
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pg.mouse.get_pos()
