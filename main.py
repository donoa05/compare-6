import pygame
import sys
import time
import random
from pathfinding_algorithms import dijkstra, astar
from pygame_utils import initialize_pygame, draw_grid, draw_path, draw_start_goal, display_message, update_display
from instructions_window import show_instructions

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cell_size = 25
        self.grid = [[0] * cols for _ in range(rows)]

    def reset(self):
        self.grid = [[0] * self.cols for _ in range(self.rows)]

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

class Graph:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.nodes = [[Node(row, col) for col in range(cols)] for row in range(rows)]
        self.build_graph()

    def build_graph(self):
        for row in range(self.rows):
            for col in range(self.cols):
                current_node = self.nodes[row][col]
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        current_node.add_neighbor(self.nodes[nr][nc])

class MazeGenerator:
    def __init__(self, graph):
        self.graph = graph

    def generate_maze(self):
        # Implement maze generation algorithm here
        pass

class PathfindingApp:
    def __init__(self):
        self.rows, self.cols = 25, 25
        self.grid = Grid(self.rows, self.cols)
        self.graph = Graph(self.rows, self.cols)
        self.maze_generator = MazeGenerator(self.graph)
        self.screen = initialize_pygame(self.rows, self.cols, self.grid.cell_size, "Pathfinding Comparison")
        self.running = True
        self.algorithm_started = False
        self.path = []
        self.start, self.goal = (0, 0), (self.rows - 1, self.cols - 1)
        self.placing_start, self.placing_goal, self.drawing_obstacle = False, False, False
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_button_down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.drawing_obstacle = False
            elif event.type == pygame.KEYDOWN:
                self.handle_key_down(event.key)

    def handle_mouse_button_down(self, pos):
        row, col = pos[1] // self.grid.cell_size, pos[0] // self.grid.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.grid.grid[row][col] == 0:
                if not self.placing_start and not self.placing_goal:
                    self.drawing_obstacle = True
                elif self.placing_start:
                    self.start = (row, col)
                    self.placing_start = False
                elif self.placing_goal:
                    self.goal = (row, col)
                    self.placing_goal = False

    def handle_key_down(self, key):
        key_functions = {
            pygame.K_s: self.toggle_placing_start,
            pygame.K_g: self.toggle_placing_goal,
            pygame.K_p: self.run_astar,
            pygame.K_d: self.run_dijkstra,
            pygame.K_r: self.reset_grid,
            pygame.K_i: show_instructions,
            pygame.K_m: self.generate_random_maze,
            pygame.K_q: sys.exit
        }
        if key in key_functions:
            key_functions[key]()

    def toggle_placing_start(self):
        self.placing_start = True

    def toggle_placing_goal(self):
        self.placing_goal = True

    def run_astar(self):
        self.run_algorithm(astar)

    def run_dijkstra(self):
        self.run_algorithm(dijkstra)

    def run_algorithm(self, algorithm):
        if not self.algorithm_started:
            self.algorithm_started = True
            start_time = time.time()
            if algorithm == astar:
                visited_nodes = astar(self.grid.grid, self.start, self.goal)
            elif algorithm == dijkstra:
                visited_nodes = dijkstra(self.grid.grid, self.start, self.goal)
            else:
                visited_nodes = []
            end_time = time.time()
            print(f"{algorithm.__name__}: {end_time - start_time}s, Nodes visited: {len(visited_nodes)}")
            self.path = visited_nodes


    def handle_drawing_obstacle(self):
        mouse_pos = pygame.mouse.get_pos()
        col = mouse_pos[0] // self.grid.cell_size
        row = mouse_pos[1] // self.grid.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid.grid[row][col] = 1

    def update_display(self):
        self.screen.fill((255, 255, 255))
        draw_grid(self.screen, self.grid.grid, self.grid.cell_size)

        if self.path and self.algorithm_started:
            draw_path(self.screen, self.path, self.grid.cell_size, (0, 255, 0))

        draw_start_goal(self.screen, self.start, self.goal, self.grid.cell_size)


        update_display()

    def reset_grid(self):
        self.grid.reset()
        self.path = []
        self.placing_start, self.placing_goal, self.algorithm_started = False, False, False

    def generate_random_maze(self):
        # Ensure the grid starts empty
        self.grid.reset()

        # Create at least two paths
        self.ensure_two_paths()

        # Add random obstacles
        for _ in range(random.randint(100, 500)):  # Random number of obstacles
            self.add_random_obstacle()

    def ensure_two_paths(self):
        # Generate two distinct paths without obstacles from start to goal
        # Path 1
        for i in range(self.rows):
            self.grid.grid[i][0] = 0  # Vertical path on the left
            self.grid.grid[0][i] = 0  # Horizontal path on the top

        # Path 2
        for i in range(self.rows):
            self.grid.grid[i][self.cols-1] = 0  # Vertical path on the right
            self.grid.grid[self.rows-1][i] = 0  # Horizontal path on the bottom

    def add_random_obstacle(self):
        row, col = random.randint(1, self.rows-2), random.randint(1, self.cols-2)
        # Ensure the cell is not part of the guaranteed paths
        if not ((row == 0 or col == 0) or (row == self.rows-1 or col == self.cols-1)):
            self.grid.grid[row][col] = 1

    @staticmethod
    def choose_orientation(width, height):
        if width < height:
            return 'H'
        elif height < width:
            return 'V'
        else:
            return 'H' if random.random() < 0.5 else 'V'

    def run(self):
        while self.running:
            self.handle_events()

            if self.drawing_obstacle:
                self.handle_drawing_obstacle()

            # Check if the user pressed 'r' to reset the grid
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.reset_grid()

            self.update_display()

            # Cap the frame rate to avoid excessive updates
            self.clock.tick(10)  # Adjust the value as needed

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    show_instructions()
    app = PathfindingApp()
    app.run()
