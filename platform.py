import pygame
import os
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE

class Platform(pygame.sprite.Sprite):

    def __init__(self, xcenter, y):
        super().__init__()

        self.defaultw = 150
        self.width = self.defaultw
        self.activeheight = round(self.width/92*9)

        # image size 92 x 9#
        # platform width 78 (centered)


        self.PFnonenone = pygame.image.load("assets/platform/PFnonenone.png").convert_alpha()
        self.PFnonehalf = pygame.image.load("assets/platform/PFnonehalf.png").convert_alpha()
        self.PFnonefull = pygame.image.load("assets/platform/PFnonefull.png").convert_alpha()
        self.currentimg = self.PFnonenone
        self.image = pygame.transform.scale(self.currentimg, (self.width, self.activeheight))
        self.rect = self.image.get_rect()

        self.rect.centerx = xcenter
        self.rect.y = y

        self.maxspd = 5
        self.speed = 0

        self.accel = 0.5
        self.hasmoved = False

        self.growcooldown = 0
        self.speedcooldown = 0

    def move(self, xchange, ychange):
        self.rect.x += xchange
        self.rect.y += ychange

    def runmovement(self):

        keys_pressed = pygame.key.get_pressed()

        self.hasmoved = False
        # if not left and right keys at once
        if not ((keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d])):
            # if leftwards inputs
            if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
                # accelerate to the left
                self.speed = max(-1*self.maxspd, self.speed - self.accel)
                self.hasmoved = True
            # if rightwards inputs
            if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
                # accelerate to the right
                self.speed = min(self.maxspd, self.speed + self.accel)
                self.hasmoved = True

        if not self.hasmoved:
            if self.speed != 0:
                if self.speed < 0:
                    self.speed += self.accel
                else:
                    self.speed -= self.accel
        if self.rect.x > 0 and self.speed < 0:
            self.move(self.speed, 0)
        if self.rect.x + self.rect.width < SCREEN_WIDTH and self.speed > 0:
            self.move(self.speed, 0) 

    def lenset(self, width):
        self.width = width
        self.activeheight = max(round(width/92*9), 15)
        tempxcenter = self.rect.centerx
        self.image = pygame.transform.scale(self.currentimg, (width, self.activeheight))
        self.rect.h = self.image.get_height()
        self.rect.w = self.image.get_width()
        self.rect.centerx = tempxcenter

    def reset(self):
        self.width = self.defaultw
        self.rect.centerx = 500
        self.rect.y = 630
        self.maxspd = 5
        self.speed = 0
        self.lenset(self.width)
        self.growcooldown = 0
        self.speedcooldown = 0

    def checkcooldowns(self):
        if self.growcooldown > 0:
            self.growcooldown -= 1
            if self.growcooldown == 0:
                self.lenset(self.width)
        if self.speedcooldown > 0:
            self.speedcooldown -= 1
            if self.speedcooldown == 0:
                self.accel = 0.5
                self.maxspd = 5
                self.speed = 0

    def setblasters(self):

        if self.speed != 0:

            if self.speed == self.maxspd:
                self.currentimg = pygame.transform.flip(self.PFnonefull, True, False)
            elif self.speed*-1 == self.maxspd:
                self.currentimg = self.PFnonefull

            elif self.speed > 0:
                self.currentimg = pygame.transform.flip(self.PFnonehalf, True, False)
            else:
                self.currentimg = self.PFnonehalf

        else:
            self.currentimg = self.PFnonenone

        self.image = pygame.transform.scale(self.currentimg, (self.rect.width, self.activeheight))

    def update(self):

        self.checkcooldowns()
        
        keys_pressed = pygame.key.get_pressed()
        
        self.runmovement()

        self.setblasters()