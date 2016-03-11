#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import sys, os
import xml.etree.ElementTree as ET
import xml.dom.minidom
from functools import partial
import petfactoryStyle
reload(petfactoryStyle)
import petfactoryStyle.compile_qrc

class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(20, 60, 300, 200)
        self.setWindowTitle('Test')

        # layout
        vbox = QtGui.QVBoxLayout(self)
        
        # treeview
        self.treeview = QtGui.QTreeView() #DeselectableTreeView()
        self.treeview.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.treeview.setAlternatingRowColors(True)
        self.treeview.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeview.setHeaderHidden(True)
        vbox.addWidget(self.treeview)

        # model
        self.model = QtGui.QStandardItemModel()
        self.treeview.setModel(self.model)

        self.populateModel()


    def cleanModel(self):
         numRows = self.model.rowCount()
         for row in range(numRows):
             self.model.removeRow(0)

    def create_item_recurse(self, xml_node, parent_item):

        name = xml_node.get('name')
        item = QtGui.QStandardItem(name)

        parent_item.appendRow(item)

        xml_children = xml_node.getchildren()

        if xml_children:

            for xml_child in xml_children:

                self.create_item_recurse(xml_child, item)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def populateModel(self):

        xmlPath = self.resource_path(r'scenegraph.xml')

        if not os.path.isfile(xmlPath):
            print('The xml file does not exist: {}'.format(xmlPath))
            return

        xml_tree = ET.parse(xmlPath)
        xml_root = xml_tree.getroot()

        self.cleanModel()
        root_item = self.model.invisibleRootItem()

        self.create_item_recurse(xml_root, root_item)

    def load_xml(self):

        fname, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Open file', directory='/home', filter='*.xml')

        if(fname):

            tree = ET.parse(fname)
            xml_root = tree.getroot()

            root_item = self.model.invisibleRootItem()
            self.cleanModel()

            xml_children = xml_root.getchildren()
            if xml_children:

                for xml_child in xml_children:

                    self.create_item_recurse(xml_child, root_item)     

def main():
    
    petfactoryStyle.compile_qrc.compile_all()
    app = QtGui.QApplication(sys.argv)
    win = BaseWin()
    app.setStyleSheet(petfactoryStyle.load_stylesheet())
    win.show()
    win.treeview.expandAll()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()