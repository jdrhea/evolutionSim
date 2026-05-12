import pygame
import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Creature:
    def __init__(self, clone_color = None, clone_size = None):
        self.switchDirection = False

        self.colorVals = random.randint(0,255)
        self.size = (random.randint(40,60))

        offspring_color = self.colorVals #+ random.randint(-20, 20)
        offspring_size = self.size #* random.uniform(0.75, 1.25)
        
        if clone_color is None:
            self.colorVals = random.randint(0,255)
            clone_color = self.colorVals
        else:
            self.colorVals = offspring_color
            clone_color = offspring_color

        if clone_size is None:
            self.size = random.randint(40,60)
            clone_size = self.size
        else:
            self.size = offspring_size
            clone_size = offspring_size
        self.old_X_position = random.randint(0, SCREEN_WIDTH)
        self.old_Y_position = random.randint(0, SCREEN_HEIGHT)

        self.new_X_position = random.randint(0, SCREEN_WIDTH)
        self.new_Y_position = random.randint(0, SCREEN_HEIGHT)

        self.total_timeleftX = self.old_X_position - self.new_X_position
        self.total_timeleftY = self.old_Y_position - self.new_Y_position
        self.life = random.randint(1,12)
        
    def update (self, dt):
        if self.total_timeleftX > 0:
            self.total_timeleftX -= 200 * dt
        elif self.total_timeleftX < 0:
            self.total_timeleftX += 200 * dt
    
        if self.total_timeleftY > 0:
            self.total_timeleftY -= 200 * dt
        elif self.total_timeleftY < 0:
            self.total_timeleftY += 200 * dt
        
        if abs(self.total_timeleftX) < 5:
            self.total_timeleftX = 0

        if abs(self.total_timeleftY) < 5:
            self.total_timeleftY = 0
        
        if self.total_timeleftX == 0 and self.total_timeleftY == 0:
            self.switchDirection = True
        
        if self.switchDirection:
            self.old_X_position = self.new_X_position
            self.old_Y_position = self.new_Y_position
            self.new_X_position = random.randint(0, SCREEN_WIDTH)
            self.new_Y_position = random.randint(0, SCREEN_HEIGHT)
            self.total_timeleftX = self.old_X_position - self.new_X_position
            self.total_timeleftY = self.old_Y_position - self.new_Y_position
            self.switchDirection = False
        self.life -= dt

    def drawCreature(self, window):

        current_x = self.new_X_position + self.total_timeleftX
        current_y = self.new_Y_position + self.total_timeleftY

        self.creature = pygame.Rect(current_x, current_y, self.size, self.size)
        pygame.draw.rect(window, (self.colorVals,self.colorVals,self.colorVals), self.creature)
        
class Food:

    def __init__(self):
        self.positionX = random.randint(0,SCREEN_WIDTH)
        self.positionY = random.randint(0,SCREEN_HEIGHT)
        self.FoodTypes = ["food", "water"]
        self.Food = random.choice(self.FoodTypes)
        self.rect = pygame.Rect(self.positionX, self.positionY, 20, 20)
        
    def drawFood(self, window):
        if self.Food == "food":
            pygame.draw.rect(window, (255, 0, 0), self.rect)
        else:
            pygame.draw.rect(window, (0, 0, 255), self.rect)



global population
original_amount = 5
population = original_amount
  
creatures = [Creature() for _ in range (original_amount)]
foodPerCreature = 0.7
food = [Food() for _ in range (round(population * foodPerCreature))]
spawn_timer = 0
timer = 0
    
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    
    dt = clock.tick(60) / 1000

    spawn_timer += dt
    timer+=dt
    generation_length = 5
    power = 2
    removeFood = False

    if spawn_timer >= generation_length:
        population += (power-1)*population
        for i in range((power-1)*len(creatures)):
            creatures.append(Creature())
            removeFood = True
            food = [Food() for _ in range (round(population * foodPerCreature))]
        spawn_timer = 0
    window.fill((0,0,0))

    for c in creatures:
        if c.life <= 0:
            creatures.remove(c)
            population -= 1
        else:
            c.update(dt)
            c.drawCreature(window)
            for f in food[:]:
                if c.creature.colliderect(f.rect):
                    c.life += round(c.colorVals/10)
                    food.remove(f)
    
    for f in food:
        if removeFood:
            food.remove(f)
        f.drawFood(window)
    print(population)
    
    pygame.display.update()