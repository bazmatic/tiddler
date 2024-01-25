import pygame
from bullet import Bullet
from maze import CollideType
from colours import RED, GREEN
from random import randint

# Define some constants
SHIP_ROTATION_SPEED = 0.19
SHIP_THRUST_POWER = 0.0003
BULLET_TTL = 2000
MAX_SHIP_SPEED = 1
MAX_BULLETS = 10
MAZE_BLOCK_SIZE = 47
SHIP_SIZE = 4
MAX_FUEL = 10000


class RotateType:
    NONE = 0
    LEFT = 1
    RIGHT = 2

class Ship:
    def __init__(self, screen, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.max_speed = 5
        self.max_force = SHIP_THRUST_POWER
        self.thrusting = False
        self.rotation = RotateType.NONE
        self.eating = False
        self.bullets = []
        self.screen = screen
        self.name = "ship"
        self.fuel = MAX_FUEL
        pygame.mixer.init()
        self.fire_sound = pygame.mixer.Sound("fire.mp3")
        self.fire_sound.set_volume(0.1)
        self.thrust_sound = pygame.mixer.Sound("thruster.mp3")
        self.eating_sound = pygame.mixer.Sound("eating.mp3")
    
    def rotate_left(self):
        self.angle += SHIP_ROTATION_SPEED
        self.rotation = RotateType.LEFT
    
    def rotate_right(self):
        self.angle -= SHIP_ROTATION_SPEED
        self.rotatiion = RotateType.RIGHT

    def stop_rotating(self):
        self.rotating = RotateType.NONE
    
    def thrust(self):
        if self.fuel <= 0:
            return
        thrust_force = pygame.math.Vector2(1, 0).rotate(-self.angle)
        self.acc += thrust_force * self.max_force
        # maximum speed
        if self.vel.length() > MAX_SHIP_SPEED:
            self.vel.scale_to_length(MAX_SHIP_SPEED)
        if self.thrusting == False:
            self.thrust_sound.play(99)
        self.thrusting = True
    
    def stop_thrust(self):
        self.thrusting = False
        self.thrust_sound.fadeout(100)

    def slow(self, amount=1):
        self.vel -= self.vel * (0.0001 * amount)

    def collided_with(self, collision_type, obj):
        if (obj.name == "block"):
            self.eat_block(obj)
            return
        if (obj.name == "bullet"):
            if (collision_type == CollideType.NONE):
                return
            if collision_type == CollideType.TOP:
                self.vel.y = abs(self.vel.y)
            elif collision_type == CollideType.BOTTOM:
                self.vel.y = -abs(self.vel.y)
            elif collision_type == CollideType.LEFT:
                self.vel.x = abs(self.vel.x)
            elif collision_type == CollideType.RIGHT:
                self.vel.x = -abs(self.vel.x)
        print("Ship collided with " + str(collision_type))

    def handle_collision_with(self, obj):
        (collide_type, struck_object) = obj.get_collision(self)
        
        if struck_object:
            self.collided_with(collide_type, struck_object)
            struck_object.collided_with(collide_type, self)
        else:
            self.stop_eating()

    def handle_bullet_collisions_with(self, obj):
        for bullet in self.bullets:
            (collide_type, struck_object) = obj.get_collision(bullet)
            
            if struck_object:
                bullet.collided_with(collide_type, struck_object)
                struck_object.collided_with(collide_type, bullet) 

    def eat_block(self, block):
        if block.hp >= 2:
            if self.eating == False:
                self.eating = True
                self.eating_sound.play()

            block.hp -= 1
            self.fuel += 10
        else:
            self.stop_eating()

    def stop_eating(self):
        self.eating = False
        self.eating_sound.fadeout(300)

    def bounce(self, collision_type):
        if collision_type == CollideType.TOP:
            self.vel.y = abs(self.vel.y)
        elif collision_type == CollideType.BOTTOM:
            self.vel.y = -abs(self.vel.y)
        elif collision_type == CollideType.LEFT:
            self.vel.x = abs(self.vel.x)
        elif collision_type == CollideType.RIGHT:
            self.vel.x = -abs(self.vel.x)

    def fire(self):
        bullet_pos = self.pos + pygame.math.Vector2(20, 0).rotate(-self.angle)
        bullet_vel = pygame.math.Vector2(10, 0).rotate(-self.angle) * 0.1
        self.bullets.append(Bullet(self.screen, bullet_pos, bullet_vel, BULLET_TTL))
        self.firing = True
        self.fire_sound.play()

    def stop_firing(self):
        self.firing = False
        
    def update(self):
        self.vel += self.acc
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)
        self.pos += self.vel
        self.acc *= 0
        if self.pos.x < 0:
            self.bounce(CollideType.LEFT)
        elif self.pos.x > self.screen.get_width():
           self.bounce(CollideType.RIGHT)
        if self.pos.y < 0:
            self.bounce(CollideType.TOP)
        elif self.pos.y > self.screen.get_height():
            self.bounce(CollideType.BOTTOM)
        self.slow()

        for bullet in self.bullets:
            bullet.update()
            bullet.draw()
            if bullet.ttl == 0:
                self.bullets.remove(bullet)

    def draw(self):
        points = [pygame.math.Vector2(SHIP_SIZE * 2, 0).rotate(-self.angle),
                  pygame.math.Vector2(-SHIP_SIZE, SHIP_SIZE).rotate(-self.angle),
                  pygame.math.Vector2(-SHIP_SIZE, -SHIP_SIZE).rotate(-self.angle)]
        points = [p + self.pos for p in points]
        # Ship is duller as it loses fuel
        fuel_fraction = min(self.fuel, MAX_FUEL) / MAX_FUEL
        #print(fuel_fraction)
        if self.eating:
            colour = pygame.Color(randint(200,255), randint(200,255), randint(200,255))
        else:
            colour = pygame.Color(255, int(255 * fuel_fraction), int(120 * fuel_fraction))
        pygame.draw.polygon(self.screen, colour, points)
        if self.thrusting:
            self.fuel -= 1
            jet_pos = pygame.math.Vector2(-10, 0).rotate(-self.angle) + self.pos
            pygame.draw.circle(self.screen, self.flame_colour(), jet_pos, 5)
            jet_pos = pygame.math.Vector2(-13, -5).rotate(-self.angle) + self.pos
            pygame.draw.circle(self.screen, self.flame_colour(0.5), jet_pos, 3)
            jet_pos = pygame.math.Vector2(-13, 5).rotate(-self.angle) + self.pos
            pygame.draw.circle(self.screen, self.flame_colour(0.5), jet_pos, 3)
        
 
    def flame_colour(self, brightness=1):
        r = 255
        g = randint(0, 255)
        b = randint(0, 255)
        r = int(r * brightness)
        g = int(g * brightness)
        b = int(b * brightness)
 
        return pygame.Color(r, g, b)
    
    def get_state(self): 
        return {
            "rotation": self.rotation,        
            "pos": self.pos,
            "vel": self.vel,
            "acc": self.acc,
            "angle": self.angle,
            "fuel": self.fuel,
            "max_speed": self.max_speed,
            "thrusting": self.thrusting,
            "firing": self.firing,
            "eating": self.eating,
            #"bullets": [bullet.get_state() for bullet in self.bullets]
        }
    
