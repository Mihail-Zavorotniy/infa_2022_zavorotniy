import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((255, 255, 255))

circle(screen, (255, 255, 0), (200, 200), 150)
circle(screen, (0, 0, 0), (200, 200), 150, 2)
circle(screen, (255, 0, 0), (140, 150), 35)
circle(screen, (255, 0, 0), (260, 150), 25)
circle(screen, (0, 0, 0), (140, 150), 35, 2)
circle(screen, (0, 0, 0), (260, 150), 25, 2)
circle(screen, (0, 0, 0), (140, 150), 15)
circle(screen, (0, 0, 0), (260, 150), 10)
rect(screen, (0, 0, 0), (125, 250, 150, 25))
line(screen, (0, 0, 0), (80, 50), (180, 150), 20)
line(screen, (0, 0, 0), (350, 50), (220, 150), 20)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()