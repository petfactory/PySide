#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore
import pprint

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      
        
        self.setGeometry(50, 50, 300, 300)
        self.setWindowTitle('Tree View')

        # layout
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(6,6,6,6)

        # model
        self.model = QtGui.QStandardItemModel()

        # tree view
        self.view = QtGui.QTreeView()
        self.view.setModel(self.model)
        self.layout.addWidget(self.view)

        # button
        print_btn = QtGui.QPushButton('Print')
        self.layout.addWidget(print_btn)
        print_btn.clicked.connect(self.print_btn_clicked)

        add_btn = QtGui.QPushButton('Add')
        self.layout.addWidget(add_btn)
        add_btn.clicked.connect(self.add_btn_clicked) 

        d = 'ABCDEFG'

        # create some items to store in the model
        items = []
        for i in range(3):
            item_1 = QtGui.QStandardItem('{0}_{1}'.format(d[i], i))
            items.append(item_1)
            
            for j in range (i):
                item_2 = QtGui.QStandardItem('{0}_{1}{2}'.format(d[i],i,j))
                item_1.appendRow(item_2)

                for k in range (i):
                    item_2.appendRow(QtGui.QStandardItem('{0}_{1}{2}{3}'.format(d[i],i,j,k)))

        self.model.appendColumn(items)

        #pprint.pprint(items)
        self.show()

    
    def add_btn_clicked(self):
        sender = self.sender()
        print(sender)


    def print_btn_clicked(self):
        item = self.model.invisibleRootItem()
        ret_dict = {}
        self.recurse(item, -1, ret_dict)
        #pprint.pprint(ret_dict)

    def recurse(self, item, depth, ret_dict):

        # returns the number of child item rows that the item has.
        for i in range(item.rowCount()):
            child = item.child(i)
            
            if child.hasChildren():
                depth += 1
                print('{0}{1}'.format('\t'*depth, child.text()))
                cd = {}
                ret_dict.update({child.text():cd})
                self.recurse(child, depth, cd)

            else:
                depth += 1
                print('{0}{1}'.format('\t'*depth, child.text()))
                ret_dict.update({child.text():[]})

            depth -= 1
    

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()