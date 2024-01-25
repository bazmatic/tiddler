import pygame
import sys
import random
from ship import Ship
from colours import GREEN, RED, WHITE, BLACK
from maze import Maze

pygame.init()

history = []
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tiddler")
font = pygame.font.Font("./Hyperspace.ttf", 36)

# Set up the clock
clock = pygame.time.Clock()

game_state = []

class Asteroid:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)
        self.radius = random.randint(10, 50)
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-1, 1)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius)

# Create a Ship object
ship = Ship(screen, screen_width/2, screen_height/2)

# Create the Maze
maze = Maze(screen, 1200, 800, 40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.rotate_left()
    elif keys[pygame.K_RIGHT]:
        ship.rotate_right()
    else:
        ship.stop_rotating()

    if keys[pygame.K_UP]:
        ship.thrust()
    else:
        ship.stop_thrust()
    if keys[pygame.K_x]:
        if (not ship.firing):
            ship.fire()
    else:
        ship.stop_firing()
    
    # Draw the background
    screen.fill((0, 0, 0))
    score_text = font.render("Fuel " + str(ship.fuel), True, pygame.Color(GREEN))
    
    # Update the Ship
    ship.update()

    ship.handle_collision_with(maze)
    ship.handle_bullet_collisions_with(maze)
    
    maze.draw()
    ship.draw()
    screen.blit(score_text, (10, 10))

    pygame.display.flip()



