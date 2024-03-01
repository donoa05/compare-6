# pathfinding_algorithms.py
import heapq

def dijkstra(grid, start, goal):
    open_list = [(0, start)]
    came_from = {}
    cost = {(row, col): float('inf') for row in range(len(grid)) for col in range(len(grid[0]))}
    cost[start] = 0
    nodes_examined = 0  # Initialize counter for nodes examined

    while open_list:
        current_cost, current = heapq.heappop(open_list)
        nodes_examined += 1  # Increment counter for each node examined
        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            print("Nodes Examined (Dijkstra):", nodes_examined)  # Print number of nodes examined
            return path

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            neighbor = current[0] + dx, current[1] + dy

            if not (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0])):
                continue

            if grid[neighbor[0]][neighbor[1]] == 1:
                continue

            tentative_cost = cost[current] + 1

            if tentative_cost < cost[neighbor]:
                came_from[neighbor] = current
                cost[neighbor] = tentative_cost
                heapq.heappush(open_list, (cost[neighbor], neighbor))

    print("Nodes Examined (Dijkstra):", nodes_examined)  # Print number of nodes examined
    return []


def astar(grid, start, goal):
    open_list = [(0, start)]
    came_from = {}
    g_score = {(row, col): float('inf') for row in range(len(grid)) for col in range(len(grid[0]))}
    g_score[start] = 0
    f_score = {(row, col): float('inf') for row in range(len(grid)) for col in range(len(grid[0]))}
    f_score[start] = heuristic(start, goal)
    nodes_examined = 0  # Initialize counter for nodes examined

    while open_list:
        current_f, current = heapq.heappop(open_list)
        nodes_examined += 1  # Increment counter for each node examined
        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            print("Nodes Examined (A*):", nodes_examined)  # Print number of nodes examined
            return path

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

        for dx, dy in directions:
            neighbor = current[0] + dx, current[1] + dy

            if not (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0])):
                continue

            if grid[neighbor[0]][neighbor[1]] == 1:
                continue

            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    print("Nodes Examined (A*):", nodes_examined)  # Print number of nodes examined
    return []

def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path
