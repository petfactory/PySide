#!/usr/bin/python

from PySide import QtCore, QtGui
import pprint
import sys
import qdarkstyle
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
from functools import partial


class CustomType(object):
    
    def __init__(self, node):
        self._node = node
        
    def getNode(self):
        return self._node

class DeselectableTreeView(QtGui.QTreeView):
    
    # deselect when clicked outside the items
    def mousePressEvent(self, event):
        self.clearSelection()
        QtGui.QTreeView.mousePressEvent(self, event)
        
    # disable doubleclick
    def edit(self, index, trigger, event):
        if trigger == QtGui.QAbstractItemView.DoubleClicked:
            return False
        return QtGui.QTreeView.edit(self, index, trigger, event)

class HierarchyTreeview(QtGui.QWidget):
 
    def __init__(self, parent=None):
 
        super(HierarchyTreeview, self).__init__(parent)

        self.dag_path_dict = None
        self.button_list = []

        self.setWindowFlags(QtCore.Qt.Tool)

        self.setGeometry(10, 50, 600, 400)
        self.setWindowTitle("TEST")
                
        vbox = QtGui.QVBoxLayout(self)
        vbox.setContentsMargins(0,0, 0, 0)

        # splitter
        splitter = QtGui.QSplitter()
        vbox.addWidget(splitter)

        treeview_parent_frame = QtGui.QFrame()
        treeview_vbox = QtGui.QVBoxLayout(treeview_parent_frame)

        # treeview
        self.treeview = QtGui.QTreeView() #DeselectableTreeView()
        self.treeview.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.treeview.setAlternatingRowColors(True)
        treeview_vbox.addWidget(self.treeview)

        refresh_button = QtGui.QPushButton('Refresh')
        refresh_button.clicked.connect(self.refresh_button_clicked)
        treeview_vbox.addWidget(refresh_button)

        add_button = QtGui.QPushButton('+')
        add_button.clicked.connect(self.add_button_clicked)
        treeview_vbox.addWidget(add_button)

        remove_button = QtGui.QPushButton('-')
        remove_button.clicked.connect(self.remove_button_clicked)
        treeview_vbox.addWidget(remove_button)
        
        splitter.addWidget(treeview_parent_frame)
        self.treeview.setHeaderHidden(True)
        self.treeview.setExpandsOnDoubleClick(False)
        
        # model
        self.model = QtGui.QStandardItemModel()
        self.treeview.setModel(self.model)

        self.populateModel()

        #self.treeview.setStyleSheet(
        ''' QTreeView {
                alternate-background-color: #AAAAAA;
                background: #A2A2A2;
                color: rgb(90, 90, 90);
                selection-background-color: #555555;
            }
            QTreeView::item:focus {
              background-color: #555555;
              color: #ffcc00;
            }

            QTreeView::branch::closed::has-children {
                image: url(branch_closed.png);
            }

            QTreeView::branch::open::has-children {
                image: url(branch_open.png);
            }
        '''
        #)


        #self.setStyleSheet(
        '''
            QPushButton {
                background-color: #AAAAAA;
                color: #222222;
                max-height: 20px;
                font: 11px;
            }

            QPushButton:pressed {
                background-color: #AAAAAA;
                color: #555555;
                max-height: 20px;
                font: 11px;
            }

            QFrame {
                background-color: #888888;
            }

            QSplitter::handle {
                image: url(branch_open.png);
            }

            QSplitter::handle:pressed {
                image: url(branch_closed.png);
            }
            '''
        #)

        button_widget = QtGui.QWidget()

        button_main_vbox = QtGui.QVBoxLayout(button_widget)

        self.button_vbox = QtGui.QVBoxLayout()
        button_main_vbox.addLayout(self.button_vbox)
        button_main_vbox.addStretch()

        splitter.addWidget(button_widget)
        splitter.setSizes([400, 200])


    def add_button_clicked(self):

        if(self.treeview.selectionModel().hasSelection()):
            for index in self.treeview.selectedIndexes():
                item = self.model.itemFromIndex(index)
                item.appendRow(QtGui.QStandardItem('ITEM'))

        else:
            #print('adding to root')
            item = self.model.invisibleRootItem()
            item.appendRow(QtGui.QStandardItem('ROOT'))


    def remove_button_clicked(self):

        if(self.treeview.selectionModel().hasSelection()):

            for index in self.treeview.selectedIndexes():

                row = index.row()
                item = self.model.itemFromIndex(index)
                parent = item.parent()

                parent_index = self.model.indexFromItem(parent)
                self.model.removeRow(row, parent_index)

    @staticmethod
    def get_item_recurse(item, dag_path_dict, parent_list=None):
        '''Returns the dag_path_dict with the leaf item as key and the 
        QStandardItem as value'''

        if parent_list is None:
            parent_list = []

        name = item.text()
        parent_list.append(str(name))

        leaf_name = parent_list[-1] 
        if leaf_name in dag_path_dict:
            print 'Warning! "{}" is alreadey in dict'.format(leaf_name)

        dag_path_dict[leaf_name] = item

        num_rows = item.rowCount()
        for row in range(num_rows):
            child = item.child(row, 0)
            HierarchyTreeview.get_item_recurse(child, dag_path_dict, parent_list)

        parent_list.pop()


    @staticmethod
    def get_full_path_recurse(item, dag_path_dict, parent_list=None):
        '''Returns the dag_path_dict with the leaf item as key and the 
        full path (tuple) as value'''

        if parent_list is None:
            parent_list = []

        name = item.text()
        parent_list.append(str(name))

        leaf_name = parent_list[-1] 
        if leaf_name in dag_path_dict:
            print 'Warning! "{}" is alreadey in dict'.format(leaf_name)

        dag_path_dict[leaf_name] = tuple(parent_list[:-1])

        num_rows = item.rowCount()
        for row in range(num_rows):
            child = item.child(row, 0)
            HierarchyTreeview.get_full_path_recurse(child, dag_path_dict, parent_list)

        parent_list.pop()


    def refresh_button_clicked(self):

        root_item = self.model.invisibleRootItem()
        # get the first child, since we will select the root node in VRED it will be similar.
        # this would not work if the invisible root item had more then one child and we wanted to
        # print them all.
        child = root_item.child(0, 0)
        self.dag_path_dict = {}
        HierarchyTreeview.get_item_recurse(child, self.dag_path_dict)
        #HierarchyTreeview.get_full_path_recurse(child, self.dag_path_dict)
        #pprint.pprint(self.dag_path_dict)

        keys = self.dag_path_dict.keys()

        for button in self.button_list:
            button.deleteLater()

        self.button_list = []

        for name in ['INT_DRIVER_SEAT', 'G__INT_DRIVER_SEAT', 'INT_PASSENGER_SEAT', 'G__INT_PASSENGER_SEAT', 'ROOF']:
            if name in keys:
                self.add_button(name, self.dag_path_dict[name], self.button_vbox)


    def add_button(self, name, item, layout):

        button = QtGui.QPushButton(name)
        button.clicked.connect(partial(self.button_clicked, name, item))
        layout.addWidget(button)
        self.button_list.append(button)

    def button_clicked(self, name, item):
        #print (name, item)
        self.treeview.setCurrentIndex(item.index())

    def cleanModel(self):
         numRows = self.model.rowCount()
         for row in range(numRows):
             self.model.removeRow(0)

    def create_item_recurse(self, xml_node, parent_item):

        name = xml_node.get('name')
        #node = Node(name)

        item = QtGui.QStandardItem(name)
        #item.setSizeHint(QtCore.QSize(0,20))
        
        #customData = CustomType(node)
        #item.setData(customData, QtCore.Qt.UserRole + 1)
        parent_item.appendRow(item)

        xml_children = xml_node.getchildren()

        if xml_children:

            for xml_child in xml_children:

                self.create_item_recurse(xml_child, item)

    def populateModel(self):

        dirName = os.path.dirname(os.path.realpath(__file__))
        xmlPath = os.path.join(dirName, r'scenegraph.xml')

        if not os.path.isfile(xmlPath):
            print('The xml file does not exist: {}'.format(xmlPath))
            return

        xml_tree = ET.parse(xmlPath)
        xml_root = xml_tree.getroot()

        self.cleanModel()
        root_item = self.model.invisibleRootItem()

        self.create_item_recurse(xml_root, root_item)


def main():
    
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    win = HierarchyTreeview()
    win.show()
    win.treeview.expandAll()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
