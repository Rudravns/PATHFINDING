from . import main
import pygame, time, math, heapq

def greedy_best_first(grid):
    steps = 0
    start = grid.get_start()
    goal = grid.get_goal()
    heuristic = lambda a, b: math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)  # Euclidean distance is often better for grids with diagonals

    if not start or not goal:
        return [], 0

    # Greedy Best-First Search uses ONLY the heuristic for the priority queue
    # f(n) = h(n)
    heap = [(heuristic(start, goal), start)]
    visited = {start}
    parent = {}
    g_score = {start: 0}  # We keep track of g_score only for visualization/UI

    y_offset = main.screen.get_height() - (main.rows * main.cell_size)
    
    while heap:
        main.stop_freeze()
        steps += 1

        # Pop node with lowest heuristic value
        _, current = heapq.heappop(heap)

        # Goal reached
        if current == goal:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()

            # Visualize final path
            for pr, pc in path:
                if (pr, pc) == goal or (pr, pc) == start:
                    continue

                rect = (
                    pc * main.cell_size,
                    pr * main.cell_size + y_offset,
                    main.cell_size,
                    main.cell_size
                )

                pygame.draw.rect(main.screen, 'green', rect)
                pygame.draw.rect(main.screen, 'black', rect, 1)

                main.render_text(
                    str(round(g_score[(pr, pc)], 2)),
                    (rect[0] + 1, rect[1] + 1),
                    size=14,
                    color="red"
                )

                pygame.display.update()
                time.sleep(main.interval)

            while True:
                if main.keyboard_interrupt(): 
                    return path, steps

        # Visualization of exploration
        if current != start:
            rect = (
                current[1] * main.cell_size,
                current[0] * main.cell_size + y_offset,
                main.cell_size,
                main.cell_size
            )
            pygame.draw.rect(main.screen, 'red', rect)
            pygame.draw.rect(main.screen, 'black', rect, 1)
            main.render_text(
                str(round(g_score[current], 2)),
                (rect[0] + 1, rect[1] + 1),
                size=14,
                color="white"
            )
            pygame.display.update()
            time.sleep(main.interval)

        # Explore neighbors
        for neighbor, weight in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                g_score[neighbor] = g_score[current] + weight
                
                # Priority is strictly the distance to the goal
                priority = heuristic(neighbor, goal)
                heapq.heappush(heap, (priority, neighbor))

    return [], 0


   
    
def get_neighbors(node, grid):
    r, c = node

    for dr, dc in [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (1, 1), (-1, 1), (1, -1), (-1, -1)
    ]:
        nr, nc = r + dr, c + dc

        # bounds
        if not (0 <= nr < len(grid.grid) and 0 <= nc < len(grid.grid[0])):
            continue

        # wall
        if grid.grid[nr][nc] == 1:
            continue

        # diagonal check (no corner cutting)
        if dr != 0 and dc != 0:
            if grid.grid[r][nc] == 1 or grid.grid[nr][c] == 1:
                continue

        # Determine weight based on movement type (straight or diagonal)
        # Using main.dijkstra_weights for consistency with other algorithms
        if dr != 0 and dc != 0:
            # Diagonal movement
            weight = main.dijkstra_weights['diagonal']
        else:
            # Straight movement
            weight = main.dijkstra_weights['straight']

        weight = main.get_final_weights(weight, nr, nc) # Apply terrain-specific weights

        yield (nr, nc), weight