# sprite classes for game

import pygame as pg
from pygame.sprite import Sprite
import random
from settings import *

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((30,40))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT /2)
        self.vx = 0
        self.vy = 0
        self.falling = False
    def update(self):
        self.vx = 0
        # self.vy = 0
        self.gravity()
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vx = -5
        if keys[pg.K_d]:
            self.vx = 5
        if keys[pg.K_w] and self.falling == False:
            self.jump()
        self.rect.x += self.vx
        self.rect.y += self.vy
    def gravity(self):
        if self.rect.y < HEIGHT-40:
            self.falling = True
            self.vy += 10
        elif self.rect.y >= HEIGHT:
            self.falling = False
            self.vy = 0
            self.rect.y = HEIGHT-40
    def jump(self):
        self.vy = -75