import pygame
import random

# Constants
SCREEN_SIZE = 600
GRID_SIZE = 20
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Directions
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# Maze generation using Depth-First Search
def generate_maze(grid_size):
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    stack = [(0, 0)]
    visited = set((0, 0))

    while stack:
        current = stack[-1]
        x, y = current
        grid[y][x] = 1  # Mark the cell as part of the maze

        # Shuffle directions to create a more random maze
        random.shuffle(DIRECTIONS)
        for direction in DIRECTIONS:
            nx, ny = x + direction[0], y + direction[1]
            if 0 <= nx < grid_size and 0 <= ny < grid_size and (nx, ny) not in visited:
                stack.append((nx, ny))
                visited.add((nx, ny))
                break
        else:
            stack.pop()

    # Mark the entrance and exit
    grid[0][0] = 1
    grid[grid_size-1][grid_size-1] = 1
    return grid

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

# Generate maze
maze = generate_maze(GRID_SIZE)

# Player position
player_pos = [0, 0]

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_pos[1] -= 1
            elif event.key == pygame.K_DOWN:
                player_pos[1] += 1
            elif event.key == pygame.K_LEFT:
                player_pos[0] -= 1
            elif event.key == pygame.K_RIGHT:
                player_pos[0] += 1

    # Constrain player within the maze
    player_pos[0] = max(0, min(player_pos[0], GRID_SIZE-1))
    player_pos[1] = max(0, min(player_pos[1], GRID_SIZE-1))

    # Draw maze
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw player
    pygame.draw.rect(screen, RED, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Check for win
    if player_pos == [GRID_SIZE-1, GRID_SIZE-1]:
        font = pygame.font.SysFont(None, 74)
        text = font.render("You Win!", True, GREEN)
        screen.blit(text, (SCREEN_SIZE//4, SCREEN_SIZE//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
