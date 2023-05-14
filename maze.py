import random
import pygame
from pygame import Surface

# Enum of collide types: 0 = no collision, 1 = top, 2 = bottom, 3 = left, 4 = right
class CollideType:
    NONE = 0
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4

class Maze:
    def __init__(self, screen, rows, cols, cell_size=100):
        self.screen = screen
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
    
    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw(self.screen)

    # Return true if the point (x, y) is within COLLISION_DIST of a cell wall

    def collide(self, x, y):
        COLLISION_DIST = 8
        row = int(y / self.cell_size)
        col = int(x / self.cell_size)
        cell = self.grid[row][col]
        if cell.top and abs(y - row*self.cell_size) < COLLISION_DIST:
            return CollideType.TOP
        if cell.bottom and abs(y - (row+1)*self.cell_size) < COLLISION_DIST:
            return CollideType.BOTTOM
        if cell.left and abs(x - col*self.cell_size) < COLLISION_DIST:
            return CollideType.LEFT
        if cell.right and abs(x - (col+1)*self.cell_size) < COLLISION_DIST:
            return CollideType.RIGHT
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
        if col < self.cols-1 and not self.grid[row][col+1].visited:  # Right
            neighbors.append((row, col+1))
        random.shuffle(neighbors)

        # Recursive call for each unvisited neighbor
        for neighbor_row, neighbor_col in neighbors:
            neighbor_cell = self.grid[neighbor_row][neighbor_col]
            if not neighbor_cell.visited:
                if neighbor_row == row - 1:  # Up
                    cell.top = False
                    neighbor_cell.bottom = False
                elif neighbor_row == row + 1:  # Down
                    cell.bottom = False
                    neighbor_cell.top = False
                elif neighbor_col == col - 1:  # Left
                    cell.left = False
                    neighbor_cell.right = False
                elif neighbor_col == col + 1:  # Right
                    cell.right = False
                    neighbor_cell.left = False
                self._generate_recursive(neighbor_row, neighbor_col)


class Cell:
    def __init__(self, row, col, cell_size=20):
        self.row = row
        self.col = col
        self.visited = False
        self.top = True
        self.bottom = True
        self.left = True
        self.right = True
        self.cell_size = cell_size

    def draw(self, surface):
        if self.top:
            pygame.draw.line(surface, (255, 255, 255), (self.col*self.cell_size, self.row*self.cell_size), ((self.col+1)*self.cell_size, self.row*self.cell_size))
        if self.bottom:
            pygame.draw.line(surface, (255, 255, 255), (self.col*self.cell_size, (self.row+1)*self.cell_size), ((self.col+1)*self.cell_size, (self.row+1)*self.cell_size))
        if self.left:
            pygame.draw.line(surface, (255, 255, 255), (self.col*self.cell_size, self.row*self.cell_size), (self.col*self.cell_size, (self.row+1)*self.cell_size))
        if self.right:
            pygame.draw.line(surface, (255, 255, 255), ((self.col+1)*self.cell_size, self.row*self.cell_size), ((self.col+1)*self.cell_size, (self.row+1)*self.cell_size))
    

    def __str__(self):
        output = "+"
        output += "-" if self.top else " "
        output += "+\n"
        output += "|" if self.left else " "
        output += " "  # This space is for the player
        output += "|" if self.right else " "
        output += "\n+"
        output += "-" if self.bottom else " "
        output += "+"
        return output
