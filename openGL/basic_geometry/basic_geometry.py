#!/usr/bin/env python

"""PySide port of the opengl/hellogl example from Qt v4.x"""

import sys
import math
from PySide import QtCore, QtGui, QtOpenGL

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                            "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class GLWidget(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)

        self.lastPos = QtCore.QPoint()

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(50, 40, 150, 255))
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GL.glTranslated(0.0, 0.0, -10.0)

    def mousePressEvent(self, event):
    	self.lastPos = QtCore.QPoint(event.pos())
        print self.lastPos

    def mouseMoveEvent(self, event):

        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            #self.setXRotation(self.xRot + 8 * dy)
            #self.setYRotation(self.yRot + 8 * dx)
            print dy
        elif event.buttons() & QtCore.Qt.RightButton:
            #self.setXRotation(self.xRot + 8 * dy)
            #self.setZRotation(self.zRot + 8 * dx)
            print dy

        self.lastPos = QtCore.QPoint(event.pos())


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.glWidget = GLWidget()

        mainLayout = QtGui.QHBoxLayout(self)
        mainLayout.addWidget(self.glWidget)

        self.setWindowTitle(self.tr("Hello GL"))
        self.setGeometry(0,0,300,300)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())