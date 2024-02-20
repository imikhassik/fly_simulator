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
YELLOW = (255, 255, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = fly_image
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .65 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = WIDTH / 2, HEIGHT / 2
        self.speed_y = 0
        self.speed_x = 0
        self.airborne = False

    def update(self):
        if self.airborne:
            self.unconstrain()
            self.fly()
        else:
            self.constrain()
            self.walk()

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

    def constrain(self):
        # constrained by screen boundaries
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def unconstrain(self):
        # wrap around screen
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotate(enemy_fly_image, 180)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .65 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.generate_coords()
        self.speed_y = 0
        self.speed_x = 0

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        # reset position and speed after a mob has moved off the screen
        if self.rect.top > HEIGHT + 10 or self.rect.left > WIDTH + 25 or self.rect.right < -25:
            self.generate_coords()
            self.generate_speed()

    def generate_coords(self):
        self.rect.x = random.randrange(WIDTH - 71)
        self.rect.y = random.randrange(-280, -80)

    def generate_speed(self):
        self.speed_y = random.randrange(2, 8)
        self.speed_x = random.randrange(-3, 3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = x
        self.rect.bottom = y
        self.speed_y = 8

    def update(self):
        self.rect.y -= self.speed_y
        if self.rect.y < 0:
            self.kill()


# set up assets directories
game_dir = os.path.dirname(__file__)
img_dir = os.path.join(game_dir, "img")

# initialize the game and create window
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fly Survival Simulator")

# load game graphics
fly_image = pygame.image.load(os.path.join(img_dir, "fly_white_small.png")).convert()
enemy_fly_image = pygame.image.load(os.path.join(img_dir, "fly_enemy_small.png")).convert()
bullet_image = pygame.image.load(os.path.join(img_dir, "bullet_small.png")).convert()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# create player
player = Player()
all_sprites.add(player)

# generate mobs
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
                        m.generate_speed()
                else:
                    # mobs go back up and stop moving
                    for m in mobs:
                        m.generate_coords()
                        m.speed_y = 0
                        m.speed_x = 0
            # shoot with space bar
            if event.key == pygame.K_SPACE:
                b = Bullet(player.rect.center, player.rect.top)
                all_sprites.add(b)
                bullets.add(b)

    # detect player collision with mob(s) and terminate
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    if hits:
        running = False

    # detect bullet - mob collision and eliminate both
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        m.generate_speed()

    # update
    all_sprites.update()

    # draw / render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    # flip the display *after* everything is drawn
    pygame.display.flip()

pygame.quit()
