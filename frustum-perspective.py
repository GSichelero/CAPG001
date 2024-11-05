import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
from OpenGL.GL import shaders
import numpy as np
import math

vertices = np.array([
    [0.0,  0.5, -3.0],
    [-0.5, -0.5, -3.0],
    [0.5, -0.5, -3.0]
], dtype=np.float32)

colors = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0]
], dtype=np.float32)

vertex_shader_source = """
#version 330 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 color;
out vec3 fragColor;

void main() {
    gl_Position = vec4(position, 1.0);
    fragColor = color;
}
"""

fragment_shader_source = """
#version 330 core
in vec3 fragColor;
out vec4 FragColor;

void main() {
    FragColor = vec4(fragColor, 1.0);
}
"""

def create_shader_program():
    vertex_shader = shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = shaders.compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
    shader_program = shaders.compileProgram(vertex_shader, fragment_shader)
    return shader_program

def setup_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    fovy = 30
    aspect = 1.5
    zNear = 2.0
    zFar = 100.0

    fovy_rad = math.radians(fovy)
    top = zNear * math.tan(fovy_rad / 2)
    bottom = -top
    right = top * aspect
    left = -right

    glFrustum(left, right, bottom, top, zNear, zFar)

def setup_viewport():
    glViewport(0, 0, 800, 600)
    glEnable(GL_DEPTH_TEST)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(shader_program)
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, vertices)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, colors)

    glDrawArrays(GL_TRIANGLES, 0, 3)

    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)

    glUseProgram(0)

    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Frustum Projection with OpenGL")

    global shader_program
    shader_program = create_shader_program()

    setup_projection()
    setup_viewport()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()