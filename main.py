# this file was created by Jacob Brandis
# Sources: goo.gl/2KMivS and Mr. Cozort's file

import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        #init game window
        # init pygame and create window
        pg.init()
        # init sound mixer
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("jumpy")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
    def new(self):
        self.score = 0
        # add all sprites to the pg group
        self.all_sprites = pg.sprite.Group()
        # create platforms group
        self.platforms = pg.sprite.Group()
        # add a player 1 to the group
        self.player = Player(self)
        self.all_sprites.add(self.player)
        # instantiate new platform 
        
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
  
        # call the run method
        self.run()
    def run(self):
        # set boolean playing to true
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def update(self):
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                    self.player.pos.y = hits[0].rect.top + 1
                    self.player.vel.y = 0
                # scroll plats with player
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT + 40:
                    plat.kill()
                    self.score += 10
        # Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False       
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0,WIDTH-width), 
                            random.randrange(-75, -30),
                            width,
                            20
                        )
            self.platforms.add(p)
            self.all_sprites.add(p)
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # double buffering - renders a frame "behind" the displayed frame
        pg.display.flip()
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type ==pg.KEYUP:
                    waiting = False
    def show_start_screen(self):
        # game splash screen
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game splash screen
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        pg.display.flip()
        self.wait_for_key()

    def draw_text(self, text, size, color, x, y,):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()

g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()