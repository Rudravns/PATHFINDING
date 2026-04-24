# Pathfinding Visualizer

An interactive Python tool to visualize various pathfinding algorithms on a 2D grid using Pygame.

## Features

- **Algorithms**: A*, Dijkstra, Breadth-First Search (BFS), and Depth-First Search (DFS).
- **Interactive Grid**: Draw walls, set start/end points, and clear the grid dynamically. Supports different terrain types like water with adjustable costs.
- **Map Building**: Generate random mazes using a recursive DFS algorithm.
- **Visualization Modes**: Toggle between step-by-step animation and instant result generation.
- **Real-time Metrics**: Displays path length, the total number of steps/explorations, and the cost (g_score) of explored nodes.

## Controls

| Input | Action |
| :--- | :--- |
| **Left Click** | Place nodes (Wall, Start, or End) |
| **Right Click** | Remove nodes (set to Empty) |
| **Scroll Wheel** | Cycle Node Types (Wall -> Start -> End) |
| **Middle Click / Tab** | Cycle through Pathfinding Algorithms |
| **Space** | Start the selected algorithm |
| **B** | Build Random Maze |
| **C** | Clear/Reset the grid |
| **ESC** | Quit application |

## Installation

1. Ensure you have Python 3.10 or higher installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the visualizer:
   ```bash
   python src/pathfinding/main.py
   ```

## Author
- Rudransh Kumar