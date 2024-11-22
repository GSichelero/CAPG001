from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *  
import math
import time
import sys


circle_radius = 0.05  
circle_segments = 30  


last_time = time.time()  
circle_position = (0.5, 0.5)  

def draw_circle(x, y):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)  
    for i in range(circle_segments + 1):
        angle = 2 * math.pi * i / circle_segments  
        dx = circle_radius * math.cos(angle)
        dy = circle_radius * math.sin(angle)
        glVertex2f(x + dx, y + dy)  
    glEnd()

def draw_square(x, y):
    glBegin(GL_QUADS)
    glVertex2f(x - circle_radius, y - circle_radius)  
    glVertex2f(x + circle_radius, y - circle_radius)  
    glVertex2f(x + circle_radius, y + circle_radius)  
    glVertex2f(x - circle_radius, y + circle_radius)  
    glEnd()

def display():
    global circle_position

    
    glClear(GL_COLOR_BUFFER_BIT)

    
    draw_square(circle_position[0], circle_position[1])

    
    glutSwapBuffers()

def timer(value):
    global last_time, circle_position

    
    mouse_x, mouse_y = glutGet(GLUT_WINDOW_X), glutGet(GLUT_WINDOW_Y)
    normalized_x = mouse_x / 800.0  
    normalized_y = 1 - (mouse_y / 600.0)  

    
    if time.time() - last_time >= 1:
        circle_position = (normalized_x, normalized_y)  
        last_time = time.time()  

    glutPostRedisplay()  
    glutTimerFunc(10, timer, 0)  

def mouse_motion(x, y):
    global circle_position
    normalized_x = x / 800.0  
    normalized_y = 1 - (y / 600.0)  
    circle_position = (normalized_x, normalized_y)

def main():
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutCreateWindow("OpenGL with GLUT")

    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 1, 0, 1)  
    glMatrixMode(GL_MODELVIEW)

    glutDisplayFunc(display)  
    glutPassiveMotionFunc(mouse_motion)  
    glutTimerFunc(10, timer, 0)  

    
    glutMainLoop()

if __name__ == "__main__":
    main()