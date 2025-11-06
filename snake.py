import pygame, sys, random

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL = 20
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 20)

GREEN1 = (100, 200, 100)
GREEN2 = (80, 180, 80)

def load_img(path):
    return pygame.transform.scale(pygame.image.load(path), (CELL, CELL))

head_up = load_img("assets/head_up.png")
head_down = load_img("assets/head_down.png")
head_left = load_img("assets/head_left.png")
head_right = load_img("assets/head_right.png")

body_h = load_img("assets/body_horizontal.png")
body_v = load_img("assets/body_vertical.png")
body_ul = load_img("assets/body_topleft.png")
body_ur = load_img("assets/body_topright.png")
body_dl = load_img("assets/body_bottomleft.png")
body_dr = load_img("assets/body_bottomright.png")

tail_up = load_img("assets/tail_up.png")
tail_down = load_img("assets/tail_down.png")
tail_left = load_img("assets/tail_left.png")
tail_right = load_img("assets/tail_right.png")

food_img = pygame.transform.scale(pygame.image.load("assets/apple.png"), (CELL, CELL))

eat_sound = pygame.mixer.Sound("assets/metal-gear-item-drop.mp3")


backgroundMusic = pygame.mixer.Sound("assets/Snake Eater.mp3")
backgroundMusic.play(-1)
backgroundMusic.set_volume(0.3)


snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL, 0)
score = 0

import random
food = (random.randint(0, (WIDTH-CELL)//CELL)*CELL,
        random.randint(0, (HEIGHT-CELL)//CELL)*CELL)

def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("Arial", size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    win.blit(surface, rect)


def start_screen():
    win.fill((0, 0, 0))
    draw_text("Snake Game", 50, (255, 255, 255), WIDTH // 2, HEIGHT // 3)
    draw_text("Drücke eine Taste zum Starten", 30, (200, 200, 200), WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def game_over_screen():
    win.fill((0, 0, 0))
    draw_text("Game Over", 50, (255, 0, 0), WIDTH // 2, HEIGHT // 3)
    draw_text("Drücke eine Taste zum Neustarten", 30, (200, 200, 200), WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def draw_background():
    for y in range(0, HEIGHT, CELL):
        for x in range(0, WIDTH, CELL):
            color = GREEN1 if (x//CELL + y//CELL)%2==0 else GREEN2
            pygame.draw.rect(win, color, (x, y, CELL, CELL))


def direction_between(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return dx // CELL, dy // CELL


def get_head_sprite(head, second):
    d = direction_between(second, head)
    if d == (1, 0): return head_right
    if d == (-1, 0): return head_left
    if d == (0, 1): return head_down
    if d == (0, -1): return head_up
    return pygame.surface.Surface((CELL, CELL))


def get_tail_sprite(second_last, tail):

    d = direction_between(tail, second_last)
    if d == (1,0):
        return tail_left
    if d == (-1,0):
        return tail_right
    if d == (0,1):
        return tail_up
    if d == (0,-1):
        return tail_down

    return pygame.surface.Surface((CELL, CELL))


def get_body_sprite(prev, curr, nxt):
    d1 = direction_between(curr, prev)
    d2 = direction_between(curr, nxt)

    if d1[0] == d2[0]:
        return body_v
    if d1[1] == d2[1]:
        return body_h

    if (d1, d2) in [((0, -1), (1, 0)), ((1, 0), (0, -1))]:
        return body_ur
    if (d1, d2) in [((0, -1), (-1, 0)), ((-1, 0), (0, -1))]:
        return body_ul
    if (d1, d2) in [((0, 1), (1, 0)), ((1, 0), (0, 1))]:
        return body_dr
    if (d1, d2) in [((0, 1), (-1, 0)), ((-1, 0), (0, 1))]:
        return body_dl
    return pygame.surface.Surface((CELL, CELL))

start_screen()
while True:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP and direction != (0, CELL):
                direction = (0, -CELL)
            if e.key == pygame.K_DOWN and direction != (0, -CELL):
                direction = (0, CELL)
            if e.key == pygame.K_LEFT and direction != (CELL, 0):
                direction = (-CELL, 0)
            if e.key == pygame.K_RIGHT and direction != (-CELL, 0):
                direction = (CELL, 0)

    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake = [new_head] + snake[:-1]

    if (new_head[0] < 0 or new_head[0] >= WIDTH
        or new_head[1] < 0 or new_head[1] >= HEIGHT) or new_head in snake[1:]:
        backgroundMusic.stop()
        pygame.mixer.music.load("assets/metalgeargameov5235.mp3")
        pygame.mixer.music.play()
        game_over_screen()
        backgroundMusic.play()
        score = 0
        snake = [(100, 100), (80, 100), (60, 100)]
        direction = (CELL, 0)
        food = (random.randint(0, (WIDTH - CELL) // CELL) * CELL,
                random.randint(0, (HEIGHT - CELL) // CELL) * CELL)

    draw_background()
    win.blit(food_img, food)

    if snake[0] == food:
        snake.append(snake[-1])
        eat_sound.play()
        score += 1
        clock.tick(5)
        food = (random.randint(0, (WIDTH - CELL) // CELL) * CELL,
                random.randint(0, (HEIGHT - CELL) // CELL) * CELL)

    win.blit(get_head_sprite(snake[0], snake[1]), snake[0])

    for i in range(1, len(snake) - 1):
        win.blit(get_body_sprite(snake[i + 1], snake[i], snake[i - 1]), snake[i])

    win.blit(get_tail_sprite(snake[-2], snake[-1]), snake[-1])

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, score_text.get_rect(center=(80, 50)))

    pygame.display.flip()
    clock.tick(5)
