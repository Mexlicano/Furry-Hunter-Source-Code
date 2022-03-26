import pygame as pg
# from pygame import mixer
from os import path
from settings import *


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def load_image_ca(folder_name, img):
    return pg.image.load(path.join(folder_name, img)).convert_alpha()


def load_image(folder_name, img):
    return pg.image.load(path.join(folder_name, img))


def load_sound(folder_name, sound):
    return pg.mixer.Sound(path.join(folder_name, sound))


def load_music(folder_name, music):
    return pg.mixer.music.load(path.join(folder_name, music))


def transform_scale(name, size):
    return pg.transform.scale(name, size)


def transform_rotozoom(name, angle):
    return pg.transform.rotozoom(name, angle, 1)


def transform_rotate(name, size):
    return pg.transform.rotate(name, size)


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2.0
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2.0
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2.0
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2.0
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


def draw_text(surface, text, font_name, size, color, x, y, align="topleft"):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    surface.blit(text_surface, text_rect)


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def button(surface, string, font_name, size, x, y, width, height, ic, ac, tc, action=None):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pg.draw.rect(surface, ac, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pg.draw.rect(surface, ic, (x, y, width, height))

    try:
        small_text = pg.font.Font(font_name, size)
    except FileNotFoundError:
        small_text = pg.font.SysFont(font_name, size)

    text_surf, text_rect = text_objects(string, small_text, tc)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    surface.blit(text_surf, text_rect)
