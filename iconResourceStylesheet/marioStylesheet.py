#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import sys, os
import qdarkstyle

class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(50, 100, 300, 300)
        self.setWindowTitle('Test')

        # layout
        vbox = QtGui.QVBoxLayout(self)

        button_1 = QtGui.QPushButton('')
        vbox.addWidget(button_1)

        button_2 = QtGui.QPushButton('')
        vbox.addWidget(button_2)      

def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()