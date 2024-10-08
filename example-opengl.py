import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Define the vertices of the triangle
vertices = [
    (1, -1, 0),  # Bottom right
    (1, 1, 0),   # Top right
    (-1, 1, 0),  # Top left
]

def draw_triangle():
    glBegin(GL_TRIANGLES)
    for vertex in vertices:
        glVertex3fv(vertex)
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
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Move the camera back
    glTranslatef(0.0, 0.0, -5)

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Clear the screen and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Draw the triangle
        draw_triangle()
        
        # Swap the buffer to display
        pygame.display.flip()
        pygame.time.wait(10)  # Wait for a short duration

if __name__ == "__main__":
    main()