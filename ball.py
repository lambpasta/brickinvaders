import pygame
import os
from math import sin, cos, radians
from random import randrange, random
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE

balls = pygame.sprite.Group()
immortal = False

def spawnballs(count, x, y, size, velocity, angle):
    for i in range(count):
        balls.add(Ball(x, y, size, velocity, angle))

def overlap(a, b):
    return a[0] <= b[0] <= a[1] or b[0] <= a[0] <= b[1]

class Ball(pygame.sprite.Sprite):

    def __init__(self, xcenter, ycenter, size, velocity, angle):
        super().__init__()

        self.size = size

        self.og_ball = pygame.image.load("assets/ball.png").convert_alpha()
        self.og_powerball = pygame.image.load("assets/powerball.png").convert_alpha()
        self.image = pygame.transform.scale(self.og_ball, (self.size, self.size))
        self.rect = self.image.get_rect()


        self.realx = xcenter - (self.size/2)
        self.realy = ycenter - (self.size/2)
        self.rect.x = int(self.realx)
        self.rect.y = int(self.realy)

        self.velocity = velocity
        self.angle = randrange(0, 900)/10+45

        self.firecooldown = 0
    
    def move(self, xchange, ychange):
        self.realx += xchange
        self.realy += ychange
        self.rect.x = int(self.realx)
        self.rect.y = int(self.realy)

    def selfspawnballs(self, count, x, y, size, velocity, angle):
        for i in range(count):
            balls.add(Ball(x, y, size, velocity, angle))

    def resetballs(self):
        for ball in balls:
            ball.realx = 500 - (ball.size/2)
            ball.realy = 628 - ball.size
            ball.velocity = 0
            ball.angle = randrange(0, 90)+45
            ball.size = 20
            ball.firecooldown = 0

        def checkcooldowns(self):
            if self.firecooldown > 0:
                self.firecooldown -= 1


    def getx(self, angle):
        return cos(radians(self.angle))*self.velocity

    def gety(self, angle):
        return sin(radians(self.angle))*self.velocity*-1

    def getleadingcorner(self):
        if self.getx(self.angle) > 0:
            if self.gety(self.angle) > 0:
                # ball is going down and right
                return self.rect.bottomright
            elif self.gety(self.angle) < 0:
                # ball is going up and right
                return self.rect.topright
            else:
                # ball is going directly right
                self.verticalbounce()

        elif self.getx(self.angle) < 0:
            if self.gety(self.angle) > 0:
                # ball is going down and left
                return self.rect.bottomleft
            elif self.gety(self.angle) < 0:
                # ball is going up and left
                return self.rect.topleft
            else:
                # ball is going directly left
                self.verticalbounce()

        elif self.gety(self.angle) != 0:
            # ball is going directly up/down
            self.horizontalbounce()

    def verticalbounce(self):
        self.angle = (90 - self.angle) + 90

    def horizontalbounce(self):
        self.angle = (180 - self.angle) + 180
    
    def multiball(self):
        self.selfspawnballs(2, self.rect.x, self.rect.y, self.size, 5, randrange(0, 900)/10+45)

    def bounceonedges(self):
        if ((self.rect.x + self.size) >= SCREEN_WIDTH) or ((self.rect.x) <= 0):
            self.verticalbounce()
        if ((self.rect.y) < 0):
            self.horizontalbounce()

    def updatepowers(self):
        if self.firecooldown > 0:
            self.firecooldown -= 1
            self.image = pygame.transform.scale(self.og_powerball, (self.size, self.size))
        else:
            self.image = pygame.transform.scale(self.og_ball, (self.size, self.size))

    def collidewplatform(self, platforms, platform):
        if pygame.sprite.spritecollide(self, platforms, False):
            leadcorner = self.getleadingcorner()

            # get line leading corner of ball is travelling in slope-intercept form (y = mx + b)

            m = self.gety(self.angle) / self.getx(self.angle) # m = y/x
            b = int(leadcorner[1] - (m*leadcorner[0])) # b = y - mx

            # if going right
            if self.getx(self.angle) > 0:
                if platform.rect.top <= (m*(platform.rect.left) + b) <= platform.rect.bottom:
                    self.verticalbounce()
                else:
                    self.horizontalbounce()

            # if going left
            if self.getx(self.angle) < 0:
                if platform.rect.top <= (m*(platform.rect.right) + b) <= platform.rect.bottom:
                    self.verticalbounce()
                else:
                    self.horizontalbounce()
            if self.getx(self.angle) == 0:
                print('dumb game thinks ball isnt moving')

            ballpospercent = ((self.rect.centerx - platform.rect.x)/platform.rect.width)*100
            self.angle -= (ballpospercent - 50)/3

    def collidewenemies(self, enemies, Powerup):
        
        enemies_hit = pygame.sprite.spritecollide(self, enemies, True)

        for enemy in enemies_hit:
            if random() >= 0.85:
                Powerup.addpowerup(enemy.rect.x, enemy.rect.y, 40, randrange(1, 5))

        if len(enemies_hit) == 2:
            if enemies_hit[0].rect.x == enemies_hit[1].rect.x:
                if self.firecooldown <= 0:
                    self.verticalbounce()
            elif enemies_hit[0].rect.y == enemies_hit[1].rect.y:
                if self.firecooldown <= 0:
                    self.horizontalbounce()
            else:
                if self.firecooldown <= 0:
                    self.verticalbounce()
                    self.horizontalbounce()
        else:
            for enemy in enemies_hit:
                if abs(self.rect.centerx - enemy.rect.centerx) > abs(self.rect.centery - enemy.rect.centery):
                    if self.firecooldown <= 0:
                        self.verticalbounce()
                else:
                    if self.firecooldown <= 0:
                        self.horizontalbounce()


    def update(self, platform, platforms, enemies, hasmoved, Powerup):

        if self.rect.y > SCREEN_HEIGHT:
            balls.remove(self)

        self.updatepowers()

        self.move(self.getx(self.angle), self.gety(self.angle))

        if hasmoved: 
            self.velocity = 5

        self.bounceonedges()

        self.collidewplatform(platforms, platform)

        if self.velocity != 0 and pygame.sprite.spritecollide(self, enemies, False):
            self.collidewenemies(enemies, Powerup)