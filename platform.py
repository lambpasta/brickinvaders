import pygame
import os
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE

class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.defaultwidth = 150

        self.og_image = pygame.image.load("assets/platform.png").convert_alpha()
        self.image = pygame.transform.scale(self.og_image, (self.defaultwidth, 20))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.maxspd = 10
        self.speed = 0

        self.accel = 1
        self.hasmoved = False

        self.growcooldown = 0
        self.speedcooldown = 0
    
    def move(self, xchange, ychange):
        self.rect.x += xchange
        self.rect.y += ychange

    def xcenter(self):
        return self.rect.x + (self.rect.width/2)

    def lenset(self, length):
        tempxcenter = self.rect.centerx
        self.image = pygame.transform.scale(self.og_image, ((length), 20))
        self.rect.height = self.image.get_height()
        self.rect.width = self.image.get_width()
        self.rect.centerx = tempxcenter

    def reset(self):
        self.rect.x = 500 - (self.defaultwidth/2)
        self.rect.y = 630
        self.maxspd = 10
        self.speed = 0
        self.lenset(self.defaultwidth)
    
    def update(self, keys_pressed):
        

        if self.growcooldown > 0:
            self.growcooldown -= 1
            if self.growcooldown == 0:
                self.lenset(150)
        if self.speedcooldown > 0:
            self.speedcooldown -= 1
            if self.speedcooldown == 0:
                self.accel = 1
                self.speed /= 2
                self.maxspeed = 10
        
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