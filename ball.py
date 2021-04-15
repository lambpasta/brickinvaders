import pygame
import os
from math import sin, cos, radians
from random import randrange, random
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE
from bloodsplatter import splatter

balls = pygame.sprite.Group()

pygame.init()

splat = pygame.mixer.Sound('assets/splat.wav')

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

    def verticalbounce(self):
        self.angle = (90 - self.angle) + 90

    def horizontalbounce(self):
        self.angle = (180 - self.angle) + 180
    
    def multiball(self):
        self.selfspawnballs(2, self.rect.x, self.rect.y, self.size, 5, randrange(0, 900)/10+45)

    def correctangles(self):
        self.angle = self.angle % 360
        if round(self.angle, 3) % 90 == 0:
            self.angle += 5

    def bounceonedges(self):
        if ((self.rect.x + self.size) >= SCREEN_WIDTH):
            self.rect.right = SCREEN_WIDTH + 1
            self.verticalbounce()
        elif ((self.rect.x) <= 0):
            self.rect.x = 1
            self.verticalbounce()
        if ((self.rect.y) < 0):
            self.rect.y = 1
            self.horizontalbounce()
            if 0 >= self.angle >= 360:
                print(ball)


    def updatepowers(self):
        if self.firecooldown > 0:
            self.firecooldown -= 1
            self.image = pygame.transform.scale(self.og_powerball, (self.size, self.size))
        else:
            self.image = pygame.transform.scale(self.og_ball, (self.size, self.size))

    def collidewplatform(self, platform):
        if pygame.sprite.collide_rect(self, platform):

            if platform.rect.top < (self.rect.bottom - self.gety(self.angle)):
                self.verticalbounce()
            else:
                self.horizontalbounce()


            ballpospercent = ((self.rect.centerx - platform.rect.x)/platform.rect.width)*100
            self.angle -= (ballpospercent - 50)/3 % 360

    def collidewenemies(self, enemies, Powerup):
        
        enemies_hit = pygame.sprite.spritecollide(self, enemies, True)

        for enemy in enemies_hit:
            if random() >= 0.85:
                Powerup.addpowerup(enemy.rect.x, enemy.rect.y, 40, randrange(1, 5))
            splatter(30, enemy.rect.centerx, enemy.rect.centery)

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


    def update(self, platform, enemies, Powerup, immortal):

        if self.rect.y > SCREEN_HEIGHT:
            if not immortal:
                balls.remove(self)
            else:
                self.rect.bottom = SCREEN_HEIGHT
                self.horizontalbounce()

        self.updatepowers()

        self.move(self.getx(self.angle), self.gety(self.angle))

        if platform.hasmoved: 
            self.velocity = 5

        self.bounceonedges()

        self.collidewplatform(platform)

        if self.velocity != 0 and pygame.sprite.spritecollide(self, enemies, False):
            self.collidewenemies(enemies, Powerup)
            splat.play()

        self.correctangles()