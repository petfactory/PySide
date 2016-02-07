#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore

class Signal:
    def __init__(self):
        self.__subscribers = []
      
    def emit(self, *args, **kwargs):
        for subs in self.__subscribers:
            subs(*args, **kwargs)

    def connect(self, func):
        self.__subscribers.append(func)  
      
    def disconnect(self, func):  
        try:  
            self.__subscribers.remove(func)  
        except ValueError:  
            print('Warning: function {} not removed '
                  'from signal {}'.format(func, self))


class MyScroll(QtGui.QScrollArea):
    def __init__(self, parent=None):
        super(MyScroll, self).__init__(parent)
        self.lastX = None
        self.lastY = None

        self.clicked = Signal()

    def mousePressEvent(self, event):
        
        xWin = event.x()
        yWin = event.y()

        xScroll = self.horizontalScrollBar().value()
        yScroll = self.verticalScrollBar().value()

        x = xWin + xScroll
        y = yWin + yScroll

        self.clicked.emit(QtCore.QPoint(x, y))

class CanvasWidget(QtGui.QWidget):
    
    def __init__(self):
        super(CanvasWidget, self).__init__()
        self._polygon = None
        self.setFixedSize(400,400)
        self.dot = QtCore.QPoint(140, 180)

    def setPolygon(self, polygon):
        self._polygon = polygon
        #print self.polygon.containsPoint(self.dot, QtCore.Qt.OddEvenFill)

    def paintEvent(self, e):

        if self._polygon is None:
            return

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp):
      
        qp.setPen(QtCore.Qt.red)
        qp.drawPolyline(self._polygon)
        #qp.drawPoint(self.dot)
        qp.drawEllipse(self.dot, 10, 10)
        qp.setFont(QtGui.QFont('Arial', 30))
        rectSize = QtCore.QSizeF(200,40)
        rect = QtCore.QRectF(self.dot, rectSize)
        
        #qp.drawText(self.dot, 'Hello World!')
        textPos = QtCore.QPoint(self.dot.x() - rect.width()*.5, self.dot.y() - rect.height()*.5)
        textRect = QtCore.QRectF(textPos, rectSize)
        qp.drawRect(textRect)

        qp.drawText(textRect, QtCore.Qt.AlignCenter, 'Hello World!')


class TestSignal(QtGui.QWidget):
    
    def __init__(self):
        super(TestSignal, self).__init__() 

        self.setGeometry(50, 100, 300, 300)
        #self.setWindowTitle('Test')

        vbox = QtGui.QVBoxLayout(self)

        scrollArea = MyScroll()
        vbox.addWidget(scrollArea)

        posList = [ QtCore.QPoint(100, 100),
                    QtCore.QPoint(250, 100),
                    QtCore.QPoint(250, 150),
                    QtCore.QPoint(200, 150),
                    QtCore.QPoint(200, 250),
                    QtCore.QPoint(100, 250),
                    QtCore.QPoint(100, 100),
                    ]

        self.polygon = QtGui.QPolygon(posList)

        canvasWidget = CanvasWidget()
        canvasWidget.setPolygon(self.polygon)
        scrollArea.setWidget(canvasWidget)
        scrollArea.clicked.connect(self.scrollClicked)

    def scrollClicked(self, point, *args):
        print point, args
        print self.polygon.containsPoint(point, QtCore.Qt.OddEvenFill)


def main():
    
    app = QtGui.QApplication(sys.argv)
    win = TestSignal()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()