from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


P, O, Q = Point(), Point(), Point()
point_selected = [False, False, False]


def magnitude(v):
    return math.sqrt(v.x**2 + v.y**2)

def angle_between(u, v):
    dot = np.dot(u, v)
    mag_u = magnitude(u)
    mag_v = magnitude(v)
    cos_theta = dot / (mag_u * mag_v)
    angle = math.acos(cos_theta) * 180.0 / math.pi
    return angle

def distance_from_point_to_line(P, O, Q):
    v = Point(Q.x - O.x, Q.y - O.y)
    w = Point(P.x - O.x, P.y - O.y)
    area = abs(v.x * w.y - v.y * w.x)
    base = magnitude(v)
    return area / base

def draw_vector(origin, vector):
    glBegin(GL_LINES)
    glVertex2f(origin.x, origin.y)
    glVertex2f(origin.x + vector.x, origin.y + vector.y)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    if point_selected[0]:
        glPointSize(10)
        glBegin(GL_POINTS)
        glVertex2f(P.x, P.y)
        glEnd()
    if point_selected[1]:
        glPointSize(10)
        glBegin(GL_POINTS)
        glVertex2f(O.x, O.y)
        glEnd()
    if point_selected[2]:
        glPointSize(10)
        glBegin(GL_POINTS)
        glVertex2f(Q.x, Q.y)
        glEnd()

    if point_selected[0] and point_selected[1] and point_selected[2]:
        u = Point(P.x - O.x, P.y - O.y)
        v = Point(Q.x - O.x, Q.y - O.y)

        glColor3f(1.0, 0.0, 0.0)
        draw_vector(O, u)

        glColor3f(0.0, 0.0, 1.0)
        draw_vector(O, v)

        print(f"Ângulo entre u e v: {angle_between(u, v):.2f} graus")
        print(f"Produto interno: {np.dot(u, v):.2f}")
        # print("Produto vetorial: ", np.cross(u, v))
        print(f"Distância entre P a linha definida por v: {distance_from_point_to_line(P, O, Q):.2f}")

    glFlush()


def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        fx = (x / 250) - 1
        fy = 1 - (y / 250)

        if not point_selected[0]:
            P.x, P.y = fx, fy
            point_selected[0] = True
        elif not point_selected[1]:
            O.x, O.y = fx, fy
            point_selected[1] = True
        elif not point_selected[2]:
            Q.x, Q.y = fx, fy
            point_selected[2] = True
        else:
            point_selected[0] = point_selected[1] = point_selected[2] = False

        glutPostRedisplay()


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glColor3f(0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow("Vetores")
    init()
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutMainLoop()

if __name__ == "__main__":
    main()