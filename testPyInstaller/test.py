#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore

class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(50, 100, 300, 300)
        self.setWindowTitle('Test')

        # layout
        vbox = QtGui.QVBoxLayout(self)
       	button = QtGui.QPushButton()
       	button.setIcon(QtGui.QIcon('logo.jpg'))
       	button.setIconSize(QtCore.QSize(300,300))
       	button.setFixedSize(320,320)
       	vbox.addWidget(button)

def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()