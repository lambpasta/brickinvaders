import pygame
import os
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE
from math import floor

enemies = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, size):
        super().__init__()

        self.size = size

        og_image = pygame.image.load("assets/enemy.png").convert_alpha()
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

    def addenemy(x, y, size):
        enemies.add(Enemy(x, y, size))

    def spawnenemies(count, size, xspacing, yspacing):
        enemyxspacing = xspacing + size
        enemyyspacing = yspacing + size
        enemycontainer = SCREEN_WIDTH - size
        for i in range(count):
            x = ((enemyxspacing)*i) % enemycontainer
            y = (enemyyspacing)*(1 + floor((enemyxspacing)*i/enemycontainer))
            Enemy.addenemy(x, y, size)

    def xcenter(self):
        return self.rect.x + (self.size/2)

    def ycenter(self):
        return self.rect.y + (self.size/2)
