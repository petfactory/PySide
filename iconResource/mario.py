#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import sys, os
import icons

class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(50, 100, 300, 300)
        self.setWindowTitle('Test')

        # layout
        vbox = QtGui.QVBoxLayout(self)
        '''
        pixmap = QtGui.QPixmap(':/qss_icons/media/mario.png')
        icon = QtGui.QIcon(pixmap)
        size = pixmap.size()
        button = QtGui.QPushButton(icon, '')
        button.setFixedSize(size + QtCore.QSize(16, 16))
        button.setIconSize(size)
        vbox.addWidget(button)
        '''
        button_stylesheet = QtGui.QPushButton('asd')
        vbox.addWidget(button_stylesheet)
        #button_stylesheet.setFixedSize(size + QtCore.QSize(16, 16))
        #button_stylesheet.setIconSize(size)
        

        button_stylesheet.setStyleSheet('''
                                        QPushButton {
                                            image: url(:/qss_icons/media/mario.png);
                                        }

                                        '''
                                        )

def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()