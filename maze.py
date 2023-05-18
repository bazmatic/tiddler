import random
from pygame import Surface, Color, draw


# Enum of collide types: 0 = no collision, 1 = top, 2 = bottom, 3 = left, 4 = right
class CollideType:
    NONE = 0
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4

# Block class
class Block:
    def __init__(self, parent, surface, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.surface = surface
        self.active = True
        self.name = "block"
        self.hp = random.randint(100, 255)

    def draw(self):
        # Draw the block on the given surface
        if self.active:
            energy = int(self.hp)
            color = Color(energy, energy, energy)
            draw.circle(self.surface, color, (self.x + self.size/2, self.y + self.size/2), self.size/2)
            #Surface.fill(self.surface,color, (self.x+1, self.y+1, self.size-1, self.size-1))
            if self.hp <= 0:
                self.active = False

    def get_collision_type(self, position):

        # Check if the given position collides with this block
        # and return the collision type
        if self.active == False:
            return CollideType.NONE
        
        if position.x >= self.x and position.x <= self.x + self.size:
            if position.y >= self.y and position.y <= self.y + self.size:              
               # Random collision type
                return random.randint(1, 4)
            
        return CollideType.NONE

    def collided_with(self, collision_type, obj):
        pass
            

# Maze class
class Maze:
    def __init__(self, screen, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.blocks = []
        self.surface = screen
        self.generate()

    def generate(self):
        # Generate random blocks for the maze
        for x in range(0, self.width, self.block_size):
            for y in range(0, self.height, self.block_size):
                if random.random() < 0.1:  # Adjust the probability as desired
                    block = Block(self, self.surface, x, y, self.block_size)
                    self.blocks.append(block)
    def draw(self):
        # Draw all the blocks of the maze on the given surface
        for block in self.blocks:
            block.draw()

    def get_collision(self, obj):
        # Check for collision at the given position
        position = obj.pos
        for block in self.blocks:
            collision_type = block.get_collision_type(position)
            if collision_type != CollideType.NONE:
                return collision_type, block
        return CollideType.NONE, None
