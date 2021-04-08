import sys
import os
import pygame
from ball import Ball, balls, immortal
from platform import Platform
from powerup import Powerup
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE
from enemy import enemies, Enemy
from math import floor
from random import randrange

"""
SETUP section - preparing everything before the main loop runs
"""
pygame.init()

# create the screen and the clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.set_alpha(0)  # make alpha bits transparent
clock = pygame.time.Clock()

# load & scale assets
click = pygame.mixer.Sound('assets/click.ogg')

og_bg = pygame.image.load("assets/background2.png")
bg = pygame.transform.scale(og_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

youdied = pygame.image.load("assets/youdied.png")
youdiedscaled = pygame.transform.scale(youdied, (SCREEN_WIDTH, SCREEN_HEIGHT))

# define useful functions for the game
def addball(xcenter, ycenter, size):
    balls.add(Ball(xcenter, ycenter, size, 0, randrange(0, 900)/10+45))

def addpowerup(x, y, size):
    enemies.add(Powerup(x, y, size))

def addenemy(x, y, size):
    enemies.add(Enemy(x, y, size))

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

def resetballs():
    for ball in balls:
        ball.realx = 500 - (ball.size/2)
        ball.realy = 628 - ball.size
        ball.velocity = 0
        ball.angle = random()*90+45
        ball.size = 20

# create the platform object and add it to a group for convenience
platform = Platform(500, 630)
platforms = pygame.sprite.Group()
platforms.add(platform)

# reset platform attributes
platform.reset()

# spawn and layout all enemies
enemycount = 100
enemysize = 50
enemyxspacing = 10 + enemysize
enemyyspacing = 10 + enemysize
enemycontainer = SCREEN_WIDTH - enemysize
for i in range(enemycount):
    x = ((enemyxspacing)*i) % enemycontainer
    y = (enemyyspacing)*(1 + floor((enemyxspacing)*i/enemycontainer))
    addenemy(x, y, enemysize)

# spawn and layout all balls
ballcount = 1
ballsize = 20
for i in range(ballcount):
    addball(platform.xcenter(), 628 - ballsize, ballsize)



# main game loop
while True:
    """
    EVENTS section - how the code reacts when users do things
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # when user clicks the 'x' on the window, close the game
            pygame.quit()
            sys.exit()

    # get user inputs
    keys_pressed = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mousex = mouse_pos[0]
    mousey = mouse_pos[1]
    mouse_buttons = pygame.mouse.get_pressed()

    # respawn button
    if len(balls) < 1 and (184 <= mousex <= 820) and (360 <= mousey <= 424) and mouse_buttons[0]:
        platform.reset()
        click.play()
        for i in range(ballcount):
            addball(platform.xcenter(), 628 - ballsize, ballsize)


    """
    UPDATE section - manipulate everything on the screen
    """

    platform.update(keys_pressed)
    balls.update(platform, platforms, enemies, platform.hasmoved)

    """
    DRAW section - make everything show up on screen
    """
    screen.blit(bg, (0, 0))

    enemies.draw(screen)
    balls.draw(screen)
    platforms.draw(screen)

    if len(balls) < 1:
        screen.blit(youdiedscaled, (0, 0))
    pygame.display.flip()  # Pygame uses a double-buffer, without this we see half-completed frames
    clock.tick(FRAME_RATE)  # Pause the clock to always maintain FRAME_RATE frames per second