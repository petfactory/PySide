#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore

@QtCore.Slot(int)
def test(*args):
    print(args)

class Communicate(QtCore.QObject):
    speakNumber = QtCore.Signal(int)

class TestSignal(QtGui.QWidget):
    
    def __init__(self):
        super(TestSignal, self).__init__() 

        self.setGeometry(50, 100, 300, 300)
        self.setWindowTitle('Test')

        self.label = QtGui.QLabel(" ")
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.dot = QtCore.QPoint(130, 150)

        posList = [ QtCore.QPoint(100, 100),
                    QtCore.QPoint(100, 200),
                    QtCore.QPoint(200, 200),
                    QtCore.QPoint(200, 100),
                    QtCore.QPoint(100, 100)
                    ]

        self.polygon = QtGui.QPolygon(posList)


        someone = Communicate()
        someone.speakNumber.connect(test)
        someone.speakNumber.emit(10)

        self.connect(self, QtCore.SIGNAL("didSomething"), test)
        self.emit(QtCore.SIGNAL("didSomething"), "important", "information")

        print self.polygon
        #OddEvenFill
        #WindingFill
        print self.polygon.containsPoint(self.dot, QtCore.Qt.OddEvenFill)

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp):
      
        qp.setPen(QtCore.Qt.red)
        qp.drawPolyline(self.polygon)
        qp.drawPoint(self.dot)

def main():
    
    app = QtGui.QApplication(sys.argv)
    win = TestSignal()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()