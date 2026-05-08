import pygame
import time
import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
creature = pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - i*dt, 50, 50)

def drawCreature():
    for i in range(0,100):
        pygame.draw.rect(window, ("white"), creature)



while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()



    dt = clock.tick(60) / 1000
    window.fill((0,0,0))
    drawCreature()
    pygame.display.update()