import sys
import ctypes

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


from OpenGL.GL.shaders import compileProgram, compileShader





def path(points):
    glBegin(GL_LINE_STRIP)
    for i in points:
        glVertex3fv(i[:3])
    glEnd()