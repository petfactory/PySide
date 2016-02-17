#!/usr/bin/python
# -*- coding: utf-8 -*-



import sys
from PySide import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        
    def initUI(self):
        
        self.setGeometry(60, 100, 250, 150)
        self.setWindowTitle('Icon')
        
        vbox = QtGui.QVBoxLayout(self)

        button = QtGui.QPushButton('Button')
        button.clicked.connect(self.button_clicked)
        vbox.addWidget(button)    

        
        self.show()
        return self

    def button_clicked(self, *args):

        modifiers = QtGui.QApplication.keyboardModifiers()

        if modifiers == QtCore.Qt.ShiftModifier:
            print('Shift+Click')

        elif modifiers == QtCore.Qt.ControlModifier:
            print('Control+Click')

        elif modifiers == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier):
            print('Control+Shift+Click')

        else:
            print('Click')
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    