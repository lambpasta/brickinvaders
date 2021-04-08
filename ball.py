import pygame
import os
from math import sin, cos, radians
from random import randrange
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE


balls = pygame.sprite.Group()
immortal = False

class Ball(pygame.sprite.Sprite):

    def __init__(self, xcenter, y, size, velocity, angle):
        super().__init__()

        self.size = size

        og_image = pygame.image.load("assets/ball.png").convert_alpha()
        self.image = pygame.transform.scale(og_image, (self.size, self.size))
        self.rect = self.image.get_rect()


        self.realx = xcenter - (self.size/2)
        self.realy = y
        self.rect.x = int(self.realx)
        self.rect.y = int(self.realy)

        self.velocity = velocity
        self.angle = randrange(0, 900)/10+45

    
    def move(self, xchange, ychange):
        self.realx += xchange
        self.realy += ychange
        self.rect.x = int(self.realx)
        self.rect.y = int(self.realy)

    def addball(xcenter, ycenter, size):
        balls.add(Ball(xcenter, ycenter, size, 0, randrange(0, 900)/10+45))

    def setallballs(param, value):
        for ball in balls:
            if param == "realx":
                ball.realx = value
            if param == "realy":
                ball.realy = value
            if param == "velocity":
                ball.velocity = value
            if param == "angle":
                ball.angle = value
            if param == "size":
                ball.size = value

    def xcenter(self):
        return self.rect.x + (self.size/2)

    def ycenter(self):
        return self.rect.y + (self.size/2)

    def getx(self, angle):
        return cos(radians(self.angle))*self.velocity

    def gety(self, angle):
        return sin(radians(self.angle))*self.velocity*-1

    def verticalbounce(self):
        self.angle = (90 - self.angle) + 90

    def horizontalbounce(self):
        self.angle = (180 - self.angle) + 180
    
    def update(self, platform, platforms, enemies, hasmoved):

        if hasmoved: 
            self.velocity = 10

        if ((self.rect.x + self.size) >= SCREEN_WIDTH) or ((self.rect.x) <= 0):
            self.verticalbounce()

        if ((self.rect.y) < 0):
            self.horizontalbounce()
        
        self.move(self.getx(self.angle), self.gety(self.angle))

        if pygame.sprite.spritecollide(self, platforms, False):
            self.horizontalbounce()
            ballpospercent = ((self.xcenter() - platform.rect.x)/platform.length)*100
            self.angle -= (ballpospercent - 50)/3

        
        enemies_hit = pygame.sprite.spritecollide(self, enemies, False)

        # if len(enemies_hit) > 0:
        #     balls.add(Ball(self.xcenter(), self.ycenter(), self.size, 10, randrange(0, 900)/10+45))
        #     print("addingball")

        for enemy in enemies_hit:
            if abs(self.xcenter() - enemy.xcenter()) < abs(self.ycenter() - enemy.ycenter()):
                self.horizontalbounce()
            else:
                self.verticalbounce()
            enemies.remove(enemy)

        for ball in balls:
            if ball.rect.y > SCREEN_HEIGHT:
                balls.remove(ball)

    