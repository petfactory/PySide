#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys, os
from PySide import QtGui, QtCore

class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(50, 100, 300, 300)
        self.setWindowTitle('Test')

        # layout
        vbox = QtGui.QVBoxLayout(self)
        button = QtGui.QPushButton()
        image_path = self.resource_path('logo.jpg')
        button.setIcon(QtGui.QIcon(image_path))
        button.setIconSize(QtCore.QSize(300,300))
        button.setFixedSize(320,320)
        button.clicked.connect(self.speak)
        vbox.addWidget(button)

    def speak(self):
      path = self.resource_path('logo.jpg')
      print('{} exists -> {}'.format(path, os.path.isfile(path)))

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()