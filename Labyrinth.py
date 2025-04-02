import pygame
import random
from collections import deque

# Constants
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 20, 20
TILE_SIZE = min(WIDTH // COLS, HEIGHT // ROWS)
FPS = 60
FOG_RADIUS = 3

# Colors
WHITE = (220, 220, 220)
BLACK = (20, 20, 20)
GREEN = (50, 205, 50)
BLUE = (30, 144, 255)
RED = (255, 69, 0)
GRID_COLOR = (60, 60, 60)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
VIOLET = (138, 43, 226)  # Reveal Power-Up Color

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]
        self.generate_maze()
        self.power_ups = self.generate_power_ups()

    def generate_maze(self):
        stack = [(0, 0)]
        visited = set(stack)
        self.grid[0][0] = 0

        while stack:
            x, y = stack[-1]
            neighbors = [(x + dx * 2, y + dy * 2) for dx, dy in DIRECTIONS
                         if 0 <= x + dx * 2 < self.cols and 0 <= y + dy * 2 < self.rows
                         and (x + dx * 2, y + dy * 2) not in visited]

            if neighbors:
                nx, ny = random.choice(neighbors)
                self.grid[(y + ny) // 2][(x + nx) // 2] = 0
                self.grid[ny][nx] = 0
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        self.grid[self.rows - 2][self.cols - 1] = 0
        self.grid[self.rows - 1][self.cols - 1] = 0

    def generate_power_ups(self):
        power_ups = []
        for _ in range(5):
            while True:
                x, y = random.randint(0, self.cols - 1), random.randint(0, self.rows - 1)
                if self.grid[y][x] == 0 and (x, y) not in [(0, 0), (self.cols - 1, self.rows - 1)]:
                    power_ups.append((x, y, random.choice([YELLOW, BROWN, VIOLET])))
                    break
        return power_ups

    def draw(self, screen, player):
        for y in range(self.rows):
            for x in range(self.cols):
                # If reveal_timer is active, show the entire map
                if player.reveal_timer > 0:
                    visible = True
                else:
                    # Otherwise, use the visibility radius
                    visible = abs(x - player.x) + abs(y - player.y) <= FOG_RADIUS

                if visible:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.grid[y][x] == 1:
                        pygame.draw.rect(screen, WHITE, rect)
                    pygame.draw.rect(screen, GRID_COLOR, rect, 1)

        # Draw the exit point
        pygame.draw.rect(screen, RED, ((self.cols - 1) * TILE_SIZE, (self.rows - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Draw power-ups
        for px, py, color in self.power_ups:
            pygame.draw.rect(screen, color, (px * TILE_SIZE + 6, py * TILE_SIZE + 6, TILE_SIZE - 12, TILE_SIZE - 12))


class Player:
    def __init__(self, maze, color):
        self.x, self.y = 0, 0
        self.maze = maze
        self.color = color
        self.speed_boost = 0
        self.move_delay = 0
        self.reveal_timer = 0

    def move(self, dx, dy):
        if self.move_delay > 0:
            self.move_delay -= 1
            return

        move_speed = 2 if self.speed_boost > 0 else 1

        for _ in range(move_speed):
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < self.maze.cols and 0 <= ny < self.maze.rows and self.maze.grid[ny][nx] == 0:
                self.x, self.y = nx, ny
                self.move_delay = 3

                for i, (px, py, color) in enumerate(self.maze.power_ups):
                    if (self.x, self.y) == (px, py):
                        if color == YELLOW:
                            self.speed_boost = FPS * 2
                        elif color == BROWN and hasattr(self.maze, 'ai'):
                            self.maze.ai.slow_down = FPS * 2
                        elif color == VIOLET:
                            self.reveal_timer = FPS * 3.5

                        self.maze.power_ups.pop(i)
                        break

    def update(self):
        if self.reveal_timer > 0:
            self.reveal_timer -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x * TILE_SIZE + 4, self.y * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8))


class AI(Player):
    def __init__(self, maze):
        super().__init__(maze, BLUE)
        self.slow_down = 0
        self.path = self.find_path()
        self.move_delay = 10

    def find_path(self):
        queue = deque([(self.x, self.y)])
        visited = {(self.x, self.y): None}

        while queue:
            x, y = queue.popleft()
            if (x, y) == (self.maze.cols - 1, self.maze.rows - 1):
                path = []
                while visited[(x, y)] is not None:
                    path.append((x, y))
                    x, y = visited[(x, y)]
                return path[::-1]

            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.maze.cols and 0 <= ny < self.maze.rows and self.maze.grid[ny][nx] == 0 and (nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited[(nx, ny)] = (x, y)
        return []

    def move_ai(self):
        if self.slow_down > 0:
            self.slow_down -= 1
        elif self.move_delay == 0:
            if not self.path or (self.x, self.y) != self.path[0]:
                self.path = self.find_path()
            if self.path:
                self.x, self.y = self.path.pop(0)
            self.move_delay = 15
        else:
            self.move_delay -= 1


def display_message(screen, message):
    font = pygame.font.Font(None, 72)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill(BLACK)
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Labyrinth")
    clock = pygame.time.Clock()

    maze = Maze(ROWS, COLS)
    player = Player(maze, GREEN)
    ai = AI(maze)
    maze.ai = ai

    running = True
    while running:
        screen.fill(BLACK)
        maze.draw(screen, player)
        player.draw(screen)
        ai.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player.move(-1, 0)
        if keys[pygame.K_RIGHT]: player.move(1, 0)
        if keys[pygame.K_UP]: player.move(0, -1)
        if keys[pygame.K_DOWN]: player.move(0, 1)

        player.update()
        ai.move_ai()

        if (player.x, player.y) == (COLS - 1, ROWS - 1) and (ai.x, ai.y) == (COLS - 1, ROWS - 1):
            display_message(screen, "DRAW!")
            break
        elif (ai.x, ai.y) == (COLS - 1, ROWS - 1):
            display_message(screen, "YOU LOST!")
            break
        elif (player.x, player.y) == (COLS - 1, ROWS - 1):
            display_message(screen, "YOU WIN!")
            break

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()