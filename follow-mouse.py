import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import time

# Define circle parameters
circle_radius = 0.05  # Radius of the circle in OpenGL coordinates
circle_segments = 30  # Number of segments to draw the circle

def draw_circle(x, y):
    """Draw a circle at the specified (x, y) position."""
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)  # Center of the circle
    for i in range(circle_segments + 1):
        angle = 2 * math.pi * i / circle_segments  # Angle for each segment
        dx = circle_radius * math.cos(angle)
        dy = circle_radius * math.sin(angle)
        glVertex2f(x + dx, y + dy)  # Calculate vertex position
    glEnd()

def main():
    # Initialize Pygame
    pygame.init()
    # Set up the display
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Set up the perspective projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 1, 0, 1)  # Set orthographic projection to match mouse coordinates
    glMatrixMode(GL_MODELVIEW)

    last_time = time.time()  # Track the last time a circle was drawn
    circle_position = (0.5, 0.5)  # Initial position of the circle

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Get the mouse position and normalize it to OpenGL coordinates
        mouse_x, mouse_y = pygame.mouse.get_pos()
        normalized_x = mouse_x / display[0]
        normalized_y = 1 - (mouse_y / display[1])  # Invert y-axis

        # Check if 10 seconds have passed
        if time.time() - last_time >= 1:
            circle_position = (normalized_x, normalized_y)  # Update the circle position
            last_time = time.time()  # Reset the timer

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw the circle at the current position
        draw_circle(circle_position[0], circle_position[1])

        # Swap the buffer to display
        pygame.display.flip()
        pygame.time.wait(10)  # Wait for a short duration

if __name__ == "__main__":
    main()