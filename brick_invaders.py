import sys
import os
import pygame
from ball import Ball, balls, immortal, spawnballs
from platform import Platform
from powerup import Powerup, powerups
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE
from enemy import enemies, Enemy, spawnenemies
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

og_speedfade = pygame.image.load("assets/speedfade.png")
speedfade = pygame.transform.scale(og_speedfade, (SCREEN_WIDTH, 70))

youdied = pygame.image.load("assets/youdied.png")
youdiedscaled = pygame.transform.scale(youdied, (SCREEN_WIDTH, SCREEN_HEIGHT))

# create the platform object and add it to a group for convenience
platform = Platform(500, 630)
platforms = pygame.sprite.Group()
platforms.add(platform)


# spawn and layout all enemies
spawnenemies(50, 50, 10, 10)

# spawn and layout all balls
ballcount = 1
ballsize = 30
ballspawny = 630 - (ballsize/2)
spawnballs(ballcount, platform.rect.centerx, ballspawny, ballsize, 0, randrange(0, 900)/10+45)

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
        spawnballs(ballcount, platform.rect.centerx, ballspawny, ballsize, 0, randrange(0, 900)/10+45)


    """
    UPDATE section - manipulate everything on the screen
    """

    platform.update()
    balls.update(platform, platforms, enemies, platform.hasmoved, Powerup)
    powerups.update(platforms, balls)

    """
    DRAW section - make everything show up on screen
    """
    screen.blit(bg, (0, 0))
    
    if platform.speedcooldown > 0:
        screen.blit(speedfade, (0, 605))
    
    enemies.draw(screen)
    balls.draw(screen)
    platforms.draw(screen)
    powerups.draw(screen)


    if len(balls) < 1:
        screen.blit(youdiedscaled, (0, 0))
    pygame.display.flip()  # Pygame uses a double-buffer, without this we see half-completed frames
    clock.tick(FRAME_RATE)  # Pause the clock to always maintain FRAME_RATE frames per second