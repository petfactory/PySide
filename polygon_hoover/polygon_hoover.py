#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore

class MyPathItem(QtGui.QGraphicsPathItem):

    def __init__(self):
        super(MyPathItem, self).__init__()
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        print('inside')

    def hoverLeaveEvent(self, event):
        print('outside')

    def shape(self):
        return self.path()


class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(50, 100, 300, 300)
        self.setWindowTitle('Test')

        # layout
        vbox = QtGui.QVBoxLayout(self)

        self.scene = QtGui.QGraphicsScene()
    
        path = QtGui.QPainterPath()
        path.addRect(0, 0, 100, 100)
        path.addRect(25, 25, 50, 50)

        item = MyPathItem()
        item.setPath(path)
        item.setBrush(QtGui.QBrush(QtCore.Qt.blue))

        self.scene.addItem(item)

        view = QtGui.QGraphicsView(self.scene)
        view.setSceneRect(0,0,300,300)
        
        vbox.addWidget(view)


def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()