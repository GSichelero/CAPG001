from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *  # Import GLUT functions
import math
import time
import sys

# Define circle parameters
circle_radius = 0.05  # Radius of the circle in OpenGL coordinates
circle_segments = 30  # Number of segments to draw the circle

# Initialize variables
last_time = time.time()  # Track the last time a circle was drawn
circle_position = (0.5, 0.5)  # Initial position of the circle

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

def draw_square(x, y):
    """Draw a square at the specified (x, y) position."""
    glBegin(GL_QUADS)
    glVertex2f(x - circle_radius, y - circle_radius)  # Bottom left
    glVertex2f(x + circle_radius, y - circle_radius)  # Bottom right
    glVertex2f(x + circle_radius, y + circle_radius)  # Top right
    glVertex2f(x - circle_radius, y + circle_radius)  # Top left
    glEnd()

def display():
    """Render the scene."""
    global circle_position

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the square at the current position
    draw_square(circle_position[0], circle_position[1])

    # Swap the buffer to display
    glutSwapBuffers()

def timer(value):
    """Timer function to update the circle position."""
    global last_time, circle_position

    # Get mouse position
    mouse_x, mouse_y = glutGet(GLUT_WINDOW_X), glutGet(GLUT_WINDOW_Y)
    normalized_x = mouse_x / 800.0  # Assuming window width is 800
    normalized_y = 1 - (mouse_y / 600.0)  # Invert y-axis

    # Check if 1 second has passed
    if time.time() - last_time >= 1:
        circle_position = (normalized_x, normalized_y)  # Update the circle position
        last_time = time.time()  # Reset the timer

    glutPostRedisplay()  # Request a redraw
    glutTimerFunc(10, timer, 0)  # Call this function again after 10ms

def mouse_motion(x, y):
    """Update circle position based on mouse movement."""
    global circle_position
    normalized_x = x / 800.0  # Assuming window width is 800
    normalized_y = 1 - (y / 600.0)  # Invert y-axis
    circle_position = (normalized_x, normalized_y)

def main():
    # Initialize GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutCreateWindow("OpenGL with GLUT")

    # Set up the orthographic projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 1, 0, 1)  # Set orthographic projection to match mouse coordinates
    glMatrixMode(GL_MODELVIEW)

    glutDisplayFunc(display)  # Register the display function
    glutPassiveMotionFunc(mouse_motion)  # Register mouse motion function
    glutTimerFunc(10, timer, 0)  # Register timer function

    # Start the GLUT main loop
    glutMainLoop()

if __name__ == "__main__":
    main()