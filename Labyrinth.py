import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 20, 20  # Maze dimensions
TILE_SIZE = min(WIDTH // COLS, HEIGHT // ROWS)
FPS = 60

# Colors
WHITE = (220, 220, 220)
BLACK = (20, 20, 20)
GREEN = (50, 205, 50)
RED = (255, 69, 0)
GRID_COLOR = (60, 60, 60)
ORANGE = (255, 165, 0)

# Directions (Right, Left, Down, Up)
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]
        self.generate_maze()
    
    def generate_maze(self):
        stack = [(0, 0)]
        visited = set(stack)
        self.grid[0][0] = 0  
        while stack:
            x, y = stack[-1]
            neighbors = [(x+dx*2, y+dy*2) for dx, dy in DIRECTIONS if 0 <= x+dx*2 < self.cols and 0 <= y+dy*2 < self.rows and (x+dx*2, y+dy*2) not in visited]
            if neighbors:
                nx, ny = random.choice(neighbors)
                self.grid[(y+ny)//2][(x+nx)//2] = 0  
                self.grid[ny][nx] = 0  
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()
        
        # Create an exit
        self.grid[self.rows - 2][self.cols - 1] = 0
        self.grid[self.rows - 1][self.cols - 1] = 0  

    def draw(self, screen):
        for y in range(self.rows):
            for x in range(self.cols):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)  

        # Draw exit portal
        pygame.draw.rect(screen, RED, ((self.cols - 1) * TILE_SIZE, (self.rows - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, ORANGE, ((self.cols - 1) * TILE_SIZE + 4, (self.rows - 1) * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8))

class Player:
    def __init__(self, maze):
        self.x, self.y = 0, 0
        self.maze = maze
    
    def move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < self.maze.cols and 0 <= ny < self.maze.rows and self.maze.grid[ny][nx] == 0:
            self.x, self.y = nx, ny
    
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x*TILE_SIZE+4, self.y*TILE_SIZE+4, TILE_SIZE-8, TILE_SIZE-8))

def display_winning_animation(screen):
    font = pygame.font.Font(None, 80)
    alpha = 0
    fade_speed = 5  
    clock = pygame.time.Clock()
    
    for _ in range(50):  # Animation duration
        screen.fill(BLACK)
        text = font.render("YOU WON!", True, (255, 255, 0))  
        text.set_alpha(alpha)  
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        alpha = min(alpha + fade_speed, 255)  
        clock.tick(30)
    
    pygame.time.delay(1500)  # Pause before quitting

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Runner")
    clock = pygame.time.Clock()
    maze = Maze(ROWS, COLS)
    player = Player(maze)
    running = True
    
    while running:
        screen.fill(BLACK)
        maze.draw(screen)
        player.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0)
        if keys[pygame.K_UP]:
            player.move(0, -1)
        if keys[pygame.K_DOWN]:
            player.move(0, 1)
        
        # Check if player reached exit
        if player.x == maze.cols - 1 and player.y == maze.rows - 1:
            display_winning_animation(screen)
            running = False  
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
