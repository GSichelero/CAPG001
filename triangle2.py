import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

points = []
window_width = 500
window_height = 500


def draw_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_line(p1, p2):
    glBegin(GL_LINES)
    glVertex2f(p1[0], p1[1])
    glVertex2f(p2[0], p2[1])
    glEnd()


def dot_product(u, v):
    return np.dot(u, v)

def cross_product(u, v):
    return u[0] * v[1] - u[1] * v[0]

def angle_between(u, v):
    dot = dot_product(u, v)
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    cos_theta = dot / (norm_u * norm_v)
    angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    return np.degrees(angle)

def distance_point_to_line(P, O, Q):
    v = np.array(Q) - np.array(O)
    p_to_o = np.array(P) - np.array(O)
    cross = cross_product(p_to_o, v)
    norm_v = np.linalg.norm(v)
    distance = np.abs(cross) / norm_v
    return distance


def mouse_click(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x_opengl = x / window_width * 2 - 1
        y_opengl = -(y / window_height * 2 - 1)
        
        points.append([x_opengl, y_opengl])
        
        if len(points) == 3:
            O, P, Q = points
            
            u = np.array(P) - np.array(O)
            v = np.array(Q) - np.array(O)
            
            angle = angle_between(u, v)
            dot = dot_product(u, v)
            cross = cross_product(u, v)
            distance = distance_point_to_line(P, O, Q)
            
            print(f"Ângulo entre u e v: {angle:.2f} graus")
            print(angle)
            print(f"Produto interno (u • v): {dot:.2f}")
            print(dot)
            print(f"Produto vetorial (u x v): {cross:.2f}")
            print(cross)
            print(f"Distância de P à linha OQ: {distance:.2f}")
            print(distance)
        
        glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    for point in points:
        draw_point(point[0], point[1])
    
    if len(points) == 3:
        O, P, Q = points
        draw_line(O, P)
        draw_line(O, Q)
    if len(points) > 3:
        points.clear()
    
    glFlush()


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(5.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow("")
    init()
    glutDisplayFunc(display)
    glutMouseFunc(mouse_click)
    glutMainLoop()

if __name__ == "__main__":
    main()