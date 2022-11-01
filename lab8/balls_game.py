import random

import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

global x, y, r, v_x, v_y, color, how_many, life_length, score, missed, lived

how_many = 10
score = 0
missed = True
x = [randint(50, 1150) for i in range(how_many)]
y = [randint(50, 850) for i in range(how_many)]
r = [randint(30, 50) for i in range(how_many)]
v_x = [randint(-10, 10) for i in range(how_many)]
v_y = [randint(-10, 10) for i in range(how_many)]
color = [COLORS[randint(0, 5)] for i in range(how_many)]
life_length = [randint(60, 90) for i in range(how_many)]
lived = [0] * how_many
bonus = [False] * how_many

def new_ball(id):
    '''

    Принимает целое число. Заменяет шарик с таким номером на новый, случайно сгенерированный, и с вероятностью 10% делает его бонусным.
    '''

    global x, y, r, v_x, v_y, color
    x[id] = randint(50, 1150)
    y[id] = randint(50, 850)
    r[id] = randint(30, 50)
    color[id] = COLORS[randint(0, 5)]
    lived[id] = 0
    bonus[id] = (randint(0, 9) == 1)
    if bonus[id]:
        v_x[id] = randint(15, 25) * random.choice([-1, 1])
        v_y[id] = randint(15, 25) * random.choice([-1, 1])
    else:
        v_x[id] = randint(-10, 10)
        v_y[id] = randint(-10, 10)
    circle(screen, color[id], (x[id], y[id]), r[id])

def pos_update():
    '''

    На каждом тике обновляет параметры всех шариков.
    Изменяет их положение в соответствии с их скоростью.
    При соприкосновении шарика со стенкой заменяет его соответствующую компоненту скорости на противоположную.
    Если шарик просуществовал определённое количество тиков, заменяет его новым шариком при помощи функции new_ball.
    Если шарик бонусный, то на каждом тике меняет его цвет.
    '''
    global x, y, r, v_x, v_y, color
    for i in range(how_many):
        lived[i] += 1
        if lived[i] == life_length[i]:
            new_ball(i)
        if x[i] - r[i] <= 0 or x[i] + r[i] >= 1200:
            v_x[i] = -v_x[i]
        if y[i] - r[i] <= 0 or y[i] + r[i] >= 900:
            v_y[i] = -v_y[i]
        x[i] += v_x[i]
        y[i] += v_y[i]
        if bonus[i]:
            color[i] = COLORS[randint(0, 5)]
        circle(screen, color[i], (x[i], y[i]), r[i])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

new_ball(0)
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            missed = True
            for i in range(how_many):
                if ((event.pos[0] - x[i])**2 + (event.pos[1] - y[i])**2) <= r[i]**2:
                    missed = False
                    if bonus[i]:
                        score += 3
                        print('+ 3 Points!')
                    else:
                        score += 1
                        print('+ 1 Point!')
                    new_ball(i)
            if missed:
                print('Miss!')
    pos_update()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
print('Your score is ' + str(score) + ' points!')

help(new_ball)
help(pos_update)
