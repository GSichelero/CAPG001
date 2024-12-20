#!/usr/bin/env python3

## @file phong.py
#  Applies the Phong method.
# 
# @author Ricardo Dutra da Silva


import sys
import ctypes
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
from PIL import Image
sys.path.append('../lib/')
import utils as ut
from ctypes import c_void_p


## Window width.
win_width  = 600
## Window height.
win_height = 600

## Program variable.
program = None
## Vertex array object.
VAO = None
## Vertex buffer object.
VBO = None

## Vertex shader.
vertex_code = """
#version 330 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 vNormal;
out vec3 fragPosition;
out vec2 vTexCoords;

void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0);
    vNormal = mat3(transpose(inverse(model))) * normal;
    fragPosition = vec3(model * vec4(position, 1.0));
    vTexCoords = texCoords;
}
"""

## Fragment shader.
fragment_code = """
#version 330 core
in vec3 vNormal;
in vec3 fragPosition;
in vec2 vTexCoords;

out vec4 fragColor;

uniform vec3 lightColor;
uniform vec3 lightPosition;
uniform vec3 cameraPosition;
uniform sampler2D texture1;

void main()
{
    float ka = 0.5;
    vec3 ambient = ka * lightColor;

    float kd = 0.8;
    vec3 n = normalize(vNormal);
    vec3 l = normalize(lightPosition - fragPosition);
    float diff = max(dot(n, l), 0.0);
    vec3 diffuse = kd * diff * lightColor;

    float ks = 1.0;
    vec3 v = normalize(cameraPosition - fragPosition);
    vec3 r = reflect(-l, n);
    float spec = pow(max(dot(v, r), 0.0), 3.0);
    vec3 specular = ks * spec * lightColor;

    vec3 color = texture(texture1, vTexCoords).rgb;
    vec3 light = (ambient + diffuse + specular) * color;
    fragColor = vec4(light, 1.0);
}
"""

def loadTexture():
    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)

    # Load image and convert to RGBA format
    image = Image.open("wall.jpg")
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(image, dtype=np.uint8)

    # Specify texture settings
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, image.width, image.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img_data)
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    return texture

## Drawing function.
#
# Draws primitive.
def display():

    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glUseProgram(program)
    gl.glBindVertexArray(VAO)

    gl.glActiveTexture(gl.GL_TEXTURE0)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    loc = gl.glGetUniformLocation(program, "texture1")
    gl.glUniform1i(loc, 0)

    Rx = ut.matRotateX(np.radians(10.0))
    Ry = ut.matRotateY(np.radians(-30.0))
    model=np.matmul(Rx,Ry)
    loc = gl.glGetUniformLocation(program, "model");
    gl.glUniformMatrix4fv(loc, 1, gl.GL_FALSE, model.transpose())

    view = ut.matTranslate(0.0, 0.0, -5.0)
    loc = gl.glGetUniformLocation(program, "view");
    gl.glUniformMatrix4fv(loc, 1, gl.GL_FALSE, view.transpose())
    
    projection = ut.matPerspective(np.radians(45.0), win_width/win_height, 0.1, 100.0)
    loc = gl.glGetUniformLocation(program, "projection");
    gl.glUniformMatrix4fv(loc, 1, gl.GL_FALSE, projection.transpose())

    # Object color.
    loc = gl.glGetUniformLocation(program, "objectColor")
    gl.glUniform3f(loc, 0.5, 0.1, 0.1)
    # Light color.
    loc = gl.glGetUniformLocation(program, "lightColor")
    gl.glUniform3f(loc, 1.0, 1.0, 1.0)
    # Light position.
    loc = gl.glGetUniformLocation(program, "lightPosition")
    gl.glUniform3f(loc, 1.0, 0.0, 2.0)
    # Camera position.
    loc = gl.glGetUniformLocation(program, "cameraPosition")
    gl.glUniform3f(loc, 0.0, 0.0, 0.0)

    gl.glDrawArrays(gl.GL_TRIANGLES, 0, 12*3)

    glut.glutSwapBuffers()


## Reshape function.
# 
# Called when window is resized.
#
# @param width New window width.
# @param height New window height.
def reshape(width,height):

    win_width = width
    win_height = height
    gl.glViewport(0, 0, width, height)
    glut.glutPostRedisplay()


## Keyboard function.
#
# Called to treat pressed keys.
#
# @param key Pressed key.
# @param x Mouse x coordinate when key pressed.
# @param y Mouse y coordinate when key pressed.
def keyboard(key, x, y):

    global type_primitive
    global mode

    if key == b'\x1b'or key == b'q':
        glut.glutLeaveMainLoop()

    glut.glutPostRedisplay()


## Init vertex data.
#
# Defines the coordinates for vertices, creates the arrays for OpenGL.
def initData():

    # Uses vertex arrays.
    global VAO
    global VBO

    vertices = np.array([
    # Position        Normal           Texture Coords
    -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  0.0,
     0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  0.0,
     0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  1.0,
    -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  0.0,
     0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  1.0,
    -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  1.0,
    
    0.5, -0.5,  0.5,  1.0,  0.0,  0.0,  0.0,  0.0,
    0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  1.0,  0.0,
    0.5,  0.5, -0.5,  1.0,  0.0,  0.0,  1.0,  1.0,
    0.5, -0.5,  0.5,  1.0,  0.0,  0.0,  0.0,  0.0,
    0.5,  0.5, -0.5,  1.0,  0.0,  0.0,  1.0,  1.0,
    0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  0.0,  1.0,
    
    0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  0.0,
   -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  0.0,
   -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  1.0,
    0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  0.0,
   -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  1.0,
    0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  1.0,
    
   -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0,  0.0,
   -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,  1.0,  0.0,
   -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0,  1.0,
   -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0,  0.0,
   -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0,  1.0,
   -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,  0.0,  1.0,
    
   -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  0.0,  0.0,
    0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0,  0.0,
    0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  1.0,  1.0,
   -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  0.0,  0.0,
    0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  1.0,  1.0,
   -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0,  1.0,
    
   -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  0.0,  0.0,
   -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  1.0,  0.0,
    0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0,  1.0,
   -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0,  0.0,
    0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  1.0,  1.0,
    0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  0.0,  1.0
    ], dtype='float32')

    # Vertex array.
    VAO = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(VAO)

    # Vertex buffer
    VBO = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)
    
    # Set attributes.
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * vertices.itemsize, None)
    gl.glEnableVertexAttribArray(0)
    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * vertices.itemsize, c_void_p(3 * vertices.itemsize))
    gl.glEnableVertexAttribArray(1)
    gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, 8 * vertices.itemsize, c_void_p(6 * vertices.itemsize))
    gl.glEnableVertexAttribArray(2)
    
    # Unbind Vertex Array Object.
    gl.glBindVertexArray(0)

    gl.glEnable(gl.GL_DEPTH_TEST);

## Create program (shaders).
#
# Compile shaders and create programs.
def initShaders():

    global program

    program = ut.createShaderProgram(vertex_code, fragment_code)


## Main function.
#
# Init GLUT and the window settings. Also, defines the callback functions used in the program.
def main():

    global texture

    glut.glutInit()
    glut.glutInitContextVersion(3, 3)
    glut.glutInitContextProfile(glut.GLUT_CORE_PROFILE)
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH)
    glut.glutInitWindowSize(win_width, win_height)
    glut.glutCreateWindow('Phong with Texture')

    initData()
    initShaders()

    texture = loadTexture()

    glut.glutReshapeFunc(reshape)
    glut.glutDisplayFunc(display)
    glut.glutKeyboardFunc(keyboard)
    glut.glutMainLoop()

if __name__ == '__main__':
    main()
