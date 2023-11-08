import sys
import ctypes

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


from OpenGL.GL.shaders import compileProgram, compileShader

from PyQt6.QtGui import QSurfaceFormat
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication
#from PyQt6.QtOpenGL import QOpenGLWindow, QOpenGLVersionProfile
#from PySide6.QtOpenGLWidgets import QOpenGLWidget

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtOpenGL import *
from PyQt6.QtOpenGLWidgets import *


from functools import partial

import pandas as pd

## Initial pyOpengl set up from this tutorial: https://www.youtube.com/watch?v=lFFYmP528Mw

vertex_src = '''
#version 330 core

layout (location=0) in vec3 vertexPos;
layout (location=1) in vec3 vertexColor;

out vec3 fragmentColor;

void main()
{
  gl_Position = vec4(vertexPos, 1.0);
  fragmentColor = vertexColor;
}
'''

fragment_src = '''
#version 330 core

in vec3 fragmentColor;

out vec4 color;

void main()
{
   color = vec4(fragmentColor, 1.0);
}
'''



added_vertices = pd.read_csv("data.csv", header = None)

added_vertices = np.array(added_vertices)

rot_angle = 0

def Path():
    glBegin(GL_LINE_STRIP)
    for i in added_vertices:
        glVertex3fv(i[:3])
    glEnd()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Trajectory Visualizer Demo")

        point_selectors_layout = QVBoxLayout()
        self.widget_list = []
        for i in range(6):
            point_select_layout = QHBoxLayout()

            name_widget = QLabel(f"Point {i}")
            point_select_layout.addWidget(name_widget)

            for n in range(3):
                widget = QSpinBox()
                widget.setMinimum(-10)
                widget.setMaximum(10)
                widget.setSingleStep(1)
                widget.setValue(added_vertices[i][n])
                widget.valueChanged.connect(partial(self.change_vector_array, len(self.widget_list), i, n))
                self.widget_list.append(widget)

                point_select_layout.addWidget(widget)
            point_selectors_layout.addLayout(point_select_layout)



        save_button = QPushButton()
        save_button.pressed.connect(self.save_points)
        point_selectors_layout.addWidget(save_button)

        full_layout = QHBoxLayout()
        #self.opengl_widget = QOpenGLWindow
        full_layout.addWidget(GLWidget())

        full_layout.addLayout(point_selectors_layout)


        widget = QWidget()
        widget.setLayout(full_layout)
        self.setCentralWidget(widget)

    def change_vector_array(self, val, x, y):
        added_vertices[x][y] = self.widget_list[val].value()
        print(val,x, y, self.widget_list[val].value())

    def save_points(self):
        df = pd.DataFrame(added_vertices)
        df.to_csv('data.csv', index=False, header=False)

    def angle_changed(self, angle):
        rot_angle = angle




class GLWidget(QOpenGLWidget):

    def __init__(self):
        super().__init__()

    def initializeGL(self):
        self.fmt = QOpenGLVersionProfile()
        self.fmt.setVersion(3, 3)
        self.fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)

        print(f"Running {glGetString(GL_VERSION)}")

        gluPerspective(45, (1), 0.1, 50.0)

        glTranslatef(0.0, 0.0, -15)

        self.count = 0

        self.timer = QTimer(self)
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Cube()
        Path()

app = QApplication(sys.argv)
window = MainWindow()
#window2 = GLWindow()
window.resize(QSize(1200, 600))
#window2.resize(QSize(800, 600))
window.show()
#window2.show()
app.exec()





