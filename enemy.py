import pygame
import os
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE
from math import floor, sqrt, atan, degrees
from random import random

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

def addenemy(x, y, size):
    enemies.add(Enemy(x, y, size))

def spawnenemies(count, size, xspacing, yspacing):
    enemyxspacing = xspacing + size
    enemyyspacing = yspacing + size
    enemycontainer = SCREEN_WIDTH - size
    for i in range(count):
        x = ((enemyxspacing)*i) % enemycontainer
        y = (enemyyspacing)*(1 + floor((enemyxspacing)*i/enemycontainer))
        addenemy(x, y, size)



class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, size):
        super().__init__()

        self.size = size

        og_image = pygame.image.load("assets/enemy2.png").convert_alpha()
        self.image = pygame.transform.scale(og_image, (self.size, self.size))
        self.rect = self.image.get_rect()


        self.realx = x
        self.realy = y
        self.rect.x = int(self.realx)
        self.rect.y = int(self.realy)
    
    def move(self, xchange, ychange):
        self.realx += xchange
        self.realy += ychange
        self.rect.x = int(self.realx)
        self.rect.y = int(self.realy)

    def shoot(self, platform):
        xdiff = platform.rect.centerx - self.rect.x
        ydiff = platform.rect.centery - self.rect.y

        # a^2 + b^2 = c^2

        # a is x, b is y

        # let x represent a/b

        # solve for b because y is always positive

        # n = x**2 + 1
        # b = (c * sqrt(n))/n

        c = 3 # velocity of bullet

        x = xdiff/ydiff
        n = x**2 + 1
        b = (c * sqrt(n))/n

        angle = degrees(atan(x))

        bullets.add(Bullet(self.rect.centerx, self.rect.bottom, x*b, b, angle))

    def update(self, platform):
        if random() > 0.9996:
            self.shoot(platform)




class Bullet(pygame.sprite.Sprite):
    def __init__(self, xcenter, y, xchange, ychange, angle):
        super().__init__()

        og_bullet = pygame.image.load("assets/bullet.png").convert_alpha()
        self.image = pygame.transform.rotate(pygame.transform.scale(og_bullet, (10, 20)), angle)
        self.rect = self.image.get_rect()

        self.realxcenter = xcenter
        self.realy = y

        self.rect.centerx = self.realxcenter
        self.rect.y = self.realy

        self.xchange = xchange
        self.ychange = ychange

    def update(self, platform):
        self.realxcenter += self.xchange
        self.realy += self.ychange

        self.rect.centerx = round(self.realxcenter)
        self.rect.y = round(self.realy)

        if self.rect.y >= SCREEN_HEIGHT:
            bullets.remove(self)

        if pygame.sprite.spritecollide(platform, bullets, True):
            platform.lenset(platform.rect.w - 20)