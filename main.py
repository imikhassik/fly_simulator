# art original by Ilya Mikhasik
# pop sounds from https://creatorassets.com/a/pop-sound-effects
# spit sounds from https://opengameart.org/content/80-cc0-creature-sfx
# buzz sound from https://www.youtube.com/watch?v=t4_5P_sWGyA
# music by pixelsphere.org / The Cynic Project

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


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(os.path.join(font_dir, "Nums-Regular.ttf.otf"), size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def spawn_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    return m


def draw_fuel_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0

    BAR_LENGTH = 100
    BAR_HEIGHT = 10

    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, YELLOW, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = fly_image
        self.image_orig.set_colorkey(WHITE)
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .65 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = WIDTH / 2, HEIGHT / 2
        self.speed_y = 0
        self.speed_x = 0
        self.airborne = False
        self.rotation = 0
        self.last_update = pygame.time.get_ticks()
        self.fuel = 100

    def update(self):
        now = pygame.time.get_ticks()
        # fuel goes down 1% every 1 second
        if now - self.last_update >= 1000:
            self.last_update = now
            self.fuel -= 1

        if self.airborne:
            self.unconstrain()
            self.fly()
        else:
            self.constrain()
            self.walk()

    def walk(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a]:
            self.rotation = 90
            self.rect.x -= 5
        if pressed_keys[pygame.K_d]:
            self.rotation = 270
            self.rect.x += 5
        if pressed_keys[pygame.K_w]:
            self.rotation = 0
            self.rect.y -= 5
        if pressed_keys[pygame.K_s]:
            self.rotation = 180
            self.rect.y += 5

        new_image = pygame.transform.rotate(self.image_orig, self.rotation)
        self.image = new_image

    def fly(self):
        self.speed_y = -2
        self.rotation = 0
        new_image = pygame.transform.rotate(self.image_orig, self.rotation)
        self.image = new_image

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

    def shoot(self):
        if not len(bullets):
            b = Bullet(player.rect.center, player.rect.top)
            all_sprites.add(b)
            bullets.add(b)
            spit_sound.play()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = pygame.transform.rotate(random.choice(enemy_images), 180)
        self.image_orig.set_colorkey(WHITE)
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .65 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.generate_coords()
        self.speed_y = 0
        self.speed_x = 0
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        # self.rotate()
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

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            # get new rotation image every 50 milliseconds
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


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


# initialize the game and create window
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fly Survival Simulator")


# set up assets directories
game_dir = os.path.dirname(__file__)
img_dir = os.path.join(game_dir, "img")
snd_dir = os.path.join(game_dir, "snd")
font_dir = os.path.join(game_dir, "fonts")

# load game graphics
fly_image = pygame.image.load(os.path.join(img_dir, "fly_white_small.png")).convert()
bullet_image = pygame.image.load(os.path.join(img_dir, "bullet_small.png")).convert()

enemy_image_names = ["fly_enemy_small.png", "fly_enemy_small_1.png",
                     "fly_enemy_small_2.png", "fly_enemy_small_3.png"]
enemy_images = []
for image_name in enemy_image_names:
    enemy_images.append(pygame.image.load(os.path.join(img_dir, image_name)).convert())

# load sounds
spit_sound = pygame.mixer.Sound(os.path.join(snd_dir, "spit-small.ogg"))
spit_sound.set_volume(0.2)
pop_sound_files = ["pop-1.mp3", "pop-6.mp3", "pop-7.mp3"]
pop_sounds = []
for pop in pop_sound_files:
    pop_sounds.append(pygame.mixer.Sound(os.path.join(snd_dir, pop)))
buzz = pygame.mixer.Sound(os.path.join(snd_dir, "buzz.ogg"))

# background music
pygame.mixer.music.load(os.path.join(snd_dir, "background.mp3"))
pygame.mixer.music.play(loops=-1)


# sprite groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# create player
player = Player()
all_sprites.add(player)

# generate mobs
for i in range(8):
    spawn_mob()

score = 0

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
                    # mobs start moving and buzzing starts
                    buzz.play(loops=-1)
                    for m in mobs:
                        m.generate_speed()
                else:
                    # mobs go back up and stop moving, buzzing stops
                    buzz.stop()
                    for m in mobs:
                        m.generate_coords()
                        m.speed_y = 0
                        m.speed_x = 0
            # shoot with space bar
            if event.key == pygame.K_SPACE:
                player.shoot()

    # detect player collision with mob(s) and terminate
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    if hits:
        running = False

    # detect bullet - mob collision and eliminate both
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        score += 1
        pop_sound = random.choice(pop_sounds)
        pop_sound.play()
        m = spawn_mob()
        m.generate_speed()

    # update
    all_sprites.update()

    # draw / render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 25, WIDTH / 2, 10)
    draw_fuel_bar(screen, 5, 5, player.fuel)
    # flip the display *after* everything is drawn
    pygame.display.flip()

pygame.quit()
