import pygame
import os
import random
import sys

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()
EASY = ['map1.txt', 'map2.txt', 'map3.txt']
MEDIUM = ['map4.txt', 'map5.txt', 'map6.txt']
HARD = ['map7.txt', 'map8.txt', 'map9.txt']

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["начало игры"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

image = load_image("flower.jpg")
image1 = pygame.transform.scale(image, (200, 100))
tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png'),
               'flower': load_image('flower.jpg'), 'lava': load_image('lava.png')}
player_image = load_image('mario.png')
tile_width = tile_height = 40
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
flowers_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall':
            self.add(walls_group)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, x, y):
        self.rect = self.image.get_rect().move(self.rect.x + x * tile_width, tile_height * y + self.rect.y)


def generate_level_easy(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '*':
                Tile('flower', x, y)
            elif level[y][x] == '~':
                Tile('lava', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                xx = x
                yy = y
    new_player = Player(xx, yy)
    return new_player, x, y


def generate_level_medium(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                xx = x
                yy = y
    new_player = Player(xx, yy)
    return new_player, x, y


def generate_level_hard(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                xx = x
                yy = y
    new_player = Player(xx, yy)
    return new_player, x, y


player, level_x, level_y = generate_level_easy(load_level(random.choice(EASY)))
start_screen()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move(-1, 0)
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move(1, 0)
            elif event.key == pygame.K_RIGHT:
                player.move(1, 0)
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move(-1, 0)
            elif event.key == pygame.K_DOWN:
                player.move(0, 1)
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move(0, -1)
            elif event.key == pygame.K_UP:
                player.move(0, -1)
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move(0, 1)
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()