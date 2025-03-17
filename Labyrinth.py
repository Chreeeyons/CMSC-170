import pygame
import random
import heapq
from collections import deque

# Constants
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 20, 20  # Maze dimensions
TILE_SIZE = WIDTH // COLS
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Directions (Right, Left, Down, Up)
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]  # 1 = wall, 0 = path
        self.generate_maze()
    
    def generate_maze(self):
        stack = [(0, 0)]
        visited = set(stack)
        self.grid[0][0] = 0  # Start position
        while stack:
            x, y = stack[-1]
            neighbors = [(x+dx*2, y+dy*2) for dx, dy in DIRECTIONS if 0 <= x+dx*2 < self.cols and 0 <= y+dy*2 < self.rows and (x+dx*2, y+dy*2) not in visited]
            if neighbors:
                nx, ny = random.choice(neighbors)
                self.grid[(y+ny)//2][(x+nx)//2] = 0  # Remove wall
                self.grid[ny][nx] = 0  # Set new path
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

    def draw(self, screen):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, WHITE, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

class Player:
    def __init__(self, maze):
        self.x, self.y = 0, 0
        self.maze = maze
    
    def move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < self.maze.cols and 0 <= ny < self.maze.rows and self.maze.grid[ny][nx] == 0:
            self.x, self.y = nx, ny
    
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x*TILE_SIZE, self.y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

class AI:
    def __init__(self, maze):
        self.x, self.y = 0, 0
        self.maze = maze
        self.path = []
        self.find_path()
    
    def find_path(self):
        start = (0, 0)
        goal = (self.maze.cols-1, self.maze.rows-1)
        queue = deque([(start, [])])
        visited = set()
        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == goal:
                self.path = path
                return
            visited.add((x, y))
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.maze.cols and 0 <= ny < self.maze.rows and self.maze.grid[ny][nx] == 0 and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))
    
    def move(self):
        if self.path:
            self.x, self.y = self.path.pop(0)
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x*TILE_SIZE, self.y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    maze = Maze(ROWS, COLS)
    player = Player(maze)
    ai = AI(maze)
    running = True
    
    while running:
        screen.fill(BLACK)
        maze.draw(screen)
        player.draw(screen)
        ai.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0)
                elif event.key == pygame.K_UP:
                    player.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1)
        
        ai.move()
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
