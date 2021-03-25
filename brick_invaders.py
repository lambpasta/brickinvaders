import sys
import os
import pygame
from ball import Ball
from platform import Platform

"""
SETUP section - preparing everything before the main loop runs
"""
pygame.init()

# Global constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FRAME_RATE = 120

# Useful colors 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Creating the screen and the clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.set_alpha(0)  # Make alpha bits transparent
clock = pygame.time.Clock()

ball = Ball(500, 400, 20)
balls = pygame.sprite.Group()
balls.add(ball)

platform = Platform(500, 630)
platforms = pygame.sprite.Group()
platforms.add(platform)

click = pygame.mixer.Sound('assets/click.ogg')

og_bg = pygame.image.load("assets/background2.png")
bg = pygame.transform.scale(og_bg, (1000, 700))

youdied = pygame.image.load("assets/youdied.png")
youdiedscaled = pygame.transform.scale(youdied, (1000, 700))

dead = False

score = 0

platform.reset()
ball.reset(platform.xcenter())

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
            ball.velocity = 10
            hasmoved = True
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:

            platform.speed = min(platform.maxspd, platform.speed + platform.accel)
            ball.velocity = 10
            hasmoved = True
    if not hasmoved:
        if platform.speed != 0:
            if platform.speed < 0:
                platform.speed += platform.accel
            else:
                platform.speed -= platform.accel
    if platform.rect.x > 0 and platform.speed < 0:
        platform.move(platform.speed, 0)
    if platform.rect.x + platform.length < 1000 and platform.speed > 0:
        platform.move(platform.speed, 0)

    #respawn button
    if dead and (184 <= mousex <= 820) and (360 <= mousey <= 424) and mouse_buttons[0]:
        platform.reset()
        ball.reset(platform.xcenter())
        click.play()
        dead = False

    """
    UPDATE section - manipulate everything on the screen
    """

    if ball.rect.y >= 700:
        dead = True

    balls.update()

    if pygame.sprite.spritecollide(platform, balls, False):

        ball.angle = (180 - ball.angle) + 180
        ballpospercent = ((ball.xcenter() - platform.rect.x)/platform.length)*100
        ball.angle -= (ballpospercent - 50)/3

    """
    DRAW section - make everything show up on screen
    """
    screen.blit(bg, (0, 0))

    if dead:
        screen.blit(youdiedscaled, (0, 0))

    balls.draw(screen)
    platforms.draw(screen)

    pygame.display.flip()  # Pygame uses a double-buffer, without this we see half-completed frames
    clock.tick(FRAME_RATE)  # Pause the clock to always maintain FRAME_RATE frames per second