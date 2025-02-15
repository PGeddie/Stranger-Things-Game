import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 803, 550
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stranger Things Maze Escape Game")

# Load images
try:
    wall_img = pygame.image.load("images/wall.png")
    player_img = pygame.image.load("images/player.png")
    exit_img = pygame.image.load("images/exit.png")
    obstacle_img = pygame.image.load("images/obstacle.png")

    # Scale images to fit tiles
    tile_size = 50
    wall_img = pygame.transform.scale(wall_img, (tile_size, tile_size))
    player_img = pygame.transform.scale(player_img, (tile_size - 10, tile_size - 10))
    exit_img = pygame.transform.scale(exit_img, (tile_size, tile_size))
    obstacle_img = pygame.transform.scale(obstacle_img, (tile_size, tile_size))
except pygame.error as e:
    print("Error loading images:", e)
    sys.exit()

# Load sounds
try:
    win_sound = pygame.mixer.Sound("sounds/win.wav")
    pygame.mixer.music.load("sounds/background.mp3")
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print("Error loading sounds:", e)
    sys.exit()

# Load background image
try:
    background_img = pygame.image.load("images/background.png")
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print("Error loading background image:", e)
    sys.exit()

# Define multiple levels as lists of strings
levels = [
  [
        "#################",
        "#S     #      E#",
        "# ####  # O ## #",
        "# O     #      #",
        "### ######## # #",
        "#   # O   #    #",
        "## ## ### # ####",
        "#              #",
        "### ### ##### ###",
        "#     O   #    #",
        "#################",
    ],
    [
        "#################",
        "#S #       #   E#",
        "# ## ### O### # #",
        "#   O      #    #",
        "### ######## ## #",
        "#   #   O       #",
        "## ## ### O######",
        "#       O      #",
        "###O### ##### ###",
        "#               #",
        "#################",
    ],
    [
    "#################",
    "#S    #   O    #",
    "## # ## O ###  #",
    "#        #  # O#",
    "#### ###O####  #",
    "#       O      #",
    "# O### ### ######",
    "#   #  O     E #",
    "## ##  ### ### #",
    "#              #",
    "#################",
],  
[
    "################",
    "#S     #     O #",
    "# ###  # ##  ###",
    "# # O  #   ##  #",
    "# # ### ########",
    "#     O       E#",
    "# ###O##### ####",
    "#        O   # #",
    "## # ### ### ## #",
    "#     O        #",
    "################",
],
[
    "################",
    "#S    #O     # #",
    "# ## ### ### # #",
    "#        O      #",
    "##O### ### # # #",
    "#   O       #  #",
    "## #######O###E#",
    "#      O   #   #",
    "# ## ###   ## ##",
    "# O      O     #",
    "################",
]
]

# Set initial game variables
current_level = 0
player_x, player_y = 1, 1
key_press_handled = False

# Function to load a specific level
def load_level(level_index):
    global maze, player_x, player_y
    maze = levels[level_index]
    
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == "S":
                player_x, player_y = x, y  # Set player start position
            elif tile == "E":
                exit_position = (x, y)  # Set exit position
    return exit_position

# Load the first level
exit_position = load_level(current_level)

# Function to draw the maze
def draw_maze():
    for row_idx, row in enumerate(maze):
        for col_idx, tile in enumerate(row):
            x, y = col_idx * tile_size, row_idx * tile_size
            if tile == "#":
                screen.blit(wall_img, (x, y))
            elif tile == "O":
                screen.blit(obstacle_img, (x, y))
            elif tile == "E":
                screen.blit(exit_img, (x, y))

# Check for collisions with walls or obstacles
def can_move(new_x, new_y):
    if new_x < 0 or new_y < 0 or new_x >= len(maze[0]) or new_y >= len(maze):
        return False
    if maze[new_y][new_x] in ["#", "O"]:
        return False
    return True

# Check for level completion and load the next level if completed
def check_for_level_completion():
    global current_level, exit_position
    if (player_x, player_y) == exit_position:
        win_sound.play()
        pygame.time.delay(1000)  # Pause briefly to celebrate
        current_level += 1
        if current_level < len(levels):
            exit_position = load_level(current_level)  # Load the next level
        else:
            print("Congratulations! You've completed all levels.")
            pygame.quit()
            sys.exit()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # Check for key press events for grid-based movement
        if event.type == KEYDOWN and not key_press_handled:
            new_x, new_y = player_x, player_y
            if event.key == K_LEFT:
                new_x -= 1
            elif event.key == K_RIGHT:
                new_x += 1
            elif event.key == K_UP:
                new_y -= 1
            elif event.key == K_DOWN:
                new_y += 1

            # Move player if the new position is valid
            if can_move(new_x, new_y):
                player_x, player_y = new_x, new_y
                check_for_level_completion()  # Check if the exit is reached
            
            key_press_handled = True  # Prevent continuous movement

        elif event.type == KEYUP:
            key_press_handled = False

    # Draw the background, maze, and player
    screen.blit(background_img, (0, 0))
    draw_maze()
    screen.blit(player_img, (player_x * tile_size, player_y * tile_size))

    pygame.display.flip()  # Update the display

pygame.quit()
