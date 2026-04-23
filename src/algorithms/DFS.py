

import pygame, sys
import time
from . import main

def dfs(grid):
    visited = set()
    path = []
    goal = grid.get_goal()
    start = grid.get_start()

    if not start or not goal:
        return [], 0

    try:
        found, path, steps = dfs_recursive(start, visited, path, grid, goal, steps=[0])

        if found:
            y_offset = main.screen.get_height() - (main.rows * main.cell_size)
            for pr, pc in path:
                if (pr, pc) == goal:
                    continue

                rect = (
                    pc * main.cell_size,
                    pr * main.cell_size + y_offset,
                    main.cell_size,
                    main.cell_size
                )

                pygame.draw.rect(main.screen, 'green', rect)
                pygame.draw.rect(main.screen, 'black', rect, 1)
                pygame.display.update()
                time.sleep(main.interval)
            time.sleep(2)
            return path, steps[0]
        return [], 0

    except RecursionError:
        raise main.NoPathFoundError
    
def dfs_recursive(current, visited, path, grid, goal, steps):
    visited.add(current)
    path.append(current)
    steps[0] += 1

    # ---------------- VISUALIZATION ----------------
    main.stop_freeze()

    y_offset = main.screen.get_height() - (main.rows * main.cell_size)
    r, c = current

    if current != grid.get_start() and current != goal:
        rect = (
            c * main.cell_size,
            r * main.cell_size + y_offset,
            main.cell_size,
            main.cell_size
        )
        pygame.draw.rect(main.screen, 'red', rect)
        pygame.draw.rect(main.screen, 'black', rect, 1)
        pygame.display.update()
        if main.instant_visualization: time.sleep(main.interval) 
    # ------------------------------------------------

    # Goal check
    if current == goal:
        return True, path, steps

    # ---------------- DIRECTION BIAS (toward goal) ----------------
    dx = goal[1] - c
    dy = goal[0] - r

    directions = [
        (1 if dy > 0 else -1, 1 if dx > 0 else -1),  # diagonal toward goal
        (1 if dy > 0 else -1, 0),
        (0, 1 if dx > 0 else -1),

        (-1, 0), (1, 0),
        (0, -1), (0, 1),

        (1, 1), (-1, 1), (1, -1), (-1, -1)
    ]
    # ---------------------------------------------------------------

    # DFS exploration
    for dr, dc in directions:
        nr, nc = r + dr, c + dc

        if 0 <= nr < main.rows and 0 <= nc < main.cols:
            if grid.get_cell(nr, nc) != 1:

                # diagonal wall check (prevents cutting corners)
                if dr != 0 and dc != 0:
                    if grid.get_cell(r, nc) == 1 or grid.get_cell(nr, c) == 1:
                        continue

                neighbor = (nr, nc)

                if neighbor not in visited:
                    found, path, steps = dfs_recursive(
                        neighbor, visited, path, grid, goal, steps
                    )

                    if found:
                        return True, path, steps

    # Backtrack
    path.pop()
    return False, path, steps