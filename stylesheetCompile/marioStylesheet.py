#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import sys, os
import petfactoryStyle
reload(petfactoryStyle)

class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(20, 60, 100, 100)
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
    app.setStyleSheet(petfactoryStyle.load_stylesheet())
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()