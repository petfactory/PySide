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


class ScrollArea(QtGui.QScrollArea):

    def __init__(self, parent=None):
        super(ScrollArea, self).__init__(parent)
        self.lastX = None
        self.lastY = None

        self.clicked = Signal()

    def mousePressEvent(self, event):
        
        xWin = event.x()
        yWin = event.y()

        xScroll = self.horizontalScrollBar().value()
        yScroll = self.verticalScrollBar().value()

        x = xWin + xScroll
        y = yWin + yScroll

        self.clicked.emit(QtCore.QPoint(x, y))

class CanvasWidget(QtGui.QWidget):
    
    def __init__(self, parent=None):

        super(CanvasWidget, self).__init__(parent)
        self.setFixedSize(400,400)
        self._parent = parent
        self.fontSize = 12
        self.font = 'Arial'
        self.strokeColor = QtGui.QColor(242, 165, 12)

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp):
      
        qp.setPen(self.strokeColor)
        qp.setFont(QtGui.QFont(self.font, self.fontSize))

        for name, infoDict in self._parent.hitInfoDict.iteritems():

            polygon = infoDict.get('polygon')
            labelPos = infoDict.get('labelPos')

            qp.drawPolyline(polygon)
            qp.drawText(labelPos, name)


class SortableDelegate(QtGui.QItemDelegate):
    
    def __init__(self, parent=None):
        super(SortableDelegate, self).__init__(parent)
        
    def createEditor(self, parent, option, index):
        
        #col = index.column()

        spinBox = QtGui.QSpinBox(parent)
        spinBox.setRange(0,9999)
        return spinBox

class AddHitAreaWin(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(AddHitAreaWin, self).__init__(parent) 

        self.setGeometry(980, 50, 300, 350)
        self.setWindowTitle('Add Hit Area')
 
        vbox = QtGui.QVBoxLayout(self)
        gridLayout = QtGui.QGridLayout()

        vbox.addLayout(gridLayout)

        addTargetNodeButton = QtGui.QPushButton('Add Node')
        addTargetNodeButton.setFixedWidth(130)
        gridLayout.addWidget(addTargetNodeButton, 0, 0)

        self.addTargetNodeLineEdit = QtGui.QLineEdit()
        gridLayout.addWidget(self.addTargetNodeLineEdit, 0, 1)

        setLabelPosButton = QtGui.QPushButton('Set Label Pos')
        setLabelPosButton.setFixedWidth(130)
        setLabelPosButton.clicked.connect(self.setLabelPosButtonClicked)
        gridLayout.addWidget(setLabelPosButton, 1, 0)
        

        labelPosHbox = QtGui.QHBoxLayout()
        gridLayout.addLayout(labelPosHbox, 1,1)

        self.labelPosXSpinBox = QtGui.QSpinBox()
        self.labelPosXSpinBox.setRange(0,9999)
        labelPosHbox.addWidget(self.labelPosXSpinBox)
        self.labelPosYSpinBox = QtGui.QSpinBox()
        self.labelPosYSpinBox.setRange(0,9999)
        labelPosHbox.addWidget(self.labelPosYSpinBox)

        appendVertexButton = QtGui.QPushButton('Append Vertex')
        appendVertexButton.setFixedWidth(130)
        appendVertexButton.clicked.connect(self.appendVertexButtonClicked)
        gridLayout.addWidget(appendVertexButton, 2, 0, QtCore.Qt.AlignTop)
        
        self.vertexModel = QtGui.QStandardItemModel()
        self.vertexModel.setHorizontalHeaderLabels(['X', 'Y'])


        self.hitAreaTableView = QtGui.QTableView()
        self.hitAreaTableView.setModel(self.vertexModel)
        self.hitAreaTableView.setItemDelegate(SortableDelegate(self.hitAreaTableView))
        self.hitAreaTableView.horizontalHeader().setStretchLastSection(True)
        self.hitAreaTableView.setAlternatingRowColors(True)
        self.hitAreaTableView.verticalHeader().hide()
        self.hitAreaTableView.setColumnWidth(0,50)
        gridLayout.addWidget(self.hitAreaTableView, 2, 1)


        removeAllVertexButton = QtGui.QPushButton('Remove Vertices')
        gridLayout.addWidget(removeAllVertexButton, 3, 1)
        removeAllVertexButton.clicked.connect(self.removeAllVertexButtonClicked)



        addHitAreaButton = QtGui.QPushButton('Add Hit Area')
        addHitAreaButton.clicked.connect(self.addHitAreaButtonClicked)
        vbox.addWidget(addHitAreaButton)

        self.setLabelPosClicked = Signal()
        self.appendVertexClicked = Signal()
        self.addHitAreaClicked = Signal()
        self.addHitAreaCanceled = Signal()

    def removeAllVertexButtonClicked(self):
        self.cleanModel(self.vertexModel)

    def cleanModel(self, model):
         numRows = model.rowCount()
         for row in range(numRows):
             model.removeRow(0)

    def addVertexPos(self, x, y):

        numRows = self.vertexModel.rowCount()

        vertexItemX = switchNameItem = QtGui.QStandardItem(str(x))
        #variantSetItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        vertexItemY = switchNameItem = QtGui.QStandardItem(str(y))
        #variantSetItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        self.vertexModel.setItem(numRows, 0, vertexItemX)
        self.vertexModel.setItem(numRows, 1, vertexItemY)


    def setLabelPosButtonClicked(self):
        self.setLabelPosClicked.emit(TestSignal.SET_LABEL_POS_STATE)

    def appendVertexButtonClicked(self):
        self.appendVertexClicked.emit(TestSignal.APPEND_VERTEX_STATE)

    def addHitAreaButtonClicked(self):
        self.addTargetNodeLineEdit.setText('')
        self.labelPosXSpinBox.setValue(0)
        self.labelPosYSpinBox.setValue(0)
        self.cleanModel(self.vertexModel)
        #self.addHitAreaClicked.emit(TestSignal.ADD_HIT_AREA_STATE)
        self.addHitAreaClicked.emit(TestSignal.VRED_STATE)

    def closeEvent(self, event):

        self.addHitAreaClicked.emit(TestSignal.ADD_HIT_AREA_CANCELED_STATE)

        '''
        if False:
            event.accept()
        else:
            event.ignore()
        '''




class TestSignal(QtGui.QWidget):
    
    VRED_STATE = 'VRED_STATE'
    SET_LABEL_POS_STATE = 'SET_LABEL_POS_STATE'
    APPEND_VERTEX_STATE = 'APPEND_VERTEX_STATE'
    ADD_HIT_AREA_STATE = 'ADD_HIT_AREA_STATE'
    ADD_HIT_AREA_CANCELED_STATE = 'ADD_HIT_AREA_CANCELED_STATE'

    def __init__(self, parent=None):
        super(TestSignal, self).__init__(parent) 

        self.addHitAreaWin = None
        self._state = TestSignal.VRED_STATE

        self.setGeometry(980, 50, 380, 350)
        self.setWindowTitle('Add Polygons ads')

        # main layout
        mainLayout = QtGui.QVBoxLayout(self)
        mainLayout.setContentsMargins(0,0,0,0)

        self.menubar = QtGui.QMenuBar()
        #self.menubar.setFixedHeight(20)
        mainLayout.addWidget(self.menubar)
        self.menubar.setNativeMenuBar(False)
        self.fileMenu = self.menubar.addMenu('File')

        self.addHitAreaAction = QtGui.QAction('Add Hit Area', self)
        self.addHitAreaAction.triggered.connect(self.openAddHitAreaWin)
        self.fileMenu.addAction(self.addHitAreaAction)

        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(6,6,6,6)
        mainLayout.addLayout(vbox)

        scrollArea = ScrollArea()
        vbox.addWidget(scrollArea)

        hitAreaDict =   {   'G__FIRST':  {  'labelPos':(30,60),
                                            'hitAreaVerts':[(10, 40),
                                                            (110, 10),
                                                            (110, 110),
                                                            (60, 90)]
                                        },

                            'G__SECOND':  { 'labelPos':(110,140),
                                            'hitAreaVerts':[(100, 120),
                                                            (200, 120),
                                                            (200, 200),
                                                            (100, 170)]
                                        },

                            'X':  {         'labelPos':(255, 140),
                                            'hitAreaVerts':[(250, 120),
                                                            (300, 120),
                                                            (250, 160)]
                                        }
                        }

        self.hitInfoDict = self.parseInfo(hitAreaDict)

        canvasWidget = CanvasWidget(self)
        scrollArea.setWidget(canvasWidget)
        scrollArea.clicked.connect(self.scrollClicked)



    def setState(self, state):

        if state == TestSignal.ADD_HIT_AREA_CANCELED_STATE:
            newState = TestSignal.VRED_STATE

        elif self._state == TestSignal.ADD_HIT_AREA_STATE:
            newState = TestSignal.VRED_STATE

        else:
            newState = state

        print 'Current State -> {}'.format(self._state)

        self._state = newState

        print 'State Set to -> {}'.format(self._state)

    def openAddHitAreaWin(self):

        if self.addHitAreaWin is None:
            self.addHitAreaWin = AddHitAreaWin()

        self.addHitAreaWin.show()

        self.addHitAreaWin.setLabelPosClicked.connect(self.setState)
        self.addHitAreaWin.appendVertexClicked.connect(self.setState)
        self.addHitAreaWin.addHitAreaClicked.connect(self.setState)
        self.addHitAreaWin.addHitAreaCanceled.connect(self.setState)

    def scrollClicked(self, point, *args):

        print 'Current State -> {}'.format(self._state)

        if self._state == TestSignal.VRED_STATE:

            #print point, args
            for name, infoDict in self.hitInfoDict.iteritems():

                polygon = infoDict.get('polygon')
                hit = polygon.containsPoint(point, QtCore.Qt.OddEvenFill)
                if hit:
                    print '{} was clicked'.format(name)
                    return

            print 'No hit'

        elif self._state == TestSignal.SET_LABEL_POS_STATE:

            if self.addHitAreaWin is None:
                print 'addHitAreaWin is not initialized!'
                return

            self.addHitAreaWin.labelPosXSpinBox.setValue(point.x())
            self.addHitAreaWin.labelPosYSpinBox.setValue(point.y())


        elif self._state == TestSignal.APPEND_VERTEX_STATE:

            if self.addHitAreaWin is None:
                print 'addHitAreaWin is not initialized!'
                return

            self.addHitAreaWin.addVertexPos(point.x(), point.y())


    def parseInfo(self, hitAreaDict):

        retDict = {}

        for name, infoDict in hitAreaDict.iteritems():

            labelPosTuple = infoDict.get('labelPos')
            hitAreaVerts = infoDict.get('hitAreaVerts')

            posList = [QtCore.QPoint(p[0], p[1]) for p in hitAreaVerts]
            polygon = polygon = QtGui.QPolygon(posList)

            labelPos = QtCore.QPoint(labelPosTuple[0], labelPosTuple[1])
            retDict[name] = {"labelPos":labelPos, 'polygon':polygon}
        
        return retDict

def main():
    
    app = QtGui.QApplication(sys.argv)
    win = TestSignal()
    win.show()
    #addHitAreaWin = AddHitAreaWin()
    #addHitAreaWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()