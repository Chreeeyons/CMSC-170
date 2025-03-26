import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600  #Window dimensions
ROWS, COLS = 20, 20  #Maze grid size
TILE_SIZE = min(WIDTH // COLS, HEIGHT // ROWS)  #Size of each tile in the grid
FPS = 60  #Frames per second for the game loop

# Colors (RGB format)
WHITE = (220, 220, 220)
BLACK = (20, 20, 20)
GREEN = (50, 205, 50)  #Player color
RED = (255, 69, 0)  #Exit color
GRID_COLOR = (60, 60, 60)  #Grid lines
ORANGE = (255, 165, 0)  #Exit portal highlight

# Movement directions (Right, Left, Down, Up)
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]  #Initialize all walls
        self.generate_maze()
    
    def generate_maze(self):
        """Generates a random maze using a depth-first search algorithm."""
        stack = [(0, 0)]  #Start from the top-left corner
        visited = set(stack)
        self.grid[0][0] = 0  #Mark the starting cell as open
        
        while stack:
            x, y = stack[-1]
            # Get unvisited neighbors two steps away
            neighbors = [(x+dx*2, y+dy*2) for dx, dy in DIRECTIONS 
                         if 0 <= x+dx*2 < self.cols and 0 <= y+dy*2 < self.rows 
                         and (x+dx*2, y+dy*2) not in visited]
            
            if neighbors:
                nx, ny = random.choice(neighbors)  #Pick a random neighbor
                self.grid[(y+ny)//2][(x+nx)//2] = 0  #Remove wall between current and chosen cell
                self.grid[ny][nx] = 0  #Open the chosen cell
                visited.add((nx, ny))
                stack.append((nx, ny))  #Move to the chosen cell
            else:
                stack.pop()  #Backtrack if no unvisited neighbors remain
        
        # Create an exit at the bottom-right corner
        self.grid[self.rows - 2][self.cols - 1] = 0
        self.grid[self.rows - 1][self.cols - 1] = 0  

    def draw(self, screen):
        """Draws the maze on the screen."""
        for y in range(self.rows):
            for x in range(self.cols):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, WHITE, rect)  #Draw walls
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)  #Draw grid lines
        
        #Draw the exit portal
        pygame.draw.rect(screen, RED, ((self.cols - 1) * TILE_SIZE, (self.rows - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, ORANGE, ((self.cols - 1) * TILE_SIZE + 4, (self.rows - 1) * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8))

class Player:
    def __init__(self, maze):
        """Initializes the player at the start of the maze."""
        self.x, self.y = 0, 0  #Player starts at the top-left corner
        self.maze = maze
    
    def move(self, dx, dy):
        """Moves the player if the destination cell is open."""
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < self.maze.cols and 0 <= ny < self.maze.rows and self.maze.grid[ny][nx] == 0:
            self.x, self.y = nx, ny  #Update player position
    
    def draw(self, screen):
        """Draws the player on the screen."""
        pygame.draw.rect(screen, GREEN, (self.x * TILE_SIZE + 4, self.y * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8))

def display_winning_animation(screen):
    """Displays a fade-in 'YOU WON!' animation when the player reaches the exit."""
    font = pygame.font.Font(None, 80)
    alpha = 0  #Transparency level
    fade_speed = 5  #Rate of fade-in effect
    clock = pygame.time.Clock()
    
    for _ in range(50):  #Animation duration loop
        screen.fill(BLACK)
        text = font.render("YOU WON!", True, (255, 255, 0))  #Winning text in yellow
        text.set_alpha(alpha)  #Apply transparency
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        alpha = min(alpha + fade_speed, 255)  #Increase transparency
        clock.tick(30)  #Control animation speed
    
    pygame.time.delay(1500)  #Pause before exiting the game

def main():
    """Main game loop that handles events, rendering, and updates."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  #Create game window
    pygame.display.set_caption("Maze Runner")
    clock = pygame.time.Clock()
    maze = Maze(ROWS, COLS)  #Create maze instance
    player = Player(maze)  #Create player instance
    running = True
    
    while running:
        screen.fill(BLACK)  #Clear screen
        maze.draw(screen)  #Draw maze
        player.draw(screen)  #Draw player
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #Check if the player closes the window
                running = False
        
        keys = pygame.key.get_pressed()  #Get pressed keys
        if keys[pygame.K_LEFT]:
            player.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0)
        if keys[pygame.K_UP]:
            player.move(0, -1)
        if keys[pygame.K_DOWN]:
            player.move(0, 1)
        
        # Check if the player has reached the exit
        if player.x == maze.cols - 1 and player.y == maze.rows - 1:
            display_winning_animation(screen)
            running = False  # End game loop
        
        pygame.display.flip()  #Refresh screen
        clock.tick(FPS)  #Maintain frame rate
    
    pygame.quit()  #Quit pygame

if __name__ == "__main__":
    main()
