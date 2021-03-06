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
        self.setWindowTitle("Test")
        

        # main layout
        mainLayout = QtGui.QVBoxLayout(self)
        mainLayout.setContentsMargins(0,0,0,0)
        
        self.menubar = QtGui.QMenuBar()
        self.menubar.setFixedHeight(20)
        mainLayout.addWidget(self.menubar)
        self.menubar.setNativeMenuBar(False)
        
        self.fileMenu = self.menubar.addMenu('File')

        export_xml_action = QtGui.QAction('Export XML', self)
        export_xml_action.triggered.connect(self.export_xml)
        self.fileMenu.addAction(export_xml_action)

        load_xml_action = QtGui.QAction('Load XML', self)
        load_xml_action.triggered.connect(self.load_xml)
        self.fileMenu.addAction(load_xml_action)

        
        self.add_quick_butons_action = QtGui.QAction('Add Quick Buttons', self)
        self.add_quick_butons_action.triggered.connect(self.refresh_button_clicked)
        self.fileMenu.addAction(self.add_quick_butons_action)
        

        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(6,6,6,6)
        mainLayout.addLayout(vbox)

        # splitter
        splitter = QtGui.QSplitter()
        vbox.addWidget(splitter)

        treeview_parent_frame = QtGui.QFrame()
        treeview_vbox = QtGui.QVBoxLayout(treeview_parent_frame)

        # treeview
        self.treeview = QtGui.QTreeView() #DeselectableTreeView()
        self.treeview.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.treeview.setAlternatingRowColors(True)
        self.treeview.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        treeview_vbox.addWidget(self.treeview)

        self.setStyleSheet('''QAbstractItemView {
                                    background-color: #aaaaaa;
                                    alternate-background-color: #bbbbbb;
                                    color: #444444;
                            }''')


        ss = '''QTreeView::branch:has-siblings:!adjoins-item {
                border-image: url(%s) 0;
            }

            QTreeView::branch:has-siblings:adjoins-item {
                border-image: url(%s) 0;
            }

            QTreeView::branch:!has-children:!has-siblings:adjoins-item {
                border-image: url(%s) 0;
            }

            QTreeView::branch:has-children:!has-siblings:closed,
            QTreeView::branch:closed:has-children:has-siblings {
                    border-image: none;
                    image: url(%s);
            }

            QTreeView::branch:open:has-children:!has-siblings,
            QTreeView::branch:open:has-children:has-siblings  {
                    border-image: none;
                    image: url(%s);
            }'''

        ss = ss % ( self.resource_path('vline.png'),
                    self.resource_path('branch-more.png'),
                    self.resource_path('branch-end.png'),
                    self.resource_path('branch-closed.png'),
                    self.resource_path('branch-open.png'))


        #print ss
        self.treeview.setStyleSheet(ss)

        treeview_button_hbox = QtGui.QHBoxLayout()
        treeview_vbox.addLayout(treeview_button_hbox)
        add_button = QtGui.QPushButton('+')
        add_button.clicked.connect(self.add_button_clicked)
        treeview_button_hbox.addWidget(add_button)

        remove_button = QtGui.QPushButton('-')
        remove_button.clicked.connect(self.remove_button_clicked)
        treeview_button_hbox.addWidget(remove_button)
        
        splitter.addWidget(treeview_parent_frame)
        self.treeview.setHeaderHidden(True)
        self.treeview.setExpandsOnDoubleClick(False)
        
        # model
        self.model = QtGui.QStandardItemModel()
        self.treeview.setModel(self.model)

        self.populateModel()


        quick_button_frame = QtGui.QFrame()
        quick_button_main_vbox = QtGui.QVBoxLayout(quick_button_frame)
        self.button_vbox = QtGui.QVBoxLayout()
        quick_button_main_vbox.addLayout(self.button_vbox)


        quick_button_main_vbox.addStretch()

        splitter.addWidget(quick_button_frame)
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
    def get_xml_recurse(q_item, xml_parent):
        '''Returns the dag_path_dict with the leaf item as key and the 
        QStandardItem as value'''

        name = q_item.text()
        xml_node = ET.Element('node')
        xml_node.set('name', name)

        xml_parent.append(xml_node)

        num_rows = q_item.rowCount()
        for row in range(num_rows):
            q_child = q_item.child(row, 0)
            HierarchyTreeview.get_xml_recurse(q_child, xml_node)


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

    def applyTint(self, path):

        temp = QtGui.QPixmap(path)
        color = QtGui.QColor(240,120,0, 255)
        painter = QtGui.QPainter(temp)
        painter.setCompositionMode(painter.CompositionMode_SourceIn)
        painter.fillRect(temp.rect(), color)
        painter.end()
        return temp

    def create_item_recurse(self, xml_node, parent_item):

        #dirName = os.path.dirname(os.path.realpath(__file__))
        #icon_path = os.path.join(dirName, r'switch.png')
        icon_path = self.resource_path(r'switch.png')

        name = xml_node.get('name')
        #node = Node(name)

        item = QtGui.QStandardItem(name)

        if name.startswith('G__'):

            pixmap = self.applyTint(icon_path)
            icon = QtGui.QIcon(pixmap)
            item.setIcon(icon)

        #item.setSizeHint(QtCore.QSize(0,20))
        
        #customData = CustomType(node)
        #item.setData(customData, QtCore.Qt.UserRole + 1)
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

        #dirName = os.path.dirname(os.path.realpath(__file__))
        xmlPath = self.resource_path(r'scenegraph.xml')
        #xmlPath = os.path.join(dirName, )

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

    def export_xml(self):
        
        xml_parent = ET.Element('root')
        q_item = self.model.invisibleRootItem()

        num_rows = q_item.rowCount()
        for row in range(num_rows):
            q_child = q_item.child(row, 0)
            HierarchyTreeview.get_xml_recurse(q_child, xml_parent)

        xmlString = ET.tostring(xml_parent)
        miniDomXml = xml.dom.minidom.parseString(xmlString)
        prettyXML = miniDomXml.toprettyxml()
        #print(prettyXML)

        fname, _ = QtGui.QFileDialog.getSaveFileName(caption='Save XML', directory='', filter='*.xml')

        if(fname):
            f = open(fname,'w')
            f.write(prettyXML)
            f.close()

def main():
    
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    win = HierarchyTreeview()
    win.show()
    win.treeview.expandAll()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
