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

class TestSignal(QtGui.QWidget):
    
    def __init__(self):
        super(TestSignal, self).__init__() 

        self.setGeometry(50, 100, 300, 300)
        self.setWindowTitle('Test')

        layout = QtGui.QVBoxLayout(self)

        clicked = Signal()
        clicked.connect(self.test)
        #clicked.disconnect(self.test)
        #clicked.disconnect(self.test)
        clicked.emit('Hello!', 12)

    def test(self, *args):
    	print args

def main():
    
    app = QtGui.QApplication(sys.argv)
    win = TestSignal()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()