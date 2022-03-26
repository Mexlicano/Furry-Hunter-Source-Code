import game
import sys
from definitions import *
from settings import *
import pygame as pg
from pygame.locals import *


class Main_Menu:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.icon = load_image("img", ICON_IMG)
        pg.display.set_caption(TITLE)
        pg.display.set_icon(self.icon)
        self.clock = pg.time.Clock()
        self.splash = load_image_ca(img_folder, SPLASH)
        self.intro = load_image_ca(img_folder, INTRO_IMG)

    def quit_menu(self):
        pg.quit()
        sys.exit()

    def play(self):
        self.fade_in()
        g = game.Game(self.screen)
        g.new()
        g.run()
        g.show_go_screen()

    def fade_in(self):
        fade = pg.Surface((WIDTH, HEIGHT))
        fade.fill(BLACK)
        self.clock.tick(FPS)
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pg.display.update()
            pg.time.delay(5)

    def fade_intro(self):
        fade_max = 255
        self.clock.tick(FPS)
        for i in range(fade_max):
            self.screen.fill((0, 0, 0))
            self.splash.set_alpha(i)
            self.screen.blit(self.splash, (0, 0))
            pg.display.flip()

        for e in range(fade_max):
            self.screen.fill((0, 0, 0))
            self.splash.set_alpha(fade_max - e)
            self.screen.blit(self.splash, (0, 0))
            pg.display.flip()

    def main_menu(self):

        while True:
            self.clock.tick(FPS)
            self.screen.fill(BLACK)
            self.screen.blit(self.intro, (0, 0))
            draw_text(self.screen, "FURRY HUNTER", title_font, 90, WHITE, (WIDTH / 2), 150, "center")

            pg.mouse.set_visible(True)
            button(self.screen, "Play", text_font1, 25, (WIDTH / 2) - 150, 250, 300, 50,
                   (50, 205, 50), (0, 255, 0), (0, 0, 0), self.play)

            button(self.screen, "Quit to Desktop", text_font1, 25, (WIDTH / 2) - 150, 350, 300, 50,
                   (50, 205, 50), (0, 255, 0), (0, 0, 0), self.quit_menu)

            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit_menu()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.quit_menu()
            pg.display.update()



if __name__ == "__main__":
    m = Main_Menu()
    m.fade_intro()
    m.main_menu()
