from functools import partial

from PySide import QtGui, QtCore

class SpinboxSlider(QtGui.QWidget):
    """docstring for SpinboxSlider"""

    valueChanged = QtCore.Signal(int)

    def __init__(self):
        super(SpinboxSlider, self).__init__()

        self.range = (0, 100)
        hbox = QtGui.QHBoxLayout(self)

        self.slider = QtGui.QSlider()
        hbox.addWidget(self.slider)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setRange(*self.range)
        
        self.spinbox = QtGui.QSpinBox()
        hbox.addWidget(self.spinbox)
        self.spinbox.setRange(*self.range)

        self.slider.valueChanged.connect(partial(self.spinbox_slider_update, self.spinbox))
        self.spinbox.valueChanged.connect(partial(self.spinbox_slider_update, self.slider))


    def spinbox_slider_update(self, widget, value):
        widget.blockSignals(True)
        widget.setValue(value)
        widget.blockSignals(False)
        self.valueChanged.emit(value)

    def setRange(self, min_, max_):
        self.range = (min_, max_)
        self.slider.setRange(*self.range)
        self.spinbox.setRange(*self.range)

        