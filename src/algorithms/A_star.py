import heapq, pygame, time, math
from . import main


def a_star(grid):
    steps = 0
    start = grid.get_start()
    goal = grid.get_goal()

    if not start or not goal:
        return [], 0

    heap = [(heuristic(start, goal), start)] # (f_score, node)
    visited = set()
    parent = {}

    g_score = {start: 0} # actual cost from start to current node

    while heap:
        main.stop_freeze()
        steps += 1

        current_f, current = heapq.heappop(heap) # node with lowest f_score

        if current in visited:
            continue

        visited.add(current)

        # ---------------- VISUALIZATION ----------------
        y_offset = main.screen.get_height() - (main.rows * main.cell_size)

        if current != start and current != goal:
            rect = (
                current[1] * main.cell_size,
                current[0] * main.cell_size + y_offset,
                main.cell_size,
                main.cell_size
            )

            pygame.draw.rect(main.screen, 'red', rect)
            pygame.draw.rect(main.screen, 'black', rect, 1)

            # show g_score (actual distance)
            main.render_text(
                str(round(g_score[current], 2)),
                (rect[0] + 1, rect[1] + 1),
                size=14,
                color="white"
            )

            pygame.display.update()
            time.sleep(main.interval)
        # ------------------------------------------------

        # Goal reached
        if current == goal:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current] # backtrack to start

            path.append(start)
            path.reverse()

            # draw final path
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

        # Explore neighbors
        for neighbor, weight in get_neighbors(current, grid):

            if neighbor in visited:
                continue

            tentative_g = g_score[current] + weight # actual cost to reach neighbor through current

            if neighbor not in g_score or tentative_g < g_score[neighbor]: # better path to neighbor found
                g_score[neighbor] = tentative_g

                f_score = tentative_g + heuristic(neighbor, goal)

                heapq.heappush(heap, (f_score, neighbor))
                parent[neighbor] = current

    # No path found
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
            # using Dijkstra's weights for consistency in path cost calculation
            weight = main.dijkstra_weights['diagonal'] 
        else:
            weight = main.dijkstra_weights['straight']

        yield (nr, nc), weight


def heuristic(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])

    # Euclidean distance (best for diagonal movement)
    return math.sqrt(dx * dx + dy * dy)