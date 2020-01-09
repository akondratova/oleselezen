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


class start_screen():
    def __init__(self):
        intro_text = ["начало игры"]
        fon = pygame.transform.scale(load_image('sun.png'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
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

    def button(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        running = False
        if (400 + 40 > mouse[0] > 400) and (500 + 25 > mouse[1] > 500):
            pygame.draw.rect(screen, (0, 0, 240), (400, 500, 40, 25))
            if (click[0] == 1 and action != None):
                if (action == "Start"):
                    running = True
                elif (action == "Exit"):
                    pygame.quit()

        else:
            pygame.draw.rect(screen, (0, 0, 255), (400, 500, 40, 25))
            smallText = pygame.font.Font("freesansbold.ttf", 20)
            textSurf, textRect = text_objects(, smallText)
            textRect.center = ((400 + (40 / 2)), (500 + (25 / 2)))
            screen.blit(textSurf, textRect)

        return running


def final_screen():
    intro_text = ["Congratulations", 'You are winner!']
    f = load_image('final.png')
    final = pygame.transform.scale(f, (750, 750))
    screen.blit(final, (0, 0))
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


def lose_screen():
    intro_text = ['Game over,', 'You lose!']
    lose = load_image('lose.jpg')
    screen.blit(lose, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
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


tile_width = tile_height = 40
r = load_image('rock.png')
rock = pygame.transform.scale(r, (tile_width, tile_height))
e = load_image('grass.png')
empty = pygame.transform.scale(e, (tile_width, tile_height))
f = load_image('flower.jpg')
flower = pygame.transform.scale(f, (tile_width, tile_height))
l = load_image('lava.png')
lava = pygame.transform.scale(l, (tile_width, tile_height))
p = load_image('portal.png')
portal = pygame.transform.scale(p, (tile_width, tile_height))
tile_images = {'wall': rock, 'empty': empty,
               'flower': flower, 'lava': lava, 'portal': portal}
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
flower_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()


class Flower(pygame.sprite.Sprite):
    image = f

    def __init__(self):
        super().__init__(flower_group)
        self.rect = self.image.get_rect()
        self.dx = 1

    def update(self, *args):
        self.rect = self.image.get_rect()
        self.dx = 1
        if pygame.sprite.spritecollideany(flower_group, walls_group):
            self.dx = -self.dx
        self.rect = self.rect.move(self.dx, 0)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall':
            self.add(walls_group)
        elif tile_type == 'portal':
            self.add(portal_group)
        elif tile_type == 'lava':
            self.add(lava_group)
        elif tile_type == 'flower':
            self.add(flower_group)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale((sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size))), (tile_width - 3, tile_height - 3)))
        self.frames_right = self.frames[:6]
        self.frames_left = self.frames[7:12]

    def update_left(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames_left)
        self.image = self.frames_left[self.cur_frame]

    def update_right(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames_right)
        self.image = self.frames_right[self.cur_frame]

    def move(self, x, y):
        self.rect = self.image.get_rect().move(self.rect.x + x * tile_width, tile_height * y + self.rect.y)


def generate_level(level):
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
            elif level[y][x] == 'x':
                Tile('portal', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                xx = x
                yy = y
    new_player = AnimatedSprite(load_image("character.jpg"), 6, 3, xx, yy)
    return new_player, x, y


player, level_x, level_y = generate_level(load_level(random.choice(EASY)))
u = 'easy'
running = start_screen.button()

while running:
    Flower()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move(-1, 0)
                player.update_left()
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move(1, 0)
            elif event.key == pygame.K_RIGHT:
                player.move(1, 0)
                player.update_right()
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move(-1, 0)
            elif event.key == pygame.K_DOWN:
                player.move(0, 1)
                player.update_left()
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move(0, -1)
            elif event.key == pygame.K_UP:
                player.move(0, -1)
                player.update_right()
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move(0, 1)

        elif pygame.sprite.spritecollideany(player, portal_group) and u == 'easy':
            size = width, height = 700, 700
            screen = pygame.display.set_mode(size)
            tile_width = tile_height = 35
            r = load_image('rock.png')
            rock = pygame.transform.scale(r, (tile_width, tile_height))
            e = load_image('grass.png')
            empty = pygame.transform.scale(e, (tile_width, tile_height))
            f = load_image('flower.jpg')
            flower = pygame.transform.scale(f, (tile_width, tile_height))
            l = load_image('lava.png')
            lava = pygame.transform.scale(l, (tile_width, tile_height))
            p = load_image('portal.png')
            portal = pygame.transform.scale(p, (tile_width, tile_height))
            tile_images = {'wall': rock, 'empty': empty,
                           'flower': flower, 'lava': lava, 'portal': portal}
            player, level_x, level_y = generate_level(load_level(random.choice(MEDIUM)))
            u = 'medium'
        elif pygame.sprite.spritecollideany(player, portal_group) and u == 'medium':
            size = width, height = 750, 750
            screen = pygame.display.set_mode(size)
            tile_width = tile_height = 25
            r = load_image('rock.png')
            rock = pygame.transform.scale(r, (tile_width, tile_height))
            e = load_image('grass.png')
            empty = pygame.transform.scale(e, (tile_width, tile_height))
            f = load_image('flower.jpg')
            flower = pygame.transform.scale(f, (tile_width, tile_height))
            l = load_image('lava.png')
            lava = pygame.transform.scale(l, (tile_width, tile_height))
            p = load_image('portal.png')
            portal = pygame.transform.scale(p, (tile_width, tile_height))
            tile_images = {'wall': rock, 'empty': empty,
                           'flower': flower, 'lava': lava, 'portal': portal}
            player, level_x, level_y = generate_level(load_level(random.choice(HARD)))
            u = 'hard'
        elif pygame.sprite.spritecollideany(player, portal_group) and u == 'hard':
            final_screen()
        elif (pygame.sprite.spritecollideany(player, flower_group) or
              pygame.sprite.spritecollideany(player, lava_group)):
            lose_screen()
            size = width, height = 600, 600
            screen = pygame.display.set_mode(size)
            tile_width = tile_height = 40
            r = load_image('rock.png')
            rock = pygame.transform.scale(r, (tile_width, tile_height))
            e = load_image('grass.png')
            empty = pygame.transform.scale(e, (tile_width, tile_height))
            f = load_image('flower.jpg')
            flower = pygame.transform.scale(f, (tile_width, tile_height))
            l = load_image('lava.png')
            lava = pygame.transform.scale(l, (tile_width, tile_height))
            p = load_image('portal.png')
            portal = pygame.transform.scale(p, (tile_width, tile_height))
            tile_images = {'wall': rock, 'empty': empty,
                           'flower': flower, 'lava': lava, 'portal': portal}
            player, level_x, level_y = generate_level(load_level(random.choice(EASY)))
            u = 'easy'
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()
