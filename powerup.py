import pygame
import os
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE

powerups = pygame.sprite.Group()

class Powerup(pygame.sprite.Sprite):

    def __init__(self, x, y, size):
        super().__init__()

        self.size = size

        og_mushroom = pygame.image.load("assets/mushroom.png").convert_alpha()
        self.image = pygame.transform.scale(og_mushroom, (self.size, self.size))
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
    
    def addpowerup(x, y, size):
        powerups.add(Powerup(x, y, size))

    def xcenter(self):
        return self.rect.x + (self.size/2)

    def ycenter(self):
        return self.rect.y + (self.size/2)

    def update(self, platforms):
        self.move(0, 3)
        if pygame.sprite.spritecollide(self, platforms, False):
            powerups.remove(self)
            for platform in platforms:
                platform.lenscale(30)