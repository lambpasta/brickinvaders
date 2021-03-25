import pygame
import os
import random

class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.length = 150

        self.og_image = pygame.image.load("assets/platform.png").convert_alpha()
        self.image = pygame.transform.scale(self.og_image, (self.length, 20))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.maxspd = 10
        self.speed = 0

        self.accel = 1
    
    def move(self, xchange, ychange):
        self.rect.x += xchange
        self.rect.y += ychange

    def xcenter(self):
        return self.rect.x + (self.length/2)

    def lenscale(self, lengthchange):
        self.length += lengthchange
        self.image = pygame.transform.scale(self.og_image, ((self.length), 20))
        self.rect.x += -1*(lengthchange/2)

    def reset(self):
        self.rect.x = 500 - (self.length/2)
        self.rect.y = 630
        self.length = 150
        self.maxspd = 10
        self.speed = 0