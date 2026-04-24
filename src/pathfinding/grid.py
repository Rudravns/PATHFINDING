import pygame
import numpy as np #faster array mapping and manipulation

class Grid:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = np.zeros((rows, cols), dtype=int)  
        self.set_cell(0, 0, 2)  # Start point at top-left
        self.set_cell(self.rows - 1, self.cols - 1, 3)  # End point at bottom-right
        self.key = {
            0: "Empty",
            1: "Wall",
            2: "Start",
            3: "End"
        }


    def draw(self, screen, offset_y=0):
        for row in range(self.rows):
            for col in range(self.cols):
                cell_value = self.grid[row, col]
                color = (255, 255, 255)  # Default to white
                if cell_value == 1:
                    color = (0, 0, 0)  # Wall - black
                elif cell_value == 2:
                    color = (0, 255, 0)  # Start - green
                elif cell_value == 3:
                    color = (0, 0, 255)  # End - BLUE
                pygame.draw.rect(screen, color, (col * self.cell_size, row * self.cell_size + offset_y, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, "black", (col * self.cell_size, row * self.cell_size + offset_y, self.cell_size, self.cell_size), 1)  # Cell border

    def set_cell(self, row, col, value):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            # Ensure only one Start (2) or End (3) exists
            if value == 2 or value == 3:
                self.grid[self.grid == value] = 0
            
            self.grid[row, col] = value

            
    def get_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row, col]
        return None
    
    def get_start(self):
        start_pos = np.argwhere(self.grid == 2)
        return tuple(start_pos[0]) if start_pos.size > 0 else None

    def get_goal(self):
        goal_pos = np.argwhere(self.grid == 3)
        return tuple(goal_pos[0]) if goal_pos.size > 0 else None

    def reset(self):
        self.grid.fill(0)  # Reset the grid to all zeros
        #set start and end points to default
        self.set_cell(0, 0, 2)  # Start point at top-left
        self.set_cell(self.rows - 1, self.cols - 1, 3)  # End point at bottom-right
    
    def __len__(self):
        return self.grid.shape[0]