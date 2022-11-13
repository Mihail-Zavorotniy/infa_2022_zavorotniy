import math
from random import choice
from random import randint as rnd
from math import pi

import pygame
from pygame import draw


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

left_key_down = False
right_key_down = False
score = 0
special_bullet = False


class Ball:
    def __init__(self, screen: pygame.Surface):
        """
        Конструктор класса Ball.
        """
        self.screen = screen
        self.x = gun.x1
        self.y = gun.y1
        self.r = 15
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.max_age = 90
        self.current_age = 0

    def move(self):
        """
        Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x + self.r >= 800:
            self.vx = -self.vx + 10
            self.x = 800 - self.r
        if self.x - self.r <= 0:
            self.vx = -self.vx - 10
            self.x = self.r
        if self.y + self.r >= 600:
            self.vy = -self.vy - 5
            self.y = 600 - self.r
        if self.y - self.r <= 0:
            self.vy = -self.vy + 5
            self.y = self.r
        self.vy -= 2
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        """
        Рисует мяч по его координатам.
        """
        draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """
        Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Если да, то убирает объект и цель из соответсвующих массивов.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        global bullets, targets
        if (self in bullets) and (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            bullets.remove(self)
            targets.remove(obj)
            return True
        else:
            return False

    def aging(self):
        """
        Если мяч просуществовал дольше определённого времени, удаляет его из массива.
        """
        global bullets
        self.current_age += 1
        if self.current_age > self.max_age:
            bullets = bullets[1:]


class Line(Ball):
    def __init__(self, screen):
        """
        Конструктор класса Line. Наследует класс Ball.
        Второй тип снарядов, переключение происходит стрелками вверх и вниз.
        """
        super().__init__(screen)
        self.r += 5
        self.an = gun.an

    def move(self):
        """
        В отличии от мячей, на движение не влияют ни гравитация, ни рамки окна.
        """
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        """
        Рисует линию. Направление линии совпадает с направлением дула.
        """
        draw.line(self.screen,
                  self.color,
                  (self.x, self.y),
                  (self.x + self.r * math.cos(self.an), self.y + self.r * math.sin(self.an)),
                  10
                  )


class Gun:
    def __init__(self, screen):
        """
        Конструктор класса Gun.
        """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = False
        self.an = pi
        self.color = GREY
        self.x1 = 40
        self.y1 = 570
        self.r = 30
        self.x2 = 70
        self.y2 = 550

    def move(self):
        """
        Двигает один конец дула.
        Движение происходит с помощью стрелочек вправо и влево.
        """
        global left_key_down, right_key_down
        if left_key_down and self.x1 >= 30:
            self.x1 -= 10
        if right_key_down and self.x1 <= 770:
            self.x1 += 10

    def fire_start(self):
        """
        Запускает процесс power_up
        """
        self.f2_on = True

    def fire_end(self, event):
        """
        Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global bullets, bullet_count
        bullet_count += 1
        if special_bullet:
            new_line = Line(screen)
            self.an = gun.an
            new_line.vx = self.f2_power * math.cos(self.an)
            new_line.vy = -self.f2_power * math.sin(self.an)
            bullets.append(new_line)
        else:
            new_ball = Ball(self.screen)
            self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
            new_ball.vx = self.f2_power * math.cos(self.an)
            new_ball.vy = -self.f2_power * math.sin(self.an)
            bullets.append(new_ball)
        self.f2_on = False
        self.f2_power = 10

    def targetting(self, event):
        """
        Прицеливание. Зависит от положения мыши.
        """
        if event.pos[0] == self.x1:
            if event.pos[1] < self.y1:
                self.an = 3*pi/2
            else:
                self.an = pi/2
        elif event.pos[0] > self.x1:
            self.an = math.atan((event.pos[1] - self.y1) / (event.pos[0] - self.x1))
        else:
            self.an = pi + math.atan((event.pos[1]-self.y1) / (event.pos[0]-self.x1))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """
        Рисует дуло в зависимоти от координат одного конца, радиуса и угла наклона.
        """
        draw.line(screen,
                  self.color,
                  (self.x1, self.y1),
                  (self.x1 + self.r * math.cos(self.an), self.y1 + self.r * math.sin(self.an)),
                  10)

    def power_up(self):
        """
        Меняет длинну и цвет дула пока оно заряжается.
        Также определет скорость снаряда.
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                self.r += 1
            self.color = RED
        else:
            self.color = GREY
            self.r = 30


class Target_round:
    def __init__(self):
        """
        Конструктор класса Target_round.
        """
        self.alive = True
        self.screen = pygame.Surface
        self.x = rnd(0, WIDTH)
        self.y = rnd(0, 300)
        self.r = rnd(20, 40)
        self.vx = rnd(3, 5) * choice([-1, 1])
        self.vy = rnd(3, 5) * choice([-1, 1])
        self.color = RED

    def move(self):
        """
        Круглые цели отскакивают от стен.
        Могут одновременно иметь и вертикальную, и горизонтальную компоненты скорости.
        """
        if self.x + self.r >= 800:
            self.vx = -self.vx
            self.x = 800 - self.r
        if self.x - self.r <= 0:
            self.vx = -self.vx
            self.x = self.r
        if self.y + self.r >= 300:
            self.vy = -self.vy
            self.y = 300 - self.r
        if self.y - self.r <= 0:
            self.vy = -self.vy
            self.y = self.r
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        """
        Рисует круглые цели.
        """
        draw.circle(screen, self.color, (self.x, self.y), self.r, 0)
        draw.circle(screen, BLACK, (self.x, self.y), self.r, 1)

    def hit(self, points=1):
        global score
        """Попадание шарика в цель."""
        score += points

    def spawn_bomb(self):
        """
        Каждая цель каждый фрейм имеет вероятность 1% сбросить бомбу.
        """
        global bombs
        if not rnd(0,99):
            new_bomb = Bomb()
            new_bomb.x = self.x
            new_bomb.y = self.y
            bombs.append(new_bomb)


class Target_square(Target_round):
    def __init__(self):
        """
        Конструктор класса Target_square. Наследует класс Target_round.
        """
        super().__init__()
        self.color = BLUE
        self.stride_time = 0
        self.moving_x = True

    def move(self):
        """
        Квадратные цели, как и круглые, отскакивают от стен.
        Двигаются либо вертикально, либо горизонтально.
        Каждые 10 фреймов с вероятностью 50% меняют ось движения.
        """
        if self.x + self.r >= 800:
            self.vx = -self.vx
            self.x = 800 - self.r
        if self.x - self.r <= 0:
            self.vx = -self.vx
            self.x = self.r
        if self.y + self.r >= 300:
            self.vy = -self.vy
            self.y = 300 - self.r
        if self.y - self.r <= 0:
             self.vy = -self.vy
             self.y = self.r
        if self.stride_time == 10:
            self.stride_time = 0
            self.stride_time += 1
        if self.moving_x:
            self.x += self.vx
        else:
            self.y += self.vy
        self.stride_time += 1
        if self.stride_time == 10:
            self.stride_time = 0
            if rnd(0,1):
                self.moving_x = not self.moving_x


    def draw(self):
        """
        Рисует квадратные цели.
        """
        draw.rect(screen,
                  self.color,
                  (self.x - self.r, self.y - self.r, 2*self.r, 2*self.r)
                  )
        draw.rect(screen,
                  BLACK,
                  (self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r),
                  1)



class Tank:
    def __init__(self):
        """
        Конструктор класса Tank.
        """
        self.alive = True
        self.screen = pygame.Surface
        self.r = 15
        self.x = gun.x1
        self.y = gun.y1

    def draw(self):
        """
        Рисует корпус и башню танка по его координатам.
        """
        draw.circle(screen, GREEN, (self.x, self.y), self.r)
        draw.circle(screen, BLACK, (self.x, self.y), self.r, 1)
        draw.rect(screen, GREEN, (self.x-30, self.y, 60, 30))
        draw.rect(screen, BLACK, (self.x - 30, self.y, 60, 30), 1)

    def pos_update(self):
        """
        Обновляет координаты танка, чтобы они совпадали с координатами начала дула
        """
        self.x = gun.x1
        self.y = gun.y1


class Bomb:
    def __init__(self):
        """
        Конструктор класса Bomb.
        """
        self.r = 10
        self.vy = 4
        self.color = BLACK

    def move(self):
        """
        Двигается вертикально вниз без ускорения.
        Если достигла нижней границы, удаляется из массива.
        """
        global bombs
        self.y += self.vy
        if len(bullets) > 0 and self.y >= HEIGHT:
            bombs.remove(self)

    def draw(self):
        """
        Рисует бомбу.
        """
        draw.circle(screen, self.color, (self.x, self.y), self.r, 0)

    def hit_tank(self, obj):
        """
        Проверяет, столкнулась ли бомба с танком.
        """
        if abs(self.x - obj.x) < 25 and abs(self.y - obj.y) < 25:
            obj.alive = False


def new_round_target():
    """ Инициализация новой круглой цели. Добавление её в массив целей."""
    global targets
    new_round_target = Target_round()
    targets.append(new_round_target)


def new_square_target():
    """ Инициализация новой квадратной цели. Добавление её в массив целей."""
    global targets
    new_square_target = Target_square()
    targets.append(new_square_target)


def display_score():
    """ Отображает текущий счёт."""
    font = pygame.font.SysFont('arial', 26)
    text = font.render('Score: ' + str(score) + '', True, (10, 10, 10))
    textpos = text.get_rect(centerx=45, y=15)
    screen.blit(text, textpos)


def display_results():
    """ Если бомба попала в танк, останавливает игру и выводит соответствующую надпись."""
    draw.rect(screen, WHITE, (tank.x - 35, tank.y - 35, 70, 70))
    draw.rect(screen, WHITE, (WIDTH / 2 - 350, HEIGHT / 2 - 40, 700, 100))
    draw.rect(screen, BLACK, (WIDTH / 2 - 350, HEIGHT / 2 - 40, 700, 100), 2)
    font = pygame.font.SysFont('arial', 36)
    text = font.render('Your tank was destroyed. Your score is '+str(score)+' points.', True, (10, 10, 10))
    textpos = text.get_rect(centerx=WIDTH/2, y=HEIGHT/2)
    screen.blit(text, textpos)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet_count = 0
targets = []
bullets = []
bombs = []

clock = pygame.time.Clock()
gun = Gun(screen)
tank = Tank()
for i in range(6):
    if rnd(0,1):
        new_round_target()
    else:
        new_square_target()

finished = False

while not finished:
    if not tank.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        display_results()
        pygame.display.update()
    else:
        screen.fill(WHITE)
        gun.move()
        gun.draw()
        tank.pos_update()
        tank.draw()
        display_score()
        for target in targets:
            target.spawn_bomb()
            target.move()
            target.draw()
        for bomb in bombs:
            bomb.hit_tank(tank)
            bomb.move()
            bomb.draw()
        for bullet in bullets:
            bullet.aging()
            bullet.draw()
        pygame.display.update()

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_key_down = True
                if event.key == pygame.K_RIGHT:
                    right_key_down = True
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    special_bullet = not special_bullet
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_key_down = False
                if event.key == pygame.K_RIGHT:
                    right_key_down = False
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gun.fire_start()
            elif event.type == pygame.MOUSEBUTTONUP:
                gun.fire_end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)

        for bullet in bullets:
            bullet.move()
            for target in targets:
                if bullet.hittest(target) and target.alive:
                    target.alive = False
                    target.hit()
                    if rnd(0,1):
                        new_round_target()
                    else:
                        new_square_target()

        gun.power_up()

pygame.quit()