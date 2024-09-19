import random
import pygame
import tkinter as tk
from tkinter import messagebox


# Cube class handles the position and movement of individual cubes (snake parts)
class cube(object):
    rows = 20  # Number of rows in the grid
    w = 500  # Width of the window

    # Initialize the cube with a position, direction, and color
    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start  # Position of the cube
        self.dirnx = 1  # Movement in x-direction (horizontal)
        self.dirny = 0  # Movement in y-direction (vertical)
        self.color = color  # Color of the cube

    # Move the cube based on its current direction
    def move(self, dirnx, dirny):
        self.dirnx = dirnx  # Update direction x
        self.dirny = dirny  # Update direction y
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)  # Update position

    # Draw the cube on the surface, with optional eyes for the snake's head
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows  # Size of each grid square
        i = self.pos[0]  # Cube's x position
        j = self.pos[1]  # Cube's y position

        # Draw the cube as a rectangle
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:  # Draw eyes for the head of the snake
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)  # Left eye
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)  # Right eye


# Snake class handles the snake's movement and behavior
class snake(object):
    body = []  # List of cubes representing the snake's body
    turns = {}  # Dictionary to store the positions and direction of turns

    # Initialize the snake with a color and starting position
    def __init__(self, color, pos):
        self.color = color  # Snake color
        self.head = cube(pos)  # Head of the snake is a cube
        self.body.append(self.head)  # Add the head to the body
        self.dirnx = 0  # Initial direction x
        self.dirny = 1  # Initial direction y (moving down)

    # Move the snake based on key inputs
    def move(self):
        for event in pygame.event.get():  # Check for quit event
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()  # Get all pressed keys

        # Update the direction based on key presses
        if keys[pygame.K_LEFT]:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys[pygame.K_RIGHT]:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys[pygame.K_UP]:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys[pygame.K_DOWN]:
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # Move each cube in the body based on its direction or turns
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])  # Move the cube in the turn's direction
                if i == len(self.body) - 1:  # Remove the turn after the last body part moves
                    self.turns.pop(p)
            else:
                # Handle edge of the screen wrapping for each direction
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)  # Keep moving in the current direction

    # Reset the snake to the initial position
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []  # Clear the body
        self.body.append(self.head)  # Add the head back to the body
        self.turns = {}  # Clear turns
        self.dirnx = 0
        self.dirny = 1

    # Add a cube to the snake when it eats a snack
    def addCube(self):
        tail = self.body[-1]  # Get the last cube (tail)
        dx, dy = tail.dirnx, tail.dirny  # Get its current direction

        # Add a new cube in the correct position based on the tail's direction
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        # Set the new cube's direction to match the tail
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    # Draw the entire snake body on the surface
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)  # Draw the head with eyes
            else:
                c.draw(surface)  # Draw the rest of the body


# Draw the grid on the surface
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows  # Distance between grid lines

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn  # Update x position for vertical lines
        y = y + sizeBtwn  # Update y position for horizontal lines

        # Draw vertical and horizontal grid lines
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


# Redraw the game window with snake, snack, and grid
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))  # Fill the background with black
    s.draw(surface)  # Draw the snake
    snack.draw(surface)  # Draw the snack
    drawGrid(width, rows, surface)  # Draw the grid
    pygame.display.update()  # Update the display


# Randomly place a snack on the grid, avoiding the snake's body
def randomSnack(rows, item):
    positions = item.body  # Get the current positions of the snake's body

    while True:
        x = random.randrange(rows)  # Random x position
        y = random.randrange(rows)  # Random y position
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:  # Avoid placing on the snake
            continue
        else:
            break

    return (x, y)  # Return the position of the snack


# Display a message box when the game ends
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)  # Make the window stay on top
    root.withdraw()  # Hide the window
    messagebox.showinfo(subject, content)  # Show the message box
    try:
        root.destroy()  # Destroy the window
    except:
        pass


# Main game loop
def main():
    global width, rows, s, snack
    width = 500  # Window width
    rows = 20  # Number of rows
    win = pygame


def main():
    global width, rows, s, snack
    width = 500  # Set the width of the game window
    rows = 20  # Set the number of rows in the grid
    win = pygame.display.set_mode((width, width))  # Create the game window
    s = snake((255, 0, 0), (10, 10))  # Initialize the snake object with red color and starting position
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))  # Create the first snack object with green color
    flag = True  # Game loop flag

    clock = pygame.time.Clock()  # Create a clock object to control the frame rate

    while flag:
        pygame.time.delay(50)  # Introduce a delay to control the game speed
        clock.tick(10)  # Set the frame rate to 10 frames per second

        s.move()  # Move the snake based on user input

        # Check for collision between the snake and the snack
        if s.body[0].pos == snack.pos:
            s.addCube()  # Add a new cube to the snake's body
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))  # Place a new snack at a random position

        # Check for collision with itself
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))  # Print the score (length of the snake)
                message_box('You Lost!', f'Your score was {len(s.body)}')  # Show a message box with the score
                s.reset((10, 10))  # Reset the snake to the starting position
                break

        redrawWindow(win)  # Redraw the game window with updated positions


# Ensure the script runs the main function if executed directly
if __name__ == "__main__":
    main()
