import pygame
import time
import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def drawCreature(timer):
        creature = pygame.Rect(SCREEN_WIDTH/2 - (timer *100), SCREEN_HEIGHT/2 + (timer *100), 50, 50)
        pygame.draw.rect(window, ("white"), creature)



total_timeleft = random.randint(3,9)

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()



    dt = clock.tick(60) / 1000
    
    if total_timeleft > 0:
        total_timeleft -= dt
    else:
        total_timeleft = random.randint(3,9)
    
    
    print(total_timeleft)
    window.fill((0,0,0))
    drawCreature(total_timeleft)
    pygame.display.update()