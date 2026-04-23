import pygame, sys, os
import numpy as np
# Add src directory to path so we can import local modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import algorithms.BFS as BFS
import algorithms.A_star as A_star
import algorithms.Dijkstra as Dijkstra
import algorithms.DFS as DFS


#setting-ish thing
Pathfinding_Algorithm_types = ["A*", "Dijkstra", "Breadth-First Search",
                                "Depth-First Search"]

interval = 0.001 #in seconds, time between each step of the pathfinding algorithm, lower is faster but more intensive on CPU
instant_visualization = True
screen:pygame.Surface = None # pyright: ignore[reportAssignmentType]
Grid = None
rows = 0
cols = 0
cell_size = 0
Pathfinding_Algorithm_index = 0


#init
def init(grid):
    global screen, Grid, rows, cols, cell_size
    screen = pygame.display.get_surface()  # pyright: ignore[reportAssignmentType]
    Grid = grid
    rows = grid.rows
    cols = grid.cols
    cell_size = grid.cell_size

def set_algorithm(index):
    global Pathfinding_Algorithm_index
    Pathfinding_Algorithm_index = index

#decorator for the path to be converted into python list
def path_to_list(func):
    def wrapper(*args, **kwargs):
        path,stps = func(*args, **kwargs)
        return [tuple(item) for item in np.array(path).tolist()], stps
    return wrapper

#runner
@path_to_list
def run():
    global Pathfinding_Algorithm_index, Grid
    match Pathfinding_Algorithm_types[Pathfinding_Algorithm_index]:
        case "Breadth-First Search":
            return BFS.bfs(Grid) # pyright: ignore[reportOptionalMemberAccess]
        case "A*":
            return  A_star.a_star(Grid) # pyright: ignore[reportOptionalMemberAccess]
        case "Dijkstra":
            return  Dijkstra.dijkstra(Grid) # pyright: ignore[reportOptionalMemberAccess]
        case "Depth-First Search":
            return  DFS.dfs(Grid) # pyright: ignore[reportOptionalMemberAccess]
        case _:
            raise InvalidAlgorithmError

def quick_quit():   
    pygame.quit()
    sys.exit()

def stop_freeze():
    global interval
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quick_quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quick_quit()



#exceptions
class NoPathFoundError(Exception):
    """Custom exception for when an account has insufficient funds."""

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

class InvalidAlgorithmError(Exception):
    """Custom exception for when an account has insufficient funds."""

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)