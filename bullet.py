
import pygame
from pygame import surface
from maze import CollideType
from colours import WHITE
from random import randint as randInt

class Bullet:
    def __init__(self, screen, pos, vel, ttl):
        self.pos = pos
        self.vel = vel
        self.ttl = ttl
        self.screen = screen
        self.name = "bullet"
        self.color = pygame.Color(randInt(200, 255), randInt(200, 255), randInt(200, 255))

    def collided_with(self, collide_type, obj):
        if obj.name == "ship":
            self.ttl = 0
            return
        if obj.name == "block":
            obj.active = False
            
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
        if (self.pos.x < 0):
            self.ttl = 0

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos, 3)

