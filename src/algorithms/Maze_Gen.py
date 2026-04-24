from . import main
import random, pygame, time

def connect_to_maze(pos, grid):
    """Ensures a specific node is connected to the carved maze paths."""
    r, c = pos
    # Check immediate neighbors to see if we're already touching an open path (0)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < grid.rows and 0 <= nc < grid.cols:
            if grid.grid[nr, nc] == 0:
                return # Already connected to the maze
    
    # If isolated, force one valid neighbor to be a path
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < grid.rows and 0 <= nc < grid.cols:
            grid.grid[nr, nc] = 0
            return



def generate_maze(grid):
    #  Save start & goal 
    start = grid.get_start()
    goal = grid.get_goal()

    #  Fill everything as walls 
    grid.grid.fill(1)

    #  Choose a valid DFS start (odd coords near start) 
    sr, sc = start if start else (1, 1)

    # Force to odd indices
    sr = sr if sr % 2 == 1 else sr + 1
    sc = sc if sc % 2 == 1 else sc + 1

    sr = min(sr, grid.rows - 2)
    sc = min(sc, grid.cols - 2)

    dfs_recursive((sr, sc), set(), grid)

    #  Add loops (MULTIPLE PATHS) 
    add_loops(grid, chance=main.loop_chance)

    #  Restore start & goal safely 
    if start:
        grid.set_cell(start[0], start[1], 2)
        connect_to_maze(start, grid)

    if goal:
        grid.set_cell(goal[0], goal[1], 3)
        connect_to_maze(goal, grid)


def dfs_recursive(current, visited, grid):
    visited.add(current)
    r, c = current

    grid.grid[r, c] = 0

    # - VISUALIZATION -
    main.stop_freeze() #stop the window from freezing during maze generation, which can take a while for larger mazes

    y_offset = main.screen.get_height() - (main.rows * main.cell_size)

    rect = (
        c * main.cell_size,
        r * main.cell_size + y_offset,
        main.cell_size,
        main.cell_size
    )
    pygame.draw.rect(main.screen, 'orange', rect)
    pygame.draw.rect(main.screen, 'black', rect, 1)
    pygame.display.update()
    time.sleep(main.interval)
    # 

    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    random.shuffle(directions)

    for dr, dc in directions:
        nr, nc = r + dr, c + dc

        if 0 <= nr < grid.rows and 0 <= nc < grid.cols:
            if (nr, nc) not in visited:

                wall_r = r + dr // 2
                wall_c = c + dc // 2

                grid.grid[wall_r, wall_c] = 0
                grid.grid[nr, nc] = 0

                dfs_recursive((nr, nc), visited, grid)


#Add loops (multiple paths)
def add_loops(grid, chance=0.08):
    """
    Chance controls how many walls are removed to create loops.\n:
    0.02 -> mostly perfect maze (harder) \n
    0.08 -> balanced (normal)\n
    0.15+ -> very open / easy\n
    """
    for r in range(1, grid.rows - 1):
        for c in range(1, grid.cols - 1):

            if grid.grid[r, c] == 1:  # wall
                if random.random() < chance:

                    # Only break walls that connect paths
                    neighbors = 0
                    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                        if grid.grid[r + dr, c + dc] == 0:
                            neighbors += 1

                    if neighbors >= 2:
                        grid.grid[r, c] = 0