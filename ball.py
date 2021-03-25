import pygame
import os
from math import sin
from math import cos
from math import radians
from random import random
from platform import Platform

class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y, size):
        super().__init__()

        self.size = size

        og_image = pygame.image.load("assets/ball.png").convert_alpha()
        self.image = pygame.transform.scale(og_image, (self.size, self.size))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.velocity = 8
        self.angle = 45
    
    def move(self, xchange, ychange):
        self.rect.x += xchange
        self.rect.y += ychange

    def xcenter(self):
        return self.rect.x + (self.size/2)

    def getx(self, angle):
        return cos(radians(self.angle))*self.velocity

    def gety(self, angle):
        return sin(radians(self.angle))*self.velocity*-1
    
    def update(self):
        if ((self.rect.x + self.size) >= 1000) or ((self.rect.x) <= 0):
            self.angle = (90 - self.angle) + 90

        if ((self.rect.y) < 0):
            self.angle = (180 - self.angle) + 180
        
        self.move(self.getx(self.angle), self.gety(self.angle))

    def reset(self, xpos):
        self.rect.x = xpos - (self.size/2)
        self.rect.y = 628 - self.size
        self.velocity = 0
        self.angle = random()*90+45

    