
import pygame
from pygame import surface
from maze import CollideType
from colours import WHITE

class Bullet:
    def __init__(self, screen, pos, vel, ttl):
        self.pos = pos
        self.vel = vel
        self.ttl = ttl
        self.screen = screen

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
        pygame.draw.circle(self.screen, WHITE, self.pos, 3)

