import pygame
import os
import sys
import time
import random
from pathfinding_algorithms import dijkstra, astar
from pygame_utils import initialize_pygame, draw_grid, draw_path, draw_start_goal, display_message, update_display
from instructions_window import show_instructions
from maze_saver import save_maze, load_maze


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
class NullAlgorithm(MazeGenerator):
  def __init__(self, graph):
      super().__init__(graph)

  def generate_maze(self):
      print("NullAlgorithm: Generating maze...") 
        
      # This algorithm does very little, just print a message
      pass
class PathfindingApp:
    def __init__(self, grid_size):
      self.grid_size = grid_size  # Store the grid size
      self.rows, self.cols = grid_size, grid_size
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
      self.show_instructions = False
      self.instruction_screen = None
      self.instruction_toggle_pressed = False

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
                  
    def save_current_maze(self):
      # Prompt the user for a filename in the console
      filename = self.ask_text_input("Enter a filename for the maze (without extension): ") + '.json'
      save_maze(self.grid.grid, filename)
      print(f"Maze saved to '{filename}'.")

    def load_current_maze(self):
      filename = self.ask_text_input("Enter the filename for the maze (without extension): ") + '.json'
      if not os.path.exists(filename):
          print(f"File '{filename}' not found. Please save a maze first.")
          return
  
      loaded_grid_data = load_maze(filename)
      rows = len(loaded_grid_data)  # Assuming square grid
      cols = len(loaded_grid_data[0]) if rows > 0 else 0
      self.grid = Grid(rows, cols)  # Re-initialize the grid with the correct dimensions
      self.grid.grid = loaded_grid_data  # Directly set the loaded grid data
  
      print(f"Maze loaded from '{filename}'.")
    # Refresh the display or perform other necessary updates


    def handle_key_down(self, key):
        key_functions = {
            pygame.K_s: self.toggle_placing_start,
            pygame.K_g: self.toggle_placing_goal,
            pygame.K_p: self.run_astar,
            pygame.K_d: self.run_dijkstra,
            pygame.K_r: self.reset_grid,
            pygame.K_i: self.toggle_instructions,
            pygame.K_m: self.generate_random_maze,
            pygame.K_q: sys.exit,
            pygame.K_z: self.save_current_maze,
            pygame.K_l: self.load_current_maze,
        }
        if key in key_functions:
            key_functions[key]()
          
    def toggle_instructions(self):
        if not self.instruction_toggle_pressed:
          self.show_instructions = not self.show_instructions
          self.instruction_toggle_pressed = True
        else:
          self.instruction_toggle_pressed = False
      
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
        num_obstacles = int(self.rows * self.cols * 0.2)
        # Add random obstacles
        for _ in range(num_obstacles):  # Random number of obstacles
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

    def ask_text_input(self, prompt):
      # Define the text input box and colors
      input_box = pygame.Rect(100, 200, 300, 32)
      color_inactive = pygame.Color('lightskyblue3')
      color_active = pygame.Color('dodgerblue2')
      color = color_inactive
      active = False
      text = ''
  
      while True:
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()
              if event.type == pygame.MOUSEBUTTONDOWN:
                  # Toggle activation of the input box
                  if input_box.collidepoint(event.pos):
                      active = not active
                  else:
                      active = False
                  color = color_active if active else color_inactive
              if event.type == pygame.KEYDOWN:
                  # If input box is active, handle key events
                  if active:
                      if event.key == pygame.K_RETURN:
                          return text
                      elif event.key == pygame.K_BACKSPACE:
                          text = text[:-1]
                      else:
                          text += event.unicode
  
          # Fill the screen with background color
          self.screen.fill((30, 30, 30))
  
          # Render the prompt message
          display_message(self.screen, prompt, 24, (100, 150), (255, 255, 255))
  
          # Render the input box
          txt_surface = pygame.font.Font(None, 32).render(text, True, color)
          width = max(300, txt_surface.get_width() + 10)
          input_box.w = width
          self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
          pygame.draw.rect(self.screen, color, input_box, 2)
  
          pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()

            if self.show_instructions:
              if not self.instruction_screen:
                self.instruction_screen = initialize_pygame(15, 30, 25, "Algorithm Instructions")
                show_instructions(self.grid_size)
            else:
              if self.instruction_screen:
                  pygame.quit()
                  self.instruction_screen = None
                  self.screen = initialize_pygame(self.rows, self.cols, self.grid.cell_size, "Pathfinding Comparison")
              
            
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




class BaseWindow:
    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.font = pygame.font.Font(None, 32)
        self.font_color = (0, 0, 0)

    def display_message(self, message, font_size, position):
        text = self.font.render(message, True, self.font_color)
        text_rect = text.get_rect(center=position)
        self.screen.blit(text, text_rect)

    def update_display(self):
        pygame.display.flip()

class GridSizeSelectionWindow(BaseWindow):
    def __init__(self):
        super().__init__("Grid Size Selection", 400, 300)
        self.selected_size = None
        self.sizes = [15, 20, 25, 30]

    def run(self):
      running = True
      while running and self.selected_size is None:
          self.screen.fill((255, 255, 255))
          self.display_message("Select Grid Size", 36, (self.width // 2, 50))

          for i, size in enumerate(self.sizes):
              self.display_message(f"{size}x{size}", 24, (self.width // 2, 120 + i * 40))

          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  running = False
              elif event.type == pygame.MOUSEBUTTONDOWN:
                  mouse_x, mouse_y = pygame.mouse.get_pos()
                  for i, _ in enumerate(self.sizes):
                      if 150 + i * 40 <= mouse_y <= 150 + (i + 1) * 40:
                          self.selected_size = self.sizes[i]
                          break

          self.update_display()

      pygame.quit()
      return self.selected_size

if __name__ == "__main__":
  pygame.init()
  window = GridSizeSelectionWindow()
  selected_size = window.run()
  if selected_size:
      show_instructions(selected_size)  # If you still want to show instructions, pass the grid size here
      app = PathfindingApp(selected_size)  # Pass the selected size to PathfindingApp
      app.run()





