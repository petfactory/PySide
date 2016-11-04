#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from functools import partial

from PySide import QtGui, QtCore

# from . import uicomponents
import uicomponents


class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(50, 100, 300, 300)
        self.setWindowTitle('Test')

        # layout
        vbox = QtGui.QVBoxLayout(self)

        slider_range = (0, 100)

        spinbox_slider_1 = uicomponents.SpinboxSlider()
        vbox.addWidget(spinbox_slider_1)
        spinbox_slider_1.valueChanged.connect(self.widget_changed)
        spinbox_slider_1.setRange(40, 600)

        spinbox_slider_2 = uicomponents.SpinboxSlider()
        vbox.addWidget(spinbox_slider_2)
        spinbox_slider_2.valueChanged.connect(self.widget_changed)

    def widget_changed(self, value):
        print value

def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()