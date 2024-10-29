from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

scale_factor = 1.0
scale_step = 0.1

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)

def draw_rectangle():
    vertices = [
        [-1, -0.5], [1, -0.5], [1, 0.5], [-1, 0.5]
    ]

    glBegin(GL_QUADS)
    glColor3f(0.0, 0.8, 0.2)
    for vertex in vertices:
        glVertex2f(vertex[0], vertex[1])
    glEnd()

def display():
    global scale_factor

    glClear(GL_COLOR_BUFFER_BIT)
    
    glLoadIdentity()
    
    glScalef(scale_factor, scale_factor, 1.0)

    draw_rectangle()

    glutSwapBuffers()

def keyboard(key, x, y):
    global scale_factor

    if key == b'w':
        scale_factor += scale_step
    elif key == b's':
        scale_factor -= scale_step
        if scale_factor < 0.1:
            scale_factor = 0.1
    glutPostRedisplay()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-3.0, 3.0, -3.0, 3.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(600, 600)
    glutCreateWindow('Retangulo com Escala')

    init()
    
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    glutMainLoop()

if __name__ == "__main__":
    main()