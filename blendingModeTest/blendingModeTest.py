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

        self.pixmap_circle_mask = QtGui.QPixmap('circle_mask.png')   
        self.pixmap_birds = QtGui.QPixmap('blue_birds')
        self.pixmap_black_square = QtGui.QPixmap('shadow.png')
        self.pixmap_white_square = QtGui.QPixmap('highlight.png')

        self.out_width, self.our_height = self.pixmap_circle_mask.size().toTuple()
        self.crop_rect = QtCore.QRect(0, 0, self.out_width, self.our_height)

        self.label = QtGui.QLabel()
        vbox.addWidget(self.label)

        self.color_button = QtGui.QPushButton('Select Color')
        vbox.addWidget(self.color_button)
        self.color_button.clicked.connect(self.select_color)

        self.color_dialog = QtGui.QColorDialog(self)
        self.color_dialog.currentColorChanged.connect(self.draw_pixmap)
        
        self.draw_pixmap(QtGui.QColor(0,127,56,255))
        
    def select_color(self):
        self.color_dialog.show()

    def draw_pixmap(self, color):

        base_pixmap = QtGui.QPixmap(self.out_width, self.our_height) 

        painter = QtGui.QPainter(base_pixmap)
        
        # draw base
        painter.fillRect(self.crop_rect, color)
        #painter.drawPixmap(crop_rect, pixmap_birds)

        # multiply
        painter.setCompositionMode(painter.CompositionMode_Multiply)
        painter.drawPixmap(self.crop_rect, self.pixmap_black_square)

        # plus / screen
        #painter.setCompositionMode(painter.CompositionMode_Plus)
        painter.setCompositionMode(painter.CompositionMode_Screen)
        painter.drawPixmap(self.crop_rect, self.pixmap_white_square)

        # stencil
        painter.setCompositionMode(painter.CompositionMode_DestinationAtop)
        painter.drawPixmap(self.crop_rect, self.pixmap_circle_mask)
        
        painter.end()

        self.label.setPixmap(base_pixmap)



def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()