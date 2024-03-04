#maze_saver.py
import json

def save_maze(grid, filename):
    # Save the grid directly, assuming it's alrsdfeady in a format that can be serialized (e.g., a 2D list of integers)
    with open(filename, 'w') as file:
        json.dump(grid, file)

def load_maze(filename):
  # Load the grid from the specified file
  with open(filename, 'r') as file:
      grid_data = json.load(file)
  return grid_data
