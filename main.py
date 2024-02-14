import pygame
import os
import random

WIDTH = 600
HEIGHT = 800
FPS = 60

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(img_dir, "fly_white_small.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT / 2
        self.speed_y = 0
        self.speed_x = 0
        self.airborne = False

    def update(self):
        if self.airborne:
            self.fly()
        else:
            self.walk()

        if self.airborne:
            # wrap around screen
            if self.rect.left > WIDTH:
                self.rect.right = 0
            if self.rect.right < 0:
                self.rect.left = WIDTH
            if self.rect.top > HEIGHT:
                self.rect.bottom = 0
            if self.rect.bottom < 0:
                self.rect.top = HEIGHT
        else:
            # constrained by walls
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0

    def walk(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a]:
            self.rect.x -= 5
        if pressed_keys[pygame.K_d]:
            self.rect.x += 5
        if pressed_keys[pygame.K_w]:
            self.rect.y -= 5
        if pressed_keys[pygame.K_s]:
            self.rect.y += 5

    def fly(self):
        self.speed_y = -2
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a]:
            self.speed_x = -5
        if pressed_keys[pygame.K_d]:
            self.speed_x = 5
        if pressed_keys[pygame.K_w]:
            self.speed_y = -5
        if pressed_keys[pygame.K_s]:
            self.speed_y = 5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - 30)
        self.rect.y = random.randrange(-200, -50)
        self.speed_y = 0
        self.speed_x = 0

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        # reset position and speed after a mob has moved off the screen
        if self.rect.top > HEIGHT + 10 or self.rect.left > WIDTH + 25 or self.rect.right < -25:
            self.rect.x = random.randrange(WIDTH - 30)
            self.rect.y = random.randrange(-200, -50)
            self.speed_y = random.randrange(2, 8)
            self.speed_x = random.randrange(-3, 3)


# set up assets directories
game_dir = os.path.dirname(__file__)
img_dir = os.path.join(game_dir, "img")

# initialize the game and create window
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fly Survival Simulator")

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()

# create player
player = Player()
all_sprites.add(player)

# create mobs
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# game loop
running = True
while running:
    # keep game running at FPS speed
    clock.tick(FPS)

    # process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # toggle walk / fly mode
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                player.airborne = not player.airborne
                if player.airborne:
                    # mobs start moving
                    for m in mobs:
                        m.speed_y = random.randrange(2, 8)
                        m.speed_x = random.randrange(-3, 3)
                else:
                    # mobs go back up and stop moving
                    for m in mobs:
                        m.rect.x = random.randrange(WIDTH - 30)
                        m.rect.y = random.randrange(-200, -50)
                        m.speed_y = 0
                        m.speed_x = 0

    # update
    all_sprites.update()

    # draw / render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    # flip the display *after* everything is drawn
    pygame.display.flip()

pygame.quit()
