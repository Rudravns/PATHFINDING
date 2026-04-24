import pygame, sys
import time
from . import main

def dfs(grid):
    # Increase recursion limit for deep exploration on larger grids
    sys.setrecursionlimit(5000)
    
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
            while True:
                if main.keyboard_interrupt(): return path, steps[0]

        return [], 0

    except RecursionError:
        raise main.NoPathFoundError
    
def dfs_recursive(current, visited, path, grid, goal, steps):
    visited.add(current)
    path.append(current)
    steps[0] += 1

    # ---------------- VISUALIZATION (like BFS) ----------------
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
        time.sleep(main.interval)
    # ----------------------------------------------------------

    # Goal check
    if current == goal:
        return True, path, steps

    # Build neighbors
    neighbors = []
    for dr, dc in [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (1, 1), (-1, 1), (1, -1), (-1, -1)
    ]:
        nr, nc = r + dr, c + dc

        if 0 <= nr < main.rows and 0 <= nc < main.cols:
            if grid.get_cell(nr, nc) != 1:

                # diagonal wall check
                if dr != 0 and dc != 0:
                    if grid.get_cell(r, nc) == 1 or grid.get_cell(nr, c) == 1:
                        continue

                neighbors.append((nr, nc))

    # DFS exploration
    for neighbor in neighbors:
        if neighbor not in visited:
            found, path, steps = dfs_recursive(
                neighbor, visited, path, grid, goal, steps
            )

            if found:
                return True, path, steps

    # Backtrack
    path.pop()
    return False, path, steps