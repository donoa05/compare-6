# instructions_window.py
import pygame
from pygame_utils import initialize_pygame, display_message, update_display

def show_instructions():
    pygame.init()
    rows, cols = 15, 30
    cell_size = 25
    screen = initialize_pygame(rows, cols, cell_size, "Algorithm Instructions")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

        screen.fill((255, 255, 255))
        display_message(screen, "Algorithm Instructions", 36, (10, 10), (0, 0, 0))
        display_message(screen, "Press 's' to place start", 24, (10, 50), (0, 0, 0))
        display_message(screen, "Press 'g' to place goal", 24, (10, 80), (0, 0, 0))
        display_message(screen, "Press 'p' for A* algorithm", 24, (10, 110), (0, 0, 0))
        display_message(screen, "Press 'd' for Dijkstra's algorithm", 24, (10, 140), (0, 0, 0))
        display_message(screen, "Press 'r' to reset the grid", 24, (10, 170), (0, 0, 0))
        display_message(screen, "Press 'm' to generate a random maze", 24, (10, 200), (0, 0, 0))
        display_message(screen, "Press 'q' to close this window", 24, (10, 230), (0, 0, 0))

        update_display()

    pygame.quit()

