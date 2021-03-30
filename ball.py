import pygame
import os
from math import sin, cos, radians
from random import randrange
from platform import Platform
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE

balls = pygame.sprite.Group()
immortal = False

class Ball(pygame.sprite.Sprite):

    def __init__(self, xcenter, size):
        super().__init__()

        self.size = size

        og_image = pygame.image.load("assets/ball.png").convert_alpha()
        self.image = pygame.transform.scale(og_image, (self.size, self.size))
        self.rect = self.image.get_rect()


        self.realx = xcenter - (self.size/2)
        self.realy = 628 - self.size
        self.rect.x = int(self.realx)
        self.rect.y = int(self.realy)

        self.velocity = 0
        self.angle = randrange(0, 90)+45

    
    def move(self, xchange, ychange):
        self.realx += xchange
        self.realy += ychange
        self.rect.x = int(self.realx)
        self.rect.y = int(self.realy)

    def xcenter(self):
        return self.rect.x + (self.size/2)

    def getx(self, angle):
        return cos(radians(self.angle))*self.velocity

    def gety(self, angle):
        return sin(radians(self.angle))*self.velocity*-1
    
    def update(self, platform, platforms):
        if ((self.rect.x + self.size) >= SCREEN_WIDTH) or ((self.rect.x) <= 0):
            self.angle = (90 - self.angle) + 90

        if ((self.rect.y) < 0):
            self.angle = (180 - self.angle) + 180
        
        self.move(self.getx(self.angle), self.gety(self.angle))

        if pygame.sprite.spritecollide(self, platforms, False):
            self.angle = (180 - self.angle) + 180
            ballpospercent = ((self.xcenter() - platform.rect.x)/platform.length)*100
            self.angle -= (ballpospercent - 50)/3

        for ball in balls:
            if ball.rect.y > SCREEN_HEIGHT:
                balls.remove(ball)

    