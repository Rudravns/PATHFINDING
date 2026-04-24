import pygame, sys
import time
from collections import deque
from . import main

def bfs(grid):
    visited = set()
    parent = {}
    steps = 0
    
    goal = grid.get_goal()
    start = grid.get_start()
    
    if not start or not goal:
        return []

    queue = deque([start])
    visited.add(start)

    while queue:
        main.stop_freeze()

        # Dynamically calculate offset in case window resized or init delayed
        y_offset = main.screen.get_height() - (main.rows * main.cell_size)
        
        current = queue.popleft()
        r, c = current

        # Visualize exploration (skip drawing over the start/end nodes)
        if current != start and current != goal:
            rect = (c * main.cell_size, r * main.cell_size + y_offset, main.cell_size, main.cell_size)
            pygame.draw.rect(main.screen, 'red', rect)
            pygame.draw.rect(main.screen, 'black', rect, 1) # Draw border
            pygame.display.update()
            time.sleep(main.interval)

        if current == goal:
            path = []
            temp = current
            while temp in parent:
                path.append(temp)
                temp = parent[temp]
            path.reverse() 
            
            for pr, pc in path:
                if (pr, pc) == goal: continue
                rect = (pc * main.cell_size, pr * main.cell_size + y_offset, main.cell_size, main.cell_size)
                pygame.draw.rect(main.screen, 'green', rect)
                pygame.draw.rect(main.screen, 'black', rect, 1)
                pygame.display.update()
                time.sleep(main.interval)
            while True:
                if main.keyboard_interrupt(): return path, steps
  

        # Neighbors: Up, Down, Left, Right, and Diagonals
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            nr, nc = r + dr, c + dc
            steps += 1

            if 0 <= nr < main.rows and 0 <= nc < main.cols:
                cell_val = grid.get_cell(nr, nc)
                
                if cell_val == 1: # Wall
                    continue
                    
                # Check for corner-cutting over walls during diagonal movement
                if dr != 0 and dc != 0:
                    if grid.get_cell(r, nc) == 1 or grid.get_cell(nr, c) == 1:
                        continue
                    
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = current
                    queue.append((nr, nc))

    raise main.NoPathFoundError