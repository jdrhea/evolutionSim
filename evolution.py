import pygame
import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.SysFont('Gill Sans', 48)

class Creature:
    def __init__(self, clone_color = None, clone_size = None, clone_speed = None):
        self.switchDirection = False

        self.SS = 75
        self.Ss = 50
        self.ss = 25
        self.SizeGenotypes = [self.SS, self.Ss, self.ss]

        self.CC = 255
        self.Cc = 255
        self.cc = 25
        self.ColorGenotypes = [self.CC, self.Cc, self.cc]

        self.FF = 150
        self.Ff = 150
        self.ff = 300
        self.SpeedGenotypes = [self.FF, self.Ff, self.ff]

        isSexualReproduction = random.randint(0,1)

        if isSexualReproduction == 1:

            # sexual reproduction = randomized genetics

            self.speed = random.choice(self.SpeedGenotypes)
            self.size = random.choice(self.SizeGenotypes)
            self.colorVals = random.choice(self.ColorGenotypes)

        else:

            # asexual reproduction = exact clone

            if clone_speed is None:
                self.speed = random.choice(self.SpeedGenotypes)
            else:
                self.speed = clone_speed

            if clone_size is None:
                self.size = random.choice(self.SizeGenotypes)
            else:
                self.size = clone_size

            if clone_color is None:
                self.colorVals = random.choice(self.ColorGenotypes)
            else:
                self.colorVals = clone_color
        self.speed = max(25, self.speed)
        self.size = max(10, self.size)
        self.colorVals = max(25, self.colorVals)

            


        self.old_X_position = random.randint(0, SCREEN_WIDTH)
        self.old_Y_position = random.randint(0, SCREEN_HEIGHT)

        self.new_X_position = random.randint(0, SCREEN_WIDTH)
        self.new_Y_position = random.randint(0, SCREEN_HEIGHT)

        self.total_timeleftX = self.old_X_position - self.new_X_position
        self.total_timeleftY = self.old_Y_position - self.new_Y_position
        self.life = random.randint(1,12)
        
    def update (self, dt):
        if self.total_timeleftX > 0:
            self.total_timeleftX -= self.speed * dt
        elif self.total_timeleftX < 0:
            self.total_timeleftX += self.speed * dt
    
        if self.total_timeleftY > 0:
            self.total_timeleftY -= self.speed * dt
        elif self.total_timeleftY < 0:
            self.total_timeleftY += self.speed * dt
        
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
        self.FoodTypes = ["apple", "water"]
        self.Food = random.choice(self.FoodTypes)
        self.rect = pygame.Rect(self.positionX, self.positionY, 20, 20)
        
    def drawFood(self, window):
        if self.Food == "apple":
            pygame.draw.rect(window, (255, 0, 0), self.rect)
        else:
            pygame.draw.rect(window, (0, 0, 255), self.rect)
class Predators:

    def __init__(self):
        self.positionX = SCREEN_WIDTH
        self.positionY = random.randint(0,SCREEN_HEIGHT)
        

        self.new_X_position = 0
        self.new_Y_position = self.positionY

        self.total_timeleftX = self.positionX - self.new_X_position
        self.total_timeleftY = self.positionY - self.new_Y_position
        
        # Initialize rect here so it's always available
        self.rect = pygame.Rect(self.positionX, self.positionY, 100, 100)
    def update(self, dt):
        if self.total_timeleftX > 0:
            self.total_timeleftX -= 400 * dt
        elif self.total_timeleftX < 0:
            self.total_timeleftX += 400 * dt
    
        if self.total_timeleftY > 0:
            self.total_timeleftY -= 400 * dt
        elif self.total_timeleftY < 0:
            self.total_timeleftY += 400 * dt
        
        if abs(self.total_timeleftX) < 5:
            self.total_timeleftX = 0

        if abs(self.total_timeleftY) < 5:
            self.total_timeleftY = 0
    def drawPredator(self, window):
        current_x = self.new_X_position + self.total_timeleftX
        current_y = self.new_Y_position + self.total_timeleftY
        self.rect.x = current_x
        self.rect.y = current_y
        pygame.draw.rect(window, (255, 0, 0), self.rect)
        




global population
original_amount = 5
population = original_amount
  
creatures = [Creature() for _ in range (original_amount)]
foodPerCreature = 0.7
predatorToPrey = 0.1
food = [Food() for _ in range (round(population * foodPerCreature))]
spawn_timer = 0
predators = []

predator_timer = 0



    
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    
    dt = clock.tick(60) / 1000

    spawn_timer += dt
    predator_timer += dt
    generation_length = 5
    removeFood = False
    power = 2

    if spawn_timer >= generation_length:
        for i in range((power-1)*len(creatures)):
            creatures.append(Creature(clone_color=creatures[i].colorVals, clone_size=creatures[i].size))
            removeFood = True
            food = [Food() for _ in range (round(population * foodPerCreature))]
        spawn_timer = 0
    if predator_timer >= random.randint(5,15):
        predators.extend([Predators() for _ in range (round(predatorToPrey * population))])
        predator_timer = 0
    window.fill((0,0,0))

    for c in creatures[:]:
        if c.life <= 0:
            creatures.remove(c)
        else:
            c.update(dt)
            c.drawCreature(window)
            for f in food[:]:
                if c.creature.colliderect(f.rect):
                    c.life += round(c.size) / 10
                    food.remove(f)
            for p in predators[:]:
                if c.creature.colliderect(p.rect) and c.colorVals > random.randint(100,200):
                    creatures.remove(c)
    
    for f in food:
        if removeFood:
            food.remove(f)
        f.drawFood(window)
    for p in predators[:]:
        p.drawPredator(window)
        p.update(dt)
        if p.total_timeleftX == 0:
            predators.remove(p)
    population = len(creatures)
    average_size = sum(c.size for c in creatures) / len(creatures)
    average_speed = sum(c.speed for c in creatures) / len(creatures)
    average_color = (sum(c.colorVals for c in creatures) / len(creatures)) / 255
    PopulationCounter = font.render("Population: " + str(population), True, 'white')
    window.blit(PopulationCounter, (SCREEN_WIDTH - SCREEN_WIDTH/4,SCREEN_HEIGHT / 8))

    FoodtoCreature = font.render("Food:Creature: " + str(foodPerCreature), True, 'white')
    window.blit(FoodtoCreature, (SCREEN_WIDTH - SCREEN_WIDTH/3,SCREEN_HEIGHT / 4))

    average_size_counter = font.render("AverageSize: " + str(average_size), True, 'red')
    window.blit(average_size_counter, (SCREEN_WIDTH - SCREEN_WIDTH/3,5* SCREEN_HEIGHT / 8))

    average_speed_counter = font.render("AverageSpeed: " + str(average_speed), True, 'blue')
    window.blit(average_speed_counter, (SCREEN_WIDTH - SCREEN_WIDTH/3,3* SCREEN_HEIGHT / 4))

    average_color_counter = font.render("AverageColor: " + str(average_color), True, 'Yellow')
    window.blit(average_color_counter, (SCREEN_WIDTH - SCREEN_WIDTH/3,7* SCREEN_HEIGHT / 8))
    
    pygame.display.update()