import pygame as pg
import win32api
from os import path

# Define for Marine's gun and your monitor's hertz
vec = pg.math.Vector2
device = win32api.EnumDisplayDevices()
settings = win32api.EnumDisplaySettings(device.DeviceName, -1)



# Define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (40, 40, 40)
LIGHT_GREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRASS = (39, 174, 96)
CYAN = (0, 255, 255)

# Game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = getattr(settings, 'DisplayFrequency')
TITLE = "Furry Hunter"
ICON_IMG = "FH icon.png"
CROSSHAIR = "crosshair.png"
BACKGROUND_COLOR = GRASS
INTRO_IMG = 'intro2.png'
SPLASH = "splash2.png"
MAP_NAME = 'picnic_map.tmx'
IMG_FOLDER_NAME = "img"
MAP_FOLDER_NAME = "map"
FONT_FOLDER_NAME = 'font'
SND_FOLDER_NAME = "sound"
MUSIC_FOLDER_NAME = "music"
GAME_OVER_BACKGROUND = "furry marine (hyena).png"

# Player settings
MARINE_SPEED = 350.0
MARINE_ROT_SPEED = 250.0
MARINE_IMG = 'marine1.png'
MARINE_POS = (200, 20)
MARINE_HIT_RECT = pg.Rect(0, 0, 150, 150)
BARREL_OFFSET = vec(120, 40)
MARINE_CURRENT_HEALTH = 300
MARINE_TARGET_HEALTH = 300
MARINE_MAX_HEALTH = 300
BAR_LENGTH = 100
BAR_HEIGHT = 20
FURRY_SPAWN_COVER = "bushes.png"

# Gun Settings
BULLET_IMG = "new_bullet.png"
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
KICKBACk = 200
GUN_SPREAD = 5
BULLET_DAMAGE = 10

# MedKit Settings
CURRENT_ENERGY = 0
MAX_ENERGY = 1000
ENERGY_LENGTH = 250
REGENERATING_AMOUNT = 100
HEALING_AMOUNT = 7500

# Furry settings
# FURRY_CORPSE = {"1": None}
FURRIES = ("polar bear.png", "tiger.png", "black wolf.png", )
FURRY_SPEED = (275, 250, 300, 245, 265)
FURRY_HIT_RECT = pg.Rect(0, 0, 50, 50)
FURRY_HEALTH = 100
FURRY_DAMAGE = 1500
FURRY_KNOCK_BACK = 20
AVOID_RADIUS = 100
DETECT_RADIUS = HEIGHT * 64
NEXT_FURRY_LEVEL = 3

# Effect Setting
MUZZLE_FLASHES = ["new_muzzle.png"]
MUZZLE_DURATION = 40
MUZZLE_OFFSET = vec(145, 40)
FURRY_CORPSE = "splat red.png"

# Layers
WALL_LAYER = 1
MARINE_LAYER = 2
BULLET_LAYER = 1
FURRY_LAYER = 2
EFFECT_LAYER = 4
CROSSHAIR_LAYER = 5

# Sound Settings
GAME_OVER_MUSIC = "Game Over Music.wav"
PICNIC_MUSIC = "The First Wave - Jon Björk.mp3"
MARINE_HIT_SOUNDS = []  # Unused
FURRY_MOAN_SOUNDS = []  # Unused
FURRY_HIT_SOUNDS = ["furry_splat.wav"]
WEAPON_SOUND_GUN = ["gunshot.wav"]
EFFECTS_SOUNDS = {}     # Unused

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, IMG_FOLDER_NAME)
font_folder = path.join(game_folder, FONT_FOLDER_NAME)
title_font = path.join(font_folder, 'WolfBrothersBold.ttf')
text_font1 = path.join(font_folder, 'freesansbold.ttf')
text_font2 = path.join(font_folder, "comici.ttf")