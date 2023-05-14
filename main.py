import pygame
import sys
import random
from maze import Maze, CollideType
from colours import GREEN, RED, WHITE, BLACK

pygame.init()

screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tiddler")

# Set up the clock
clock = pygame.time.Clock()

# Define some constants
SHIP_ROTATION_SPEED = 0.19
SHIP_THRUST_POWER = 0.0002
BULLET_TTL = 10000
MAX_SHIP_SPEED = 1
MAX_BULLETS = 10
MAZE_BLOCK_SIZE = 47

class Bullet:
    def __init__(self, pos, vel, ttl):
        self.pos = pos
        self.vel = vel
        self.ttl = ttl

    def collide(self, obj):
        collide_type = (obj.collide(self.pos.x, self.pos.y))
        self.bounce(collide_type)

    def bounce(self, collision_type):
        if collision_type == CollideType.TOP:
            self.vel.y = abs(self.vel.y)
        elif collision_type == CollideType.BOTTOM:
            self.vel.y = -abs(self.vel.y)
        elif collision_type == CollideType.LEFT:
            self.vel.x = abs(self.vel.x)
        elif collision_type == CollideType.RIGHT:
            self.vel.x = -abs(self.vel.x)

    def update(self):
        self.pos += self.vel
        self.ttl -= 1

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.pos, 3)

class Ship:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.max_speed = 5
        self.max_force = SHIP_THRUST_POWER
        self.thrusting = False
    
    def rotate_left(self):
        self.angle += SHIP_ROTATION_SPEED
    
    def rotate_right(self):
        self.angle -= SHIP_ROTATION_SPEED
    
    def thrust(self):
        thrust_force = pygame.math.Vector2(1, 0).rotate(-self.angle)
        self.acc += thrust_force * self.max_force
        # maximum speed
        if self.vel.length() > MAX_SHIP_SPEED:
            self.vel.scale_to_length(MAX_SHIP_SPEED)
        self.thrusting = True

    def slow(self):
        self.vel = self.vel - (self.vel * 0.0002)

    def bounce(self, collision_type):
        if collision_type == CollideType.TOP:
            self.vel.y = abs(self.vel.y)
        elif collision_type == CollideType.BOTTOM:
            self.vel.y = -abs(self.vel.y)
        elif collision_type == CollideType.LEFT:
            self.vel.x = abs(self.vel.x)
        elif collision_type == CollideType.RIGHT:
            self.vel.x = -abs(self.vel.x)

    def collide(self, obj):
        collide_type = (obj.collide(self.pos.x, self.pos.y))
        self.bounce(collide_type)

    def fire(self):
        bullet_pos = self.pos + pygame.math.Vector2(20, 0).rotate(-self.angle)
        bullet_vel = pygame.math.Vector2(10, 0).rotate(-self.angle) * 0.1
        bullet_ttl = BULLET_TTL
        bullets.append(Bullet(bullet_pos, bullet_vel, bullet_ttl))
        self.firing = True
        
    def update(self):
        self.vel += self.acc
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)
        self.pos += self.vel
        self.acc *= 0
        if self.pos.x < 0:
            self.pos.x = screen_width
        elif self.pos.x > screen_width:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = screen_height
        elif self.pos.y > screen_height:
            self.pos.y = 0
        self.slow()

    def draw(self):
        points = [pygame.math.Vector2(20, 0).rotate(-self.angle),
                  pygame.math.Vector2(-10, 10).rotate(-self.angle),
                  pygame.math.Vector2(-10, -10).rotate(-self.angle)]
        points = [p + self.pos for p in points]
        pygame.draw.polygon(screen, GREEN, points)
        if self.thrusting:
            jet_pos = pygame.math.Vector2(-10, 0).rotate(-self.angle) + self.pos
            pygame.draw.circle(screen, RED, jet_pos, 5)
            jet_pos = pygame.math.Vector2(-13, -5).rotate(-self.angle) + self.pos
            pygame.draw.circle(screen, RED, jet_pos, 3)
            jet_pos = pygame.math.Vector2(-13, 5).rotate(-self.angle) + self.pos
            pygame.draw.circle(screen, RED, jet_pos, 3)
            self.thrusting = False

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
ship = Ship(screen_width/2, screen_height/2)

# Create the Maze
maze = Maze(10, 10, 157)
maze.generate()

bullets = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.rotate_left()
    if keys[pygame.K_RIGHT]:
        ship.rotate_right()
    if keys[pygame.K_UP]:
        ship.thrust()
    if keys[pygame.K_x]:
        if (not ship.firing):
            ship.fire()
        ship.firing = True
    else:
        ship.firing = False
    
    # Draw the background
    screen.fill((0, 0, 0))
    
    # Update the Ship
    ship.update()
    ship.collide(maze)

    ship.draw()

    # Draw the Maze
    maze.draw(screen)
    
    for bullet in bullets:
        bullet.update()
        bullet.collide(maze)
        bullet.draw()
        if bullet.ttl == 0:
            bullets.remove(bullet)
    
    pygame.display.update()
