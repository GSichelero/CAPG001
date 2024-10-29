from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

rotation_x, rotation_y, rotation_z = 0, 0, 0

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def draw_cube():
    vertices = [
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
    ]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]

    glBegin(GL_QUADS)
    for edge in edges:
        for vertex in edge:
            glColor3f(0.0, 0.5, 0.8)
            glVertex3fv(vertices[vertex])
    glEnd()

def display():
    global rotation_x, rotation_y, rotation_z
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -7.0)

    glRotatef(rotation_x, 1.0, 0.0, 0.0)
    glRotatef(rotation_y, 0.0, 1.0, 0.0)
    glRotatef(rotation_z, 0.0, 0.0, 1.0)

    draw_cube()

    glutSwapBuffers()

def keyboard(key, x, y):
    global rotation_x, rotation_y, rotation_z
    if key == b'x':
        rotation_x += 5
    elif key == b'y':
        rotation_y += 5
    elif key == b'z':
        rotation_z += 5
    elif key == b'r':
        rotation_x, rotation_y, rotation_z = 0, 0, 0
    glutPostRedisplay()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutCreateWindow('Cubo 3D com Transformações')

    init()
    
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    glutMainLoop()

if __name__ == "__main__":
    main()