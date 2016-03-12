#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore


class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(5, 50, 600, 500)
        self.setWindowTitle('Test')

        self.image_dict = {}
        self.image_dict['blue'] = QtGui.QGraphicsPixmapItem(QtGui.QPixmap('blue.png'))
        self.image_dict['green'] = QtGui.QGraphicsPixmapItem(QtGui.QPixmap('green.png'))
        self.image_dict['red'] = QtGui.QGraphicsPixmapItem(QtGui.QPixmap('red.png'))

        self.scene = QtGui.QGraphicsScene()
    
        self.model = QtGui.QStandardItemModel()    

        self.tableview = QtGui.QTableView()
        header = self.tableview.horizontalHeader()
        header.setStretchLastSection(True)
        #self.tableview.setAlternatingRowColors(True)
        self.tableview.setModel(self.model)
        self.tableview.clicked.connect(self.tableview_clicked)
        self.add_items()
        self.model.setHorizontalHeaderLabels(['Layers'])

        view = QtGui.QGraphicsView(self.scene)
        #updateSceneRect
        view.setSceneRect(0,0,800,600)        

        splitter =  QtGui.QSplitter(self)
        splitter.addWidget(self.tableview)
        splitter.addWidget(view)

    def tableview_clicked(self, index):
        z_value = index.row()
        item = self.model.itemFromIndex(index)
        pixmapItem = self.image_dict.get(item.text())
        if not pixmapItem:
            return

        if item.checkState() == QtCore.Qt.CheckState.Checked:
            pixmapItem.setZValue(z_value)
            self.scene.addItem(pixmapItem)
        else:
            self.scene.removeItem(pixmapItem)



    def add_items(self):

        name_list = ['blue', 'green', 'red']

        for row, item in enumerate(name_list):

            item = QtGui.QStandardItem(item)
            
            item.setCheckable(True)
            self.model.setItem(row, 0, item)



def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()