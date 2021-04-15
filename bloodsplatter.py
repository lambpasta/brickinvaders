import pygame
import os
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE
from random import randint
from math import cos, sin, radians

blood = pygame.sprite.Group()

def splatter(count, centerx, centery):
    for i in range(count):
        blood.add(Bloodsplatter(centerx, centery))


class Bloodsplatter(pygame.sprite.Sprite):
    def __init__(self, xcenter, ycenter):
        super().__init__()

        og_blood = pygame.image.load("assets/blood.png")
        self.image = pygame.transform.scale(og_blood, (randint(5, 20), randint(5, 20)))
        self.rect = self.image.get_rect()

        self.rect.centerx = xcenter
        self.rect.centery = ycenter

        self.realw = self.rect.w
        self.realh = self.rect.h

        self.angle = randint(1, 361)

        self.velocity = 2

    def getx(self, angle):
        return cos(radians(self.angle))*self.velocity

    def gety(self, angle):
        return sin(radians(self.angle))*self.velocity*-1

    def update(self):
        self.rect.centerx += self.getx(self.angle)
        self.rect.centery += self.gety(self.angle)
        self.realw -= 0.7
        self.realh -= 0.7
        self.rect.h = round(self.realh)
        self.rect.w = round(self.realw)
        if self.rect.w <= 0 or self.rect.h <= 0:
            blood.remove(self)