#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys, os
from PySide import QtGui, QtCore


class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(5, 50, 600, 500)
        self.setWindowTitle('Test')

        self.image_dict = {}
        self.image_dict['blue'] = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(self.resource_path('blue.png')))
        self.image_dict['green'] = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(self.resource_path('green.png')))
        self.image_dict['red'] = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(self.resource_path('red.png')))

        self.scene = QtGui.QGraphicsScene()
    
        self.model = QtGui.QStandardItemModel()
        self.model.itemChanged.connect(self.item_changed)

        self.tableview = QtGui.QTableView()
        header = self.tableview.horizontalHeader()
        header.setStretchLastSection(True)
        #self.tableview.setAlternatingRowColors(True)
        self.tableview.setModel(self.model)
        #self.tableview.clicked.connect(self.tableview_clicked)
        self.add_items()
        self.model.setHorizontalHeaderLabels(['Layers'])

        view = QtGui.QGraphicsView(self.scene)
        view.setSceneRect(0,0,800,600)        

        splitter = QtGui.QSplitter(self)
        splitter.addWidget(self.tableview)
        splitter.addWidget(view)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def item_changed(self, item):

        z_value = item.row()
        pixmapItem = self.image_dict.get(item.text())
        if not pixmapItem:
            return

        if item.checkState() == QtCore.Qt.CheckState.Checked:
            pixmapItem.setZValue(z_value)
            self.scene.addItem(pixmapItem)
        else:
            self.scene.removeItem(pixmapItem)


    def add_items(self):

        self.model.blockSignals(True)

        name_list = ['blue', 'green', 'red']

        for row, item in enumerate(name_list):

            item = QtGui.QStandardItem(item)
            
            item.setCheckable(True)
            self.model.setItem(row, 0, item)

        self.model.blockSignals(False)



def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()