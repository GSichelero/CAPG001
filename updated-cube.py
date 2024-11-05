from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

# Shader sources
vertex_shader_source = """
#version 330 core
layout(location = 0) in vec3 aPos;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}
"""

fragment_shader_source = """
#version 330 core
out vec4 FragColor;

void main() {
    FragColor = vec4(0.0, 0.5, 0.8, 1.0);
}
"""

vertices = np.array([
    -1, -1, -1,  1, -1, -1,  1,  1, -1,  -1,  1, -1,  # Front face
    -1, -1,  1,  1, -1,  1,  1,  1,  1,  -1,  1,  1,  # Back face
    -1, -1, -1, -1,  1, -1, -1,  1,  1,  -1, -1,  1,  # Left face
     1, -1, -1,  1,  1, -1,  1,  1,  1,   1, -1,  1,  # Right face
    -1, -1, -1,  1, -1, -1,  1, -1,  1,  -1, -1,  1,  # Bottom face
    -1,  1, -1,  1,  1, -1,  1,  1,  1,  -1,  1,  1   # Top face
], dtype=np.float32)

VAO = None
VBO = None
shader = None
rotation_x, rotation_y, rotation_z = 0, 0, 0

def init():
    global VAO, VBO, shader
    
    shader = compileProgram(
        compileShader(vertex_shader_source, GL_VERTEX_SHADER),
        compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
    )
    
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    glEnable(GL_DEPTH_TEST)
    

def create_rotation_matrix(angle, axis):
    """Creates a rotation matrix for a given angle (in degrees) and axis."""
    angle = np.radians(angle)
    c, s = np.cos(angle), np.sin(angle)
    if axis == 'x':
        return np.array([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
    elif axis == 'y':
        return np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
    elif axis == 'z':
        return np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

def display():
    global rotation_x, rotation_y, rotation_z

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(shader)

    # Create model matrix with rotation
    model = np.eye(4, dtype=np.float32)
    model = np.dot(model, create_rotation_matrix(rotation_x, 'x'))
    model = np.dot(model, create_rotation_matrix(rotation_y, 'y'))
    model = np.dot(model, create_rotation_matrix(rotation_z, 'z'))

    # View matrix: simple translation along Z-axis
    view = np.eye(4, dtype=np.float32)
    view[3, 2] = -7.0

    # Projection matrix (perspective)
    projection = np.eye(4, dtype=np.float32)
    aspect_ratio = 1.0  # Assuming square viewport
    fov = np.radians(45)
    near, far = 1.0, 50.0
    f = 1.0 / np.tan(fov / 2)
    projection[0, 0] = f / aspect_ratio
    projection[1, 1] = f
    projection[2, 2] = (far + near) / (near - far)
    projection[2, 3] = (2 * far * near) / (near - far)
    projection[3, 2] = -1
    projection[3, 3] = 0

    # Pass matrices to shader
    glUniformMatrix4fv(glGetUniformLocation(shader, "model"), 1, GL_FALSE, model)
    glUniformMatrix4fv(glGetUniformLocation(shader, "view"), 1, GL_FALSE, view)
    glUniformMatrix4fv(glGetUniformLocation(shader, "projection"), 1, GL_FALSE, projection)

    glBindVertexArray(VAO)
    glDrawArrays(GL_QUADS, 0, 24)
    glBindVertexArray(0)

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
        rotation_x = rotation_y = rotation_z = 0
    glutPostRedisplay()

def reshape(width, height):
    glViewport(0, 0, width, height)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b'3D Cube with Modern OpenGL using GLUT')

    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    glutMainLoop()

if __name__ == "__main__":
    main()