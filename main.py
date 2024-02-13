import pygame
import os

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

        # wrap around screen
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT

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
player = Player()
all_sprites.add(player)

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

    # update
    all_sprites.update()

    # draw / render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    # flip the display *after* everything is drawn
    pygame.display.flip()

pygame.quit()
