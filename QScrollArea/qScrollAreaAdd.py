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


class ScrollArea(QtGui.QScrollArea):

    def __init__(self, parent=None):
        super(ScrollArea, self).__init__(parent)
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
    
    def __init__(self, parent=None):

        super(CanvasWidget, self).__init__(parent)
        self.setFixedSize(400,400)
        self._parent = parent
        self.fontSize = 12
        self.font = 'Arial'
        self.strokeColor = QtGui.QColor(242, 165, 12)

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp):
      
        qp.setPen(self.strokeColor)
        qp.setFont(QtGui.QFont(self.font, self.fontSize))

        for name, infoDict in self._parent.hitInfoDict.iteritems():

            polygon = infoDict.get('polygon')
            labelPos = infoDict.get('labelPos')

            qp.drawPolyline(polygon)
            qp.drawText(labelPos, name)


class TestSignal(QtGui.QWidget):
    
    def __init__(self):
        super(TestSignal, self).__init__() 

        self.setGeometry(980, 50, 380, 350)
        self.setWindowTitle('Add Polygons')

        vbox = QtGui.QVBoxLayout(self)

        scrollArea = ScrollArea()
        vbox.addWidget(scrollArea)

        hitAreaDict =   {   'G__FIRST':  {  'labelPos':(30,60),
                                            'hitAreaVerts':[(10, 40),
                                                            (110, 10),
                                                            (110, 110),
                                                            (60, 90)]
                                        },

                            'G__SECOND':  { 'labelPos':(110,140),
                                            'hitAreaVerts':[(100, 120),
                                                            (200, 120),
                                                            (200, 200),
                                                            (100, 170)]
                                        },

                            'X':  {         'labelPos':(255, 140),
                                            'hitAreaVerts':[(250, 120),
                                                            (300, 120),
                                                            (250, 160)]
                                        }
                        }

        self.hitInfoDict = self.parseInfo(hitAreaDict)

        canvasWidget = CanvasWidget(self)
        scrollArea.setWidget(canvasWidget)
        scrollArea.clicked.connect(self.scrollClicked)


    def scrollClicked(self, point, *args):

        #print point, args
        for name, infoDict in self.hitInfoDict.iteritems():

            polygon = infoDict.get('polygon')
            hit = polygon.containsPoint(point, QtCore.Qt.OddEvenFill)
            if hit:
                print '{} was clicked'.format(name)
                return

        print 'No hit'


    def parseInfo(self, hitAreaDict):

        retDict = {}

        for name, infoDict in hitAreaDict.iteritems():

            labelPosTuple = infoDict.get('labelPos')
            hitAreaVerts = infoDict.get('hitAreaVerts')

            posList = [QtCore.QPoint(p[0], p[1]) for p in hitAreaVerts]
            polygon = polygon = QtGui.QPolygon(posList)

            labelPos = QtCore.QPoint(labelPosTuple[0], labelPosTuple[1])
            retDict[name] = {"labelPos":labelPos, 'polygon':polygon}
        
        return retDict


def main():
    
    app = QtGui.QApplication(sys.argv)
    win = TestSignal()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()