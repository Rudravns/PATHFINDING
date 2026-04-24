import sys, os, pygame

from utility import quick_quit, render_text
from grid import Grid

# Add src directory to path so we can import local modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import algorithms

class PathfindingVisualizer:
    def __init__(self):
        #init
        pygame.init()
        

        self.screen = pygame.display.set_mode((1300, 700))
        pygame.display.set_caption("Pathfinding Visualizer")
        self.clock = pygame.time.Clock()
        
        
        # 17 rows * 40 = 680px. Fits within 700px height.
        self.map = Grid(35, 40, 20)  
        algorithms.init(self.map)
        

        self.type = 1


    def run(self):
        # Horizontal boundary for UI
        grid_width = self.map.cols * self.map.cell_size; grid_height = self.map.rows * self.map.cell_size
        # Vertical offset to align grid to the bottom (700 - 680 = 20)
        y_offset = self.screen.get_height() - (self.map.rows * self.map.cell_size)

        # Padding rectangle for the top area
        pad_rect = pygame.Rect(0, 0, grid_width, y_offset)
        path = []; steps = 0

        while True:
            self.screen.fill((255, 255, 255))  # Clear the screen with white background
            self.clock.tick(120)  # Limit to 120 frames per second
            self.map.draw(self.screen, y_offset)

            self.draw_UI(grid_width, path, steps)
            self.handle_mouse(y_offset)

            #draw a black line right bewtween the hight of window and hight of grid
            pygame.draw.rect(self.screen, "black", pad_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   quick_quit()
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quick_quit()
                    elif event.key == pygame.K_c:
                        self.map.reset()
                    elif event.key == pygame.K_b:
                        algorithms.build_maze()

                    if event.key == pygame.K_SPACE:
                        try:
                            path, steps = algorithms.run()
                            print("Path found:", path)
                        except algorithms.NoPathFoundError:
                            render_text("No path found", (grid_width + 20, 170), size=24, color="red", surface=self.screen)
                    if event.key == pygame.K_TAB:
                        # Cycle through pathfinding algorithms using modulus
                        new_index = (algorithms.Pathfinding_Algorithm_index + 1) % len(algorithms.Pathfinding_Algorithm_types)
                        algorithms.set_algorithm(new_index)
                        algorithms.Pathfinding_Algorithm_index = new_index

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  #Scroll Up
                        self.type = (self.type % 3) + 1
                    elif event.button == 5:  # Scroll Down
                        self.type = ((self.type - 2) % 3) + 1
                    elif event.button == 2:  # Middle click
                        # Cycle through pathfinding algorithms using modulus
                        new_index = (algorithms.Pathfinding_Algorithm_index + 1) % len(algorithms.Pathfinding_Algorithm_types)
                        algorithms.set_algorithm(new_index)
                        algorithms.Pathfinding_Algorithm_index = new_index


            pygame.display.flip()  # Update the display

    def draw_UI(self, grid_width, path=[], steps=0):
        # Draw vertical line using the actual screen height
        pygame.draw.line(self.screen, "black", (grid_width, 0), (grid_width, self.screen.get_height()), 3) 
        render_text("Pathfinding Visualizer", (grid_width + 20, 20), size=30, color="black", surface=self.screen)
        render_text(f"Node Type: {self.map.key[self.type]}", (grid_width + 20, 70), size=24, color="black", surface=self.screen)
        render_text(f"Algorithm: {algorithms.Pathfinding_Algorithm_types[algorithms.Pathfinding_Algorithm_index]}", (grid_width + 20, 120), size=24, color="black", surface=self.screen)
        render_text(f"Path_length: {len(path)}, Total Steps: {steps}", (grid_width + 20, 170), size=24, color="black", surface=self.screen)
        render_text(f"Path: {path[:8]}", (grid_width + 20, 220), size=18, color="black", surface=self.screen)
        if len(path) > 8:
            for i in range(len(path) // 8):
                render_text(str((path[i*8:(i+1)*8]))+ (", ..." if i == 2 else ""), (grid_width + 20, 220 + (i + 1) * 20), size=18, color="black", surface=self.screen)
                if i == 2: break # Limit to 5 lines of path display
        
        # Instructions
        y_padding = 40
        inst_start = 300
        render_text("Instructions:", (grid_width + 20, inst_start), size=24, color="black", surface=self.screen)
        render_text("- Left click: Place nodes", (grid_width + 20, inst_start + y_padding), size=20, color="black", surface=self.screen)
        render_text("- Right click: Remove nodes", (grid_width + 20, inst_start + 2 * y_padding), size=20, color="black", surface=self.screen)
        render_text("- Middle click or 'TAB': Cycle Algorithm", (grid_width + 20, inst_start + 3 * y_padding), size=20, color="black", surface=self.screen)
        render_text("- Scroll: Cycle Node Types", (grid_width + 20, inst_start + 4 * y_padding), size=20, color="black", surface=self.screen)
        render_text("- 'C': Clear grid", (grid_width + 20, inst_start + 5 * y_padding), size=20, color="black", surface=self.screen)
        render_text("- 'Space': Start pathfinding", (grid_width + 20, inst_start + 6 * y_padding), size=20, color="black", surface=self.screen)
        render_text("- 'B': Build Maze", (grid_width + 20, inst_start + 7 * y_padding), size=20, color="black", surface=self.screen)
        render_text("- 'ESC': Quit", (grid_width + 20, inst_start + 8 * y_padding), size=20, color="black", surface=self.screen)
        
        # FPS
        render_text(f"FPS: {int(self.clock.get_fps())}", (grid_width + 20, 670), size=24, color="black", surface=self.screen)

    def handle_mouse(self, y_offset):
        mouse_pos = pygame.mouse.get_pos()
        col = mouse_pos[0] // self.map.cell_size
        row = (mouse_pos[1] - y_offset) // self.map.cell_size
        
        # Ensure coordinates are within grid boundaries before updating cells
        if 0 <= row < self.map.rows and 0 <= col < self.map.cols:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                self.map.set_cell(row, col, self.type)
            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                self.map.set_cell(row, col, 0)  # Set to empty
        

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

    visualizer = PathfindingVisualizer()
    visualizer.run()

            