import os
import sys
import pygame
from math import floor, sin, cos, atan, sqrt, degrees, radians
from random import randrange, random, randint
from time import sleep

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FRAME_RATE = 100

lives = 3
immortal = False
dead = False
victorywave = 0

ballcount = 1
ballsize = 30
ballspawny = 630 - (ballsize/2)

pygame.init()

# create the screen and the clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.set_alpha(0)  # make alpha bits transparent
clock = pygame.time.Clock()

# load & scale assets
neogauge = pygame.mixer.music.load('assets/neogauge.mp3')

click = pygame.mixer.Sound('assets/click.ogg')

splat = pygame.mixer.Sound('assets/splat.wav')

og_bg = pygame.image.load("assets/background2.png")
bg = pygame.transform.scale(og_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

og_speedfade = pygame.image.load("assets/speedfade.png")
speedfade = pygame.transform.scale(og_speedfade, (SCREEN_WIDTH, 70))

youdied = pygame.image.load("assets/youdied.png")
youdiedscaled = pygame.transform.scale(youdied, (SCREEN_WIDTH, SCREEN_HEIGHT))

youlose = pygame.image.load("assets/youlose.jpg")
youlosescaled = pygame.transform.scale(youlose, (SCREEN_WIDTH, SCREEN_HEIGHT))

loading = pygame.image.load("assets/loading.gif")
loadingscaled = pygame.transform.scale(loading, (SCREEN_WIDTH, SCREEN_HEIGHT))

title = pygame.image.load("assets/title.png")
titlescaled = pygame.transform.scale(title, (SCREEN_WIDTH, SCREEN_HEIGHT))

victory = pygame.image.load("assets/victory.png")
victoryscaled = pygame.transform.scale(victory, (960, 540))

instructions = pygame.image.load("assets/instructions.png")
instructionsscaled = pygame.transform.scale(instructions, (SCREEN_WIDTH, SCREEN_HEIGHT))

heart = pygame.image.load("assets/heart.png")
heartscaled = pygame.transform.scale(heart, (30, 30))

# create sprite groups
platforms = pygame.sprite.Group()
balls = pygame.sprite.Group()
powerups = pygame.sprite.Group()
enemies = pygame.sprite.Group()
blood = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# declare functions
def addenemy(x, y, size):
    enemies.add(Enemy(x, y, size))

def spawnenemies(count, size, xspacing, yspacing):
    enemyxspacing = xspacing + size
    enemyyspacing = yspacing + size
    enemycontainer = SCREEN_WIDTH - (2*size)
    for i in range(count):
        x = ((enemyxspacing)*i) % enemycontainer
        y = (enemyyspacing)*(1 + floor((enemyxspacing)*i/enemycontainer))
        addenemy(x, y, size)

def spawnballs(count, x, y, size, velocity, angle):
    for i in range(count):
        balls.add(Ball(x, y, size, velocity, angle))

def splatter(count, centerx, centery):
    for i in range(count):
        blood.add(Bloodsplatter(centerx, centery))

# declare all classes (this is long - ends at line 554)
class Platform(pygame.sprite.Sprite):

    def __init__(self, xcenter, y):
        super().__init__()

        self.defaultw = 150
        self.width = self.defaultw
        self.activeheight = round(self.width/92*9)

        # image size 92 x 9
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

    def bounceonedges(self):
        if ((self.rect.x + self.size) >= SCREEN_WIDTH):
            self.rect.right = SCREEN_WIDTH + 1
            self.verticalbounce()
        elif ((self.rect.x) <= 0):
            self.rect.x = 1
            if 90 <= (self.angle % 360) <= 270:
                self.verticalbounce()
        if ((self.rect.y) < 0):
            self.rect.y = 1
            if 0 <= (self.angle % 360) <= 180:
                self.horizontalbounce()

    def updatepowers(self):
        if self.firecooldown > 0:
            self.firecooldown -= 1
            self.image = pygame.transform.scale(self.og_powerball, (self.size, self.size))
        else:
            self.image = pygame.transform.scale(self.og_ball, (self.size, self.size))

    def collidewplatform(self, platform):
        if pygame.sprite.collide_rect(self, platform):

            if platform.rect.top < (self.rect.bottom - self.gety(self.angle) - 1):
                self.verticalbounce()
            else:
                self.horizontalbounce()

            ballpospercent = ((self.rect.centerx - platform.rect.x)/platform.rect.width)*100
            self.angle -= (ballpospercent - 50)/3 - 360

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

class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, size):
        super().__init__()

        self.size = size

        og_image = pygame.image.load("assets/enemy2.png").convert_alpha()
        self.image = pygame.transform.scale(og_image, (self.size, self.size))
        self.rect = self.image.get_rect()


        self.realx = x
        self.realy = y
        self.rect.x = int(self.realx)
        self.rect.y = int(self.realy)

        self.movecycle = 0

    def shoot(self, platform):
        xdiff = platform.rect.centerx - self.rect.x
        ydiff = platform.rect.centery - self.rect.y

        # a^2 + b^2 = c^2

        # a is x, b is y

        # let x represent a/b

        # solve for b because y is always positive

        # n = x**2 + 1
        # b = (c * sqrt(n))/n

        c = 3 # velocity of bullet

        x = xdiff/ydiff
        n = x**2 + 1
        b = (c * sqrt(n))/n

        angle = degrees(atan(x))

        bullets.add(Bullet(self.rect.centerx, self.rect.bottom, x*b, b, angle))

    def update(self, platform):
        shootprobability = 0.015/len(enemies)
        if random() < shootprobability:
            self.shoot(platform)
        self.rect.x = self.realx + self.size + 20*sin(self.movecycle)
        self.movecycle += 0.03

class Bullet(pygame.sprite.Sprite):
    def __init__(self, xcenter, y, xchange, ychange, angle):
        super().__init__()

        og_bullet = pygame.image.load("assets/bullet.png").convert_alpha()
        self.image = pygame.transform.rotate(pygame.transform.scale(og_bullet, (10, 20)), angle)
        self.rect = self.image.get_rect()

        self.realxcenter = xcenter
        self.realy = y

        self.rect.centerx = self.realxcenter
        self.rect.y = self.realy

        self.xchange = xchange
        self.ychange = ychange

    def update(self, platform, immortal):
        self.realxcenter += self.xchange
        self.realy += self.ychange

        self.rect.centerx = round(self.realxcenter)
        self.rect.y = round(self.realy)

        if self.rect.y >= SCREEN_HEIGHT:
            bullets.remove(self)

        if pygame.sprite.spritecollide(platform, bullets, True) and not immortal:
            if not dead:
                platform.lenset(platform.rect.w - 20)

class Powerup(pygame.sprite.Sprite):

    def __init__(self, x, y, size, power):
        super().__init__()

        self.size = size


        # POWER VALUES:
        # 1 = grow mushroom
        # 2 = fast platform
        # 3 = multiball
        self.power = power

        if self.power == 1:
            og_mushroom = pygame.image.load("assets/mushroom.png").convert_alpha()
            self.image = pygame.transform.scale(og_mushroom, (self.size, self.size))
            self.rect = self.image.get_rect()      
        if self.power == 2:
            og_swiftness = pygame.image.load("assets/swiftness.png").convert_alpha()
            self.image = pygame.transform.scale(og_swiftness, (self.size, self.size))
            self.rect = self.image.get_rect()
        if self.power == 3:
            og_multiball = pygame.image.load("assets/multiball.png").convert_alpha()
            self.image = pygame.transform.scale(og_multiball, (self.size, self.size))
            self.rect = self.image.get_rect()
        if self.power == 4:
            og_fireflower = pygame.image.load("assets/fireflower.png").convert_alpha()
            self.image = pygame.transform.scale(og_fireflower, (self.size, self.size))
            self.rect = self.image.get_rect()


        self.realx = x
        self.realy = y
        self.rect.x = int(self.realx)
        self.rect.y = int(self.realy)

    def move(self, xchange, ychange):
        self.realx += xchange
        self.realy += ychange
        self.rect.x = int(self.realx)
        self.rect.y = int(self.realy)

    def addpowerup(x, y, size, power):
        powerups.add(Powerup(x, y, size, power))

    def xcenter(self):
        return self.rect.x + (self.size/2)

    def ycenter(self):
        return self.rect.y + (self.size/2)

    def dopower(self, platforms, balls):
        if self.power == 1:
            for platform in platforms:
                platform.lenset(platform.rect.w + 75)
                platform.growcooldown = 150
        elif self.power == 2:
            for platform in platforms:
                platform.maxspd = 10
                platform.accel = 1
                platform.speedcooldown = 1500
        elif self.power == 3:
            for ball in balls:
                ball.multiball()
        elif self.power == 4:
            for ball in balls:
                ball.firecooldown = 400

    def update(self, platforms, balls):
        self.move(0, 2)
        if pygame.sprite.spritecollide(self, platforms, False):
            self.dopower(platforms, balls)
            powerups.remove(self)

class Bloodsplatter(pygame.sprite.Sprite):
    def __init__(self, xcenter, ycenter):
        super().__init__()

        og_blood = pygame.image.load("assets/blood.png")
        self.image = pygame.transform.scale(og_blood, (randint(5, 20), randint(5, 20)))
        self.rect = self.image.get_rect()

        self.rect.centerx = xcenter
        self.rect.centery = ycenter

        self.realw = self.rect.w
        self.realh = self.rect.h

        self.angle = randint(1, 361)

        self.velocity = 2

    def getx(self, angle):
        return cos(radians(self.angle))*self.velocity

    def gety(self, angle):
        return sin(radians(self.angle))*self.velocity*-1

    def update(self):
        self.rect.centerx += self.getx(self.angle)
        self.rect.centery += self.gety(self.angle)
        self.realw -= 0.7
        self.realh -= 0.7
        self.rect.h = round(self.realh)
        self.rect.w = round(self.realw)
        if self.rect.w <= 0 or self.rect.h <= 0:
            blood.remove(self)


titlescreen = True
losescreen = False
maingame = False
instructions = False
youlose = False



pygame.mixer.music.play(-1, 0, 0)


# main game loop
while True:


    # get user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # when user clicks the 'x' on the window, close the game
            pygame.quit()
            sys.exit()

    keys_pressed = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()


    if titlescreen:
        screen.blit(titlescaled, (0, 0))
        if keys_pressed[pygame.K_s]:
            screen.blit(loadingscaled, (0, 0))
            maingame = True
        if keys_pressed[pygame.K_i]:
            maingame = False
            titlescreen = False
            instructions = True
            title = False
            youlose = False


    if instructions:
        screen.blit(instructionsscaled, (0, 0))
        if keys_pressed[pygame.K_ESCAPE]:
            instructions = False
            titlescreen = True
            maingame = False
            youlose = False

    
    if losescreen:
        screen.blit(youlosescaled, (0, 0))

        if mouse_buttons[0]:
            instructions = False
            titlescreen = True
            maingame = False
            losescreen = False
            click.play()
            screen.blit(loadingscaled, (0, 0))


    if maingame:
        # create starting objects
        platform = Platform(500, 630)
        platforms.add(platform)
        spawnenemies(60, 50, 10, 5)
        spawnballs(ballcount, platform.rect.centerx, ballspawny, ballsize, 0, randrange(0, 900)/10+45)
        lives = 3
        dead = False

    while maingame:
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
        if dead and (((184 <= mousex <= 820) and (360 <= mousey <= 424) and mouse_buttons[0]) or keys_pressed[pygame.K_r]):
            balls.empty()
            platform.reset()
            click.play()
            spawnballs(ballcount, platform.rect.centerx, ballspawny, ballsize, 0, randrange(0, 900)/10+45)
            dead = False
        if dead and (((184 <= mousex <= 820) and (437 <= mousey <= 500) and mouse_buttons[0]) or keys_pressed[pygame.K_ESCAPE]):
            maingame = False
            titlescreen = True
            losescreen = False
            platforms.empty()
            balls.empty()
            enemies.empty()
            bullets.empty()
            blood.empty()
            powerups.empty()


        """
        UPDATE section - manipulate everything on the screen
        """

        platform.update()
        enemies.update(platform)
        balls.update(platform, enemies, Powerup, immortal)
        powerups.update(platforms, balls)
        bullets.update(platform, immortal)
        blood.update()
        if len(balls) < 1 or platform.rect.w < 40:
            if not dead:
                if lives > 1:
                    lives -= 1
                else:
                    maingame = False
                    titlescreen = False
                    losescreen = True
                    platforms.empty()
                    balls.empty()
                    enemies.empty()
                    bullets.empty()
                    blood.empty()
                    powerups.empty()
            dead = True

        if maingame:
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
            bullets.draw(screen)
            blood.draw(screen)

            if dead and not len(enemies) < 1:
                screen.blit(youdiedscaled, (0, 0))

            if len(enemies) < 1:
                vicy = sin(victorywave)
                screen.blit(victoryscaled, (20, vicy*100 + 80))
                immortal = True
                victorywave += 0.03

            for i in range(lives):
                screen.blit(heartscaled, (10+30*i, 660))

            pygame.display.flip()  # Pygame uses a double-buffer, without this we see half-completed frames

            clock.tick(FRAME_RATE)  # Pause the clock to always maintain FRAME_RATE frames per second

    pygame.display.flip()
