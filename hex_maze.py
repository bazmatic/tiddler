import random
import pygame
from pygame import Surface

# Enum of collide types: 0 = no collision, 1 = top, 2 = bottom, 3 = left, 4 = right, 5 = top-left, 6 = top-right, 7 = bottom-left, 8 = bottom-right
class CollideType:
    NONE = 0
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
    TOP_LEFT = 5
    TOP_RIGHT = 6
    BOTTOM_LEFT = 7
    BOTTOM_RIGHT = 8

class Maze:
    def __init__(self, rows, cols, cell_size=100):
        self.cell_size = cell_size
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell(r, c, cell_size) for c in range(cols)] for r in range(rows)]

    def __str__(self):
        output = ""
        for row in self.grid:
            for cell in row:
                output += str(cell)
            output += "\n"
        return output
    
    def draw(self, surface):
        for row in self.grid:
            for cell in row:
                cell.draw(surface)

    # Return true if the point (x, y) is within COLLISION_DIST of a cell wall

    def collide(self, x, y):
        COLLISION_DIST = 8
        row = int(y / self.cell_size)
        col = int(x / self.cell_size)
        cell = self.grid[row][col]
        if cell.walls.top and abs(y - row*self.cell_size) < COLLISION_DIST:
            return CollideType.TOP
        if cell.walls.bottom and abs(y - (row+1)*self.cell_size) < COLLISION_DIST:
            return CollideType.BOTTOM
        if cell.walls.left and abs(x - col*self.cell_size) < COLLISION_DIST:
            return CollideType.LEFT
        if cell.walls.right and abs(x - (col+1)*self.cell_size) < COLLISION_DIST:
            return CollideType.RIGHT
        if cell.walls.top_left and abs(y - row*self.cell_size) < COLLISION_DIST and abs(x - col*self.cell_size) < COLLISION_DIST:
            return CollideType.TOP_LEFT
        if cell.walls.top_right and abs(y - row*self.cell_size) < COLLISION_DIST and abs(x - (col+1)*self.cell_size) < COLLISION_DIST:
            return CollideType.TOP_RIGHT
        if cell.walls.bottom_left and abs(y - (row+1)*self.cell_size) < COLLISION_DIST and abs(x - col*self.cell_size) < COLLISION_DIST:
            return CollideType.BOTTOM_LEFT
        if cell.walls.bottom_right and abs(y - (row+1)*self.cell_size) < COLLISION_DIST and abs(x - (col+1)*self.cell_size) < COLLISION_DIST:
            return CollideType.BOTTOM_RIGHT
        return False

    def generate(self):
        start_row = random.randint(0, self.rows - 1)
        start_col = random.randint(0, self.cols - 1)
        self._generate_recursive(start_row, start_col)

    def _generate_recursive(self, row, col):
        cell = self.grid[row][col]
        cell.visited = True

        # Randomly shuffle the neighbors
        neighbors = []
        if row > 0 and not self.grid[row-1][col].visited:  # Up
            neighbors.append((row-1, col))
        if row < self.rows-1 and not self.grid[row+1][col].visited:  # Down
            neighbors.append((row+1, col))
        if col > 0 and not self.grid[row][col-1].visited:  # Left
            neighbors.append((row, col-1))
       
class Cell:
    def __init__(self, row, col, cell_size=20):
        self.row = row
        self.col = col
        self.visited = False
        #self.top = True
        #self.bottom = True
        #self.left = True
        #self.right = True
        self.cell_size = cell_size
        # walls is a dictionary of booleans
        self.walls = {
            "top": True,
            "bottom": True,
            "left": True,
            "right": True,
            "top_left": True,
            "top_right": True,
            "bottom_left": True,
            "bottom_right": True,
        }

    
    def draw(self, surface):
        for wall in self.walls:
            if self.walls[wall]:
                pygame.draw.line(surface, (255, 255, 255), (self.col*self.cell_size, self.row*self.cell_size), ((self.col+1)*self.cell_size, self.row*self.cell_size))