import pygame as pg
import sys
from os import path
from random import choice, choices
from settings import *
from definitions import *
from sprites import *
from tilemap import *


class Game:
    def __init__(self, surface):
        pg.init()
        self.screen = surface
        self.clock = pg.time.Clock()
        self.load_data()
        self.infected = False
        self.survived = False

    def fade_in(self):
        fade = pg.Surface((WIDTH, HEIGHT))
        fade.fill(BLACK)
        self.clock.tick(FPS)
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pg.display.update()
            pg.time.delay(5)

    def load_data(self) -> None:
        """Loads the data from the selected folders"""
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, IMG_FOLDER_NAME)
        self.map_folder = path.join(self.game_folder, MAP_FOLDER_NAME)
        self.sound_folder = path.join(self.game_folder, SND_FOLDER_NAME)
        self.font_folder = path.join(self.game_folder, FONT_FOLDER_NAME)
        self.music_folder = path.join(self.game_folder, MUSIC_FOLDER_NAME)
        # self.title_font = path.join(self.font_folder, 'WolfBrothersBold.ttf')
        # self.text_font1 = path.join(self.font_folder, 'freesansbold.ttf')
        # self.text_font2 = path.join(self.font_folder, "comici.ttf")
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.go_background = load_image(self.img_folder, GAME_OVER_BACKGROUND)
        self.icon = load_image(self.img_folder, ICON_IMG)
        self.crosshairPNG = load_image(self.img_folder, CROSSHAIR)
        self.map = TiledMap(path.join(self.map_folder, MAP_NAME))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.marine_img = load_image_ca(self.img_folder, MARINE_IMG)
        self.bullet_img = load_image_ca(self.img_folder, BULLET_IMG)
        self.bush_img = load_image_ca(self.img_folder, FURRY_SPAWN_COVER)
        self.furry_img_list = []
        for img in FURRIES:
            self.furry_img_list.append(load_image_ca(self.img_folder, img))
        self.furry_corpse = load_image_ca(self.img_folder, FURRY_CORPSE)
        self.furry_corpse = pg.transform.scale(self.furry_corpse, (64, 64))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(load_image_ca(self.img_folder, img))

        # Add Background Music
        load_music(self.music_folder, PICNIC_MUSIC)

        self.effects_sound = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sound[type] = load_sound(self.sound_folder, EFFECTS_SOUNDS[type])
        self.weapon_sounds = {}
        self.weapon_sounds['gun'] = []
        for snd in WEAPON_SOUND_GUN:
            s = load_sound(self.sound_folder, snd)
            s.set_volume(0.35)
            self.weapon_sounds['gun'].append(s)
        self.furry_moan_sounds = []
        for snd in FURRY_MOAN_SOUNDS:
            s = load_sound(self.sound_folder, snd)
            s.set_volume(0.35)
            self.furry_moan_sounds.append(s)
        self.marine_hit_sounds = []
        for snd in MARINE_HIT_SOUNDS:
            self.marine_hit_sounds.append(load_sound(self.sound_folder, snd))
        self.furry_hit_sounds = []
        for snd in FURRY_HIT_SOUNDS:
            self.furry_hit_sounds.append(load_sound(self.sound_folder, snd))
        self.furry_spawns = []
        self.round_value = 0
        self.score_value = 0

    def furry_spawn(self):
        self.round_value += 1
        max_furries = (3 * self.round_value) + 1
        for s in range(max_furries):
            x, y = choice(self.furry_spawns)
            Furry(self, x, y)


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.furries = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.crosshair = pg.sprite.Group()
        for tile_object in self.map.tmx_data.objects:
            if tile_object.name == "player":
                self.marine = Marine(self, tile_object.x, tile_object.y)
            if tile_object.name == "furry":
                furry_pos = (tile_object.x, tile_object.y)
                self.furry_spawns.append(furry_pos)
            if tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "furry_boss":
                pass
        self.camera = Camera(self.map.width, self.map.height)
        self.crosshair.add(Crosshair(self.crosshairPNG))
        self.paused = False
        self.healthbar = pg.sprite.GroupSingle(HealthBar(self))
        self.medkit = pg.sprite.GroupSingle(Medkit(self))
        self.furry_spawn()
        

    def quit_game(self):
        pg.quit()
        sys.exit()

    def pause(self):
        self.screen.blit(self.dim_screen, (0, 0))
        draw_text(self.screen, "Paused", text_font2, 105, RED, WIDTH / 2, ((HEIGHT / 2) - 440), align="center")
        button(self.screen, "Resume", "freesansbold.ttf", 20,  (WIDTH / 2) - 150, 300, 300, 50, (50, 205, 50),
               (0, 255, 0), (0, 0, 0), self.unpause)
        button(self.screen, "Quit to Main Menu", "freesansbold.ttf", 20,  (WIDTH / 2) - 150, 400, 300, 50,
               (50, 205, 50), (0, 255, 0), (0, 0, 0), self.stop_playing)
        button(self.screen, "Quit to Desktop", "freesansbold.ttf", 20,  (WIDTH / 2) - 150, 500, 300, 50, (50, 205, 50),
               (0, 255, 0), (0, 0, 0), self.quit_game)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit_game()
                if event.key == K_p:
                    self.paused = not self.paused

    def stop_playing(self):
        if self.playing:
            self.playing = not self.playing

    def unpause(self):
        if self.paused:
            self.paused = not self.paused

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mouse.set_visible(False)
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.35)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        # update portion of the game loop
        if len(self.furries) == 0:
            self.furry_spawn()
        self.mouse_pos = (pg.mouse.get_pos()[0] - self.camera.camera.x, pg.mouse.get_pos()[1] - self.camera.camera.y)
        self.all_sprites.update()
        self.camera.update(self.marine)

        # furries hit marine
        hits = pg.sprite.spritecollide(self.marine, self.furries, False, collide_hit_rect)
        for hit in hits:
            self.healthbar.sprite.get_damage(FURRY_DAMAGE)
            hit.vel = vec(0, 0)
            if round(self.healthbar.sprite.current_health) <= 0:
                pg.mixer.music.stop()
                self.playing = not self.playing
                self.infected = not self.infected
        if hits:
            self.marine.pos += vec(FURRY_KNOCK_BACK, 0).rotate(-hits[0].rot)

        # bullets hit furries
        hits = pg.sprite.groupcollide(self.furries, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)

        # Update the Medkit
        if self.medkit.sprite.current_energy != self.medkit.sprite.maximum_energy:
            self.medkit.sprite.regenerate()

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:
            if isinstance(sprite, Furry):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        self.screen.blit(self.bush_img, self.camera.apply_rect(self.map_rect))
        draw_text(self.screen, 'Furries: {}'.format(len(self.furries)), title_font, 50, WHITE,
                       WIDTH - 10, 10, align="topright")
        draw_text(self.screen, f"Round: {self.round_value}", title_font, 50, WHITE, WIDTH - 10, 50, align="topright")
        draw_text(self.screen, "FPS: {:.0f}".format(self.clock.get_fps()), title_font, 50, WHITE, 10, 10, align="topleft")
        # Draw both Medkit and Health Bar
        self.crosshair.draw(self.screen)
        self.crosshair.update()
        self.healthbar.update()
        self.medkit.update()
        if self.paused:
            self.pause()

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == QUIT:
                self.quit_game()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit_game()
                if event.key == K_p:
                    self.paused = not self.paused
                if event.key == K_q and self.medkit.sprite.current_energy == self.medkit.sprite.maximum_energy and self.healthbar.sprite.current_health != self.healthbar.sprite.maximum_health:
                    self.medkit.sprite.healing()
                    self.healthbar.sprite.get_health(HEALING_AMOUNT)

    def show_go_screen(self):
        # Function Properties
        run = True

        # Stop the music
        pg.mixer.music.stop()

        # Fading effect
        fade = pg.Surface((WIDTH, HEIGHT))
        fade.fill(BLACK)
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pg.display.update()

        # Play this music after above statements
        game_over_music = load_music(self.sound_folder, GAME_OVER_MUSIC)
        pg.mixer.music.play()

        while run:

            self.screen.blit(self.go_background, (0, 0))
            draw_text(self.screen, "Silly space hooman. You can't just wipe all of us out.",
                           text_font2, 28, WHITE, (WIDTH / 2), (HEIGHT - 100), align="center")
            draw_text(self.screen, "BECAUSE WE FUCK LIKE RABBITS!!!",
                           title_font, 42, WHITE, (WIDTH / 2), (HEIGHT - 50), align="center")
            pg.display.update()


            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit_game()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.quit_game()
                if event.type == pg.MOUSEBUTTONDOWN:
                    pg.mixer.music.stop()
                    run = not run
