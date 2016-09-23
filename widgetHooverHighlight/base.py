#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore

def apa():
    print 12

class MySpinBox(QtGui.QDoubleSpinBox) :
    def __init__(self, *args, **kwargs):
        QtGui.QDoubleSpinBox.__init__(self, *args, **kwargs)
        self.setMouseTracking(True)
        for child in self.children():
            print child
            try:
                child.setMouseTracking(True)
            except AttributeError:pass

    def mouseMoveEvent(self, event):
        print 1212

class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(50, 100, 300, 300)
        self.setWindowTitle('Test')
        
        self.vbox = QtGui.QVBoxLayout(self)

        self.scene = QtGui.QGraphicsScene()
        self.scene.addPixmap(QtGui.QPixmap('base.png'))
        view = QtGui.QGraphicsView(self.scene)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        view.setSceneRect(0, 0, 300, 240)
        view.setFixedSize(302, 242)
        self.vbox.addWidget(view)

        self.uiVbox = QtGui.QVBoxLayout()
        self.vbox.addLayout(self.uiVbox)
        self.uiVbox.setContentsMargins(6, 6, 6, 6)

        self.origoLabel, self.origoSpinbox, self.origoGraphic = self.addSpinBox('Origo', 'arrow.png', (0, 0))
        self.camDistLabel, self.camDistSpinbox, self.camDistGraphic = self.addSpinBox('Camera dist', 'arrow.png', (0, 0))
        self.camPitchLabel, self.camPitchSpinbox, self.camPitchGraphic  = self.addSpinBox('Camera pitch', 'arrow.png', (0, 50))
        self.camJawLabel, self.camJawSpinbox, self.camJawGraphic  = self.addSpinBox('Camera jaw', 'arrow.png', (0, 100))
        self.focallength, self.focallengthSpinbox, self.focallengthGraphic  = self.addSpinBox('Focallength', 'arrow.png', (0, 150))

        #self.useExistingCamCB = QtGui.QCheckBox('Use Existing Camera')
        self.useExistingCamGroup = QtGui.QGroupBox('Use Existing Camera')
        self.useExistingCamGroup.setLayout(QtGui.QVBoxLayout())
        self.existingCameraName = QtGui.QLineEdit()
        self.useExistingCamGroup.layout().addWidget(self.existingCameraName)
        self.useExistingCamGroup.setCheckable(True)
        self.uiVbox.addWidget(self.useExistingCamGroup )

        self.changeFocallengthGroup = QtGui.QGroupBox('Change Focallength')
        self.changeFocallengthGroup.setLayout(QtGui.QVBoxLayout())
        self.newFocallengthSpinbox = QtGui.QDoubleSpinBox()
        self.changeFocallengthGroup.layout().addWidget(self.newFocallengthSpinbox)
        self.changeFocallengthGroup.setCheckable(True)
        self.uiVbox.addWidget(self.changeFocallengthGroup )

        createAnimCB = QtGui.QCheckBox('Animate Turntable')
        self.uiVbox.addWidget(createAnimCB)

        self.vbox.addStretch()
        
        createButton = QtGui.QPushButton('Create')
        self.uiVbox.addWidget(createButton)


    def addSpinBox(self, name, graphicName, graphicPos):

        hbox = QtGui.QHBoxLayout()
        self.uiVbox.addLayout(hbox)

        label = QtGui.QLabel(name)
        label.setFixedWidth(80)
        label.installEventFilter(self)
        label.setMouseTracking(True)
        hbox.addWidget(label)

        spinbox = QtGui.QDoubleSpinBox()
        hbox.addWidget(spinbox)

        graphic = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(graphicName))
        graphic.setPos(*graphicPos)
        self.scene.addItem(graphic)
        graphic.setOpacity(0)

        return (label, spinbox, graphic)

    def eventFilter(self, widget, event):
        
        if event.type() == QtCore.QEvent.MouseMove:
            if widget == self.camDistLabel:
                #print 'camDistSpinbox'
                self.camDistGraphic.setOpacity(1)
                self.camPitchGraphic.setOpacity(0)
                self.camJawGraphic.setOpacity(0)
            elif widget == self.camPitchLabel:
                #print 'camPitchSpinbox'
                self.camDistGraphic.setOpacity(0)
                self.camPitchGraphic.setOpacity(1)
                self.camJawGraphic.setOpacity(0)
            elif widget == self.camJawLabel:
                #print 'camJawSpinbox'
                self.camDistGraphic.setOpacity(0)
                self.camPitchGraphic.setOpacity(0)
                self.camJawGraphic.setOpacity(1)
            return True

        return QtGui.QWidget.eventFilter(self, widget, event)



def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()