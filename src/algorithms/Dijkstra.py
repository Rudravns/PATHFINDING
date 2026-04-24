import heapq, pygame, time
from . import main



def dijkstra(grid):
    # Dijkstra's algorithm implementation
    steps = 0
    start = grid.get_start()
    goal = grid.get_goal()
    heap = [(0, start)]
    visited = set()
    parent = {}
    distances = {start: 0}

    while heap:
        main.stop_freeze()
        steps += 1  
        current_distance, current_node = heapq.heappop(heap)

        if current_node in visited:
            continue

        visited.add(current_node)

        # Visualize exploration
        y_offset = main.screen.get_height() - (main.rows * main.cell_size)
        if current_node != start and current_node != goal:
            rect = (current_node[1] * main.cell_size, current_node[0] * main.cell_size + y_offset, main.cell_size, main.cell_size)
            pygame.draw.rect(main.screen, 'red', rect)
            pygame.draw.rect(main.screen, 'black', rect, 1) # Draw border
            main.render_text(str(round(current_distance, 2)), (rect[0]+1, rect[1]+1), size=14, color="white")
            pygame.display.update() 
            time.sleep(main.interval)


        if current_node == goal:
            # Reconstruct the path
            path = []
            while current_node in parent:
                path.append(current_node)
                current_node = parent[current_node]
                
            path.append(start)
            path.reverse()
            # Visualize the path
            for pr, pc in path:
                if (pr, pc) == goal: continue
                rect = (pc * main.cell_size, pr * main.cell_size + y_offset, main.cell_size, main.cell_size)
                pygame.draw.rect(main.screen, 'green', rect)
                pygame.draw.rect(main.screen, 'black', rect, 1)
                main.render_text(str(round(distances[(pr,pc)],2)), (rect[0]+1, rect[1]+1), size=14, color="red")
                pygame.display.update()
                time.sleep(main.interval)
            while True:
                if main.keyboard_interrupt(): return path, steps

            

        for neighbor, weight in get_neighbors(current_node, grid):
            if neighbor not in visited:
                new_distance = current_distance + weight
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance # pyright: ignore[reportArgumentType]
                heapq.heappush(heap, (new_distance, neighbor))  # pyright: ignore[reportArgumentType]
                parent[neighbor] = current_node

    # No path found
    steps = 0
    return [], steps

def get_neighbors(node, grid):
    r, c = node

    for dr, dc in [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (1, 1), (-1, 1), (1, -1), (-1, -1)
    ]:
        nr, nc = r + dr, c + dc

        # bounds + wall check
        if not (0 <= nr < len(grid.grid) and 0 <= nc < len(grid.grid[0])):
            continue

        if grid.grid[nr][nc] == 1:
            continue

        # diagonal movement
        if dr != 0 and dc != 0:
            # prevent corner cutting
            if grid.grid[r][nc] == 1 or grid.grid[nr][c] == 1:
                continue

            weight = main.dijkstra_weights['diagonal']
        else:
            weight = main.dijkstra_weights['straight']

        weight = main.get_final_weights(weight, nr, nc) # Update weights in case of dynamic changes

        yield (nr, nc), weight