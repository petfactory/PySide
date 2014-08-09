#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore
import pprint
import json

# extend QTreeView to make the treeview deselect when clicked outside the items
class DeselectableTreeView(QtGui.QTreeView):
    def mousePressEvent(self, event):
        self.clearSelection()
        QtGui.QTreeView.mousePressEvent(self, event)

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
        #self.tree_view = QtGui.QTreeView()
        # use my custom treeview class
        self.tree_view = DeselectableTreeView()
        self.tree_view.setModel(self.model)
        self.layout.addWidget(self.tree_view)
        # enable internal drag and drop
        self.tree_view.setDragDropMode(QtGui.QAbstractItemView.InternalMove)

        # button
        print_btn = QtGui.QPushButton('Print')
        self.layout.addWidget(print_btn)
        print_btn.clicked.connect(self.print_btn_clicked)

        add_btn = QtGui.QPushButton('Add')
        self.layout.addWidget(add_btn)
        add_btn.clicked.connect(self.add_btn_clicked) 

        remove_btn = QtGui.QPushButton('Remove')
        self.layout.addWidget(remove_btn)
        remove_btn.clicked.connect(self.remove_btn_clicked)

        open_btn = QtGui.QPushButton('Open')
        self.layout.addWidget(open_btn)
        open_btn.clicked.connect(self.open_btn_clicked)

        save_btn = QtGui.QPushButton('Save')
        self.layout.addWidget(save_btn)
        save_btn.clicked.connect(self.save_btn_clicked)

        dir_btn = QtGui.QPushButton('root dir')
        self.layout.addWidget(dir_btn)
        dir_btn.clicked.connect(self.dir_btn_clicked) 

        self.show()

    def populate_model(self, dir_dict):
        
        if len(dir_dict) < 1:
            print('no items in dict')
            return

        def recurse_item(dir_dict, parent_list):

            for dir_name, sub_dir in sorted(dir_dict.iteritems()):

                item = QtGui.QStandardItem(str(dir_name))
                parent_list[-1].appendRow(item)

                if isinstance(sub_dir, dict):
                    parent_list.append(item)
                    recurse_item(sub_dir, parent_list)

                elif isinstance(sub_dir, list):
                    pass

            if len(parent_list) > 1:
                parent_list.pop()
       
        parent = self.model.invisibleRootItem()
        recurse_item(dir_dict, [parent])

    def dir_btn_clicked(self):
        selected_directory = QtGui.QFileDialog.getExistingDirectory()
        print(selected_directory)

    def open_btn_clicked(self):
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Open file', directory='/home', filter='*.json')

        if(fname):
            f = open(fname, 'r')
            data = f.read()
            self.populate_model(json.loads(data))


    def save_btn_clicked(self):
        fname, _ = QtGui.QFileDialog.getSaveFileName(self, caption='Save a file', directory='/home', filter='*.json')

        if(fname):
            item = self.model.invisibleRootItem()
            ret_dict = {}
            self.recurse(item, -1, ret_dict)
            data = json.dumps(ret_dict, indent=4)

            f = open(fname,'w')
            f.write(data) # python will convert \n to os.linesep
            f.close() # you can omit in most cases as the destructor will call if



    def add_btn_clicked(self):

        if(self.tree_view.selectionModel().hasSelection()):
            for index in self.tree_view.selectedIndexes():
                item = self.model.itemFromIndex(index)
                item.appendRow(QtGui.QStandardItem('ITEM'))

        else:
            print('adding to root')
            item = self.model.invisibleRootItem()
            item.appendRow(QtGui.QStandardItem('ROOT'))


    def remove_btn_clicked(self):

        if(self.tree_view.selectionModel().hasSelection()):

            for index in self.tree_view.selectedIndexes():

                row = index.row()
                item = self.model.itemFromIndex(index)
                parent = item.parent()

                parent_index = self.model.indexFromItem(parent)
                self.model.removeRow(row, parent_index)


    def print_btn_clicked(self):
        item = self.model.invisibleRootItem()
        ret_dict = {}
        self.recurse(item, -1, ret_dict)
        pprint.pprint(ret_dict)

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
    #ex.populate_model({u'A': {u'A 1': {u'A 1 1': []}},u'B': {u'B 1': {u'B 1 1': {u'B 1 1 1': []}}},u'C': {u'C 1': {u'C 1 1': []}}})
    ex.populate_model({})
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()