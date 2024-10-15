from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.5, -0.5)
    glVertex2f(0.5, -0.5)
    glVertex2f(0.0, 0.5)
    glEnd()
    glFlush()

glutInit()
glutCreateWindow("OpenGL Example")
glutDisplayFunc(draw)
glutMainLoop()