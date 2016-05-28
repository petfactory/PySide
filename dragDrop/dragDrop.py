#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore


class Button(QtGui.QPushButton):
    
    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        #self.setDragEnabled(True)

    #def mouseMoveEvent(self, event):
    def mousePressEvent(self, event):

        mimeData = QtCore.QMimeData()

        drag = QtGui.QDrag(self)

        qColor = QtGui.QColor()
        qColor.setRgbF(1,0,0,1)            
        pixmap = QtGui.QPixmap(24, 12)
        pixmap.fill(QtGui.QColor(qColor))
        drag.setPixmap(pixmap)
        drag.setHotSpot(QtCore.QPoint(12, 6))


        drag.setMimeData(mimeData)

        dropAction = drag.start(QtCore.Qt.MoveAction)

        QtGui.QPushButton.mousePressEvent(self, event)

    '''
    def mouseReleaseEvent(self, e):
      
        QtGui.QPushButton.mouseReleaseEvent(self, e)
        if e.button() == QtCore.Qt.LeftButton:
            print 'Release'

    def mousePressEvent(self, e):
      
        QtGui.QPushButton.mousePressEvent(self, e)
        if e.button() == QtCore.Qt.LeftButton:
            print 'press'
    '''

    def dragEnterEvent(self, event):
        print 'dragEnterEvent {} -> {}'.format(event.source().text(), self.text())
        event.accept()

    def dropEvent(self, event):
        print 'dropEvent {} -> {}'.format(event.source().text(), self.text())
        event.accept()
        
class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(50, 100, 100, 50)
        self.setWindowTitle('Test')


        # layout
        vbox = QtGui.QVBoxLayout(self)

        button1 = Button('Button 1')
        vbox.addWidget(button1)

        button2 = Button('Button 2')
        vbox.addWidget(button2)

def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()