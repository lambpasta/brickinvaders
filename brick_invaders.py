import sys
import os
import pygame
from ball import Ball, balls, immortal
from platform import Platform
from globalvars import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE

"""
SETUP section - preparing everything before the main loop runs
"""
pygame.init()

# Creating the screen and the clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.set_alpha(0)  # Make alpha bits transparent
clock = pygame.time.Clock()

platform = Platform(500, 630)
platforms = pygame.sprite.Group()
platforms.add(platform)

platform.reset()

click = pygame.mixer.Sound('assets/click.ogg')

og_bg = pygame.image.load("assets/background2.png")
bg = pygame.transform.scale(og_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

youdied = pygame.image.load("assets/youdied.png")
youdiedscaled = pygame.transform.scale(youdied, (SCREEN_WIDTH, SCREEN_HEIGHT))

def addball(xcenter, size):
    balls.add(Ball(xcenter, size))

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

for i in range(100):
    addball(platform.xcenter(), 20)

while True:
    """
    EVENTS section - how the code reacts when users do things
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # When user clicks the 'x' on the window, close our game
            pygame.quit()
            sys.exit()

    keys_pressed = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mousex = mouse_pos[0]
    mousey = mouse_pos[1]
    mouse_buttons = pygame.mouse.get_pressed()

    #move the platform
    hasmoved = False
    if not ((keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d])):
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            platform.speed = max(-1*platform.maxspd, platform.speed - platform.accel)
            setallballs("velocity", 10)
            hasmoved = True
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:

            platform.speed = min(platform.maxspd, platform.speed + platform.accel)
            setallballs("velocity", 10)
            hasmoved = True
    if not hasmoved:
        if platform.speed != 0:
            if platform.speed < 0:
                platform.speed += platform.accel
            else:
                platform.speed -= platform.accel
    if platform.rect.x > 0 and platform.speed < 0:
        platform.move(platform.speed, 0)
    if platform.rect.x + platform.length < SCREEN_WIDTH and platform.speed > 0:
        platform.move(platform.speed, 0)

    #respawn button
    if len(balls) < 1 and (184 <= mousex <= 820) and (360 <= mousey <= 424) and mouse_buttons[0]:
        platform.reset()
        click.play()
        for i in range(100):
            addball(platform.xcenter(), 20)


    """
    UPDATE section - manipulate everything on the screen
    """

    balls.update(platform, platforms)

    """
    DRAW section - make everything show up on screen
    """
    screen.blit(bg, (0, 0))

    if len(balls) < 1:
        screen.blit(youdiedscaled, (0, 0))

    balls.draw(screen)
    platforms.draw(screen)

    pygame.display.flip()  # Pygame uses a double-buffer, without this we see half-completed frames
    clock.tick(FRAME_RATE)  # Pause the clock to always maintain FRAME_RATE frames per second