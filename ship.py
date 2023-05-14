import pygame
from bullet import Bullet
from maze import CollideType
from colours import RED, GREEN

# Define some constants
SHIP_ROTATION_SPEED = 0.19
SHIP_THRUST_POWER = 0.0002
BULLET_TTL = 10000
MAX_SHIP_SPEED = 1
MAX_BULLETS = 10
MAZE_BLOCK_SIZE = 47

class Ship:
    def __init__(self, screen, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.max_speed = 5
        self.max_force = SHIP_THRUST_POWER
        self.thrusting = False
        self.bullets = []
        self.screen = screen
    
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
        for bullet in self.bullets:
            bullet.collide(obj)

    def fire(self):
        bullet_pos = self.pos + pygame.math.Vector2(20, 0).rotate(-self.angle)
        bullet_vel = pygame.math.Vector2(10, 0).rotate(-self.angle) * 0.1
        bullet_ttl = BULLET_TTL
        self.bullets.append(Bullet(self.screen, bullet_pos, bullet_vel, bullet_ttl))
        self.firing = True
        
    def update(self):
        self.vel += self.acc
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)
        self.pos += self.vel
        self.acc *= 0
        #if self.pos.x < 0:
        #    self.pos.x = screen_width
        #elif self.pos.x > screen_width:
        #   self.pos.x = 0
        #if self.pos.y < 0:
        #    self.pos.y = screen_height
        #elif self.pos.y > screen_height:
        #    self.pos.y = 0
        self.slow()

        for bullet in self.bullets:
            bullet.update()
            bullet.draw()
            if bullet.ttl == 0:
                self.bullets.remove(bullet)

    def draw(self):
        points = [pygame.math.Vector2(20, 0).rotate(-self.angle),
                  pygame.math.Vector2(-10, 10).rotate(-self.angle),
                  pygame.math.Vector2(-10, -10).rotate(-self.angle)]
        points = [p + self.pos for p in points]
        pygame.draw.polygon(self.screen, GREEN, points)
        if self.thrusting:
            jet_pos = pygame.math.Vector2(-10, 0).rotate(-self.angle) + self.pos
            pygame.draw.circle(self.screen, RED, jet_pos, 5)
            jet_pos = pygame.math.Vector2(-13, -5).rotate(-self.angle) + self.pos
            pygame.draw.circle(self.screen, RED, jet_pos, 3)
            jet_pos = pygame.math.Vector2(-13, 5).rotate(-self.angle) + self.pos
            pygame.draw.circle(self.screen, RED, jet_pos, 3)
            self.thrusting = False
