import pygame
import os
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE

powerups = pygame.sprite.Group()

class Powerup(pygame.sprite.Sprite):

    def __init__(self, x, y, size, power):
        super().__init__()

        self.size = size


        # POWER VALUES:
        # 1 = grow mushroom
        # 2 = fast platform
        # 3 = multiball
        self.power = power

        if self.power == 1:
            og_mushroom = pygame.image.load("assets/mushroom.png").convert_alpha()
            self.image = pygame.transform.scale(og_mushroom, (self.size, self.size))
            self.rect = self.image.get_rect()      
        if self.power == 2:
            og_swiftness = pygame.image.load("assets/swiftness.png").convert_alpha()
            self.image = pygame.transform.scale(og_swiftness, (self.size, self.size))
            self.rect = self.image.get_rect()
        if self.power == 3:
            og_multiball = pygame.image.load("assets/multiball.png").convert_alpha()
            self.image = pygame.transform.scale(og_multiball, (self.size, self.size))
            self.rect = self.image.get_rect()
        if self.power == 4:
            og_fireflower = pygame.image.load("assets/fireflower.png").convert_alpha()
            self.image = pygame.transform.scale(og_fireflower, (self.size, self.size))
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
    
    def addpowerup(x, y, size, power):
        powerups.add(Powerup(x, y, size, power))

    def xcenter(self):
        return self.rect.x + (self.size/2)

    def ycenter(self):
        return self.rect.y + (self.size/2)
    
    def dopower(self, platforms, balls):
        if self.power == 1:
            for platform in platforms:
                platform.lenset(200)
                platform.growcooldown = 2000
        elif self.power == 2:
            for platform in platforms:
                platform.maxspd = 8
                platform.accel = 1
                platform.speedcooldown = 2000
        elif self.power == 3:
            for ball in balls:
                ball.multiball()
        elif self.power == 4:
            for ball in balls:
                ball.firecooldown = 800

    def update(self, platforms, balls):
        self.move(0, 2)
        if pygame.sprite.spritecollide(self, platforms, False):
            self.dopower(platforms, balls)
            powerups.remove(self)