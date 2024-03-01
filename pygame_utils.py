# pygame_utils.py
import pygame


def initialize_pygame(rows, cols, cell_size, caption):
  pygame.init()
  screen = pygame.display.set_mode((cols * cell_size, rows * cell_size))
  pygame.display.set_caption(caption)
  return screen


def draw_grid(screen, grid, cell_size):
  for row in range(len(grid)):
    for col in range(len(grid[0])):
      color = (0, 0, 0) if grid[row][col] == 1 else (255, 255, 255)
      pygame.draw.rect(
          screen, color,
          (col * cell_size, row * cell_size, cell_size, cell_size))
      pygame.draw.rect(
          screen, (0, 0, 0),
          (col * cell_size, row * cell_size, cell_size, cell_size), 1)


def draw_path(screen, path, cell_size, color):
  for node in path:
    row, col = node
    pygame.draw.rect(screen, color,
                     (col * cell_size, row * cell_size, cell_size, cell_size))


def draw_start_goal(screen, start, goal, cell_size):
  pygame.draw.rect(
      screen, (255, 0, 0),
      (start[1] * cell_size, start[0] * cell_size, cell_size, cell_size))
  pygame.draw.rect(
      screen, (0, 0, 255),
      (goal[1] * cell_size, goal[0] * cell_size, cell_size, cell_size))


def display_message(screen, message, font_size, position, color):
  font = pygame.font.Font(None, font_size)
  text = font.render(message, True, color)
  screen.blit(text, position)


def update_display():
  pygame.display.flip()
