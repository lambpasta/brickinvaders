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

    def verticalbounce(self):
        self.angle = (90 - self.angle) + 90

    def horizontalbounce(self):
        self.angle = (180 - self.angle) + 180
    
    def multiball(self):
        self.selfspawnballs(2, self.rect.x, self.rect.y, self.size, 10, randrange(0, 900)/10+45)

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

            
            self.rect.bottom = platform.rect.top
            self.horizontalbounce()

            ballpospercent = ((self.rect.centerx - platform.rect.x)/platform.rect.width)*100
            self.angle -= (ballpospercent - 50)/3

    def collidewenemies(self, enemies, Powerup):
        
        enemies_hit = pygame.sprite.spritecollide(self, enemies, True)

        for enemy in enemies_hit:
            if random() >= 0.85:
                Powerup.addpowerup(enemy.rect.x, enemy.rect.y, 40, randrange(1, 5))

        if self.firecooldown <= 0:
            if len(enemies_hit) == 2:
                if enemies_hit[0].rect.x == enemies_hit[1].rect.x:
                    self.verticalbounce()
                elif enemies_hit[0].rect.y == enemies_hit[1].rect.y:
                    self.horizontalbounce()
                else:
                    self.horizontalbounce()
                    self.verticalbounce()

            elif self.velocity != 0 and enemies_hit:
                
                xchange = self.getx(self.angle)
                ychange = self.gety(self.angle)

                slope = ychange/xchange

                if ychange > 0:
                    for enemy in enemies_hit:

                        xonedge = ((enemy.rect.top/slope), (enemy.rect.top/slope) + self.size)
                        enemyxrange = (enemy.rect.left, enemy.rect.right)
                        
                        if overlap(xonedge, enemyxrange):
                            self.verticalbounce()
                        else:
                            self.horizontalbounce()

                elif ychange < 0:
                    for enemy in enemies_hit:

                        xonedge = ((enemy.rect.bottom/slope), (enemy.rect.bottom/slope) + self.size)
                        enemyxrange = (enemy.rect.left, enemy.rect.right)
                        
                        if overlap(xonedge, enemyxrange):
                            self.verticalbounce()
                        else:
                            self.horizontalbounce()

                else:
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

        self.collidewenemies(enemies, Powerup)