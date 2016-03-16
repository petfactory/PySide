#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys, os
from PySide import QtGui, QtCore
import petfactoryStyle

'''
# custom data
class MyPixmapData(object):
    
    def __init__(self, pixmap):
        self.pixmap = pixmap

class ParentItem(QtGui.QStandardItem):
    
    def __init__(self, *args):
        super(ParentItem, self).__init__(*args)

    def clone(self):
        return ParentItem()

    def type(self):
        return QtGui.QStandardItem.UserType+1

class ChildItem(QtGui.QStandardItem):
    
    def __init__(self, *args):
        super(ChildItem, self).__init__(*args)

    def clone(self):
        return ChildItem()

    def type(self):
        return QtGui.QStandardItem.UserType+2
'''

class MyTreeView(QtGui.QTreeView):
    
    def __init__(self):
        super(MyTreeView, self).__init__() 

    def mousePressEvent(self, event):
        
        index = self.indexAt(event.pos())
        model = index.model()
        if model is not None:

            clicked_row = index.row()
            parent_index = index.parent()

            #model.blockSignals(True)
            parent_item = model.itemFromIndex(parent_index)

            if parent_item is not None:

                for row in range(parent_item.rowCount()):
                    child_item = parent_item.child(row)
                    if row != clicked_row:
                        child_item.setCheckState(QtCore.Qt.CheckState.Unchecked)

            #model.blockSignals(False)
            self.update()

        QtGui.QTreeView.mousePressEvent(self, event)


#class BaseWin(QtGui.QWidget):
class BaseWin(QtGui.QMainWindow):
    
    PARENT_ITEM = 0
    CHILD_ITEM = 1

    DATA_ITEM_TYPE = QtCore.Qt.UserRole
    DATA_PIXMAP_KEY = QtCore.Qt.UserRole+1
    #DATA_Z_VALUE = QtCore.Qt.UserRole+2


    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(5, 50, 600, 500)
        self.setWindowTitle('Test')
        self.layer_dict = {}

        self.valid_ext = ['.png', '.jpg', '.jpeg']

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        file_menu = menubar.addMenu('&File')

        #exit_action = QtGui.QAction('Exit', self)
        #exit_action.setShortcut('Ctrl+Q')
        #exit_action.setStatusTip('Exit application')
        #exit_action.triggered.connect(self.close)
        #file_menu.addAction(exit_action)


        open_action = QtGui.QAction(QtGui.QIcon(self.resource_path('open_dir.png')), '&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open directory')
        open_action.triggered.connect(self.open_dir)
        file_menu.addAction(open_action)

        #self.toolbar = self.addToolBar('Open')
        #self.toolbar.addAction(open_action)


        self.scene = QtGui.QGraphicsScene()
    
        self.model = QtGui.QStandardItemModel()

        ''' Set the item prototype
        self.model.setItemPrototype(ParentItem()) '''

        self.model.itemChanged.connect(self.item_changed)
        self.model.rowsRemoved.connect(self.rows_removed)

        #self.treeview = QtGui.QTreeView()
        self.treeview = MyTreeView()
        self.treeview.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        
        self.treeview.setDragEnabled(True)
        self.treeview.setDragDropMode(QtGui.QAbstractItemView.InternalMove)

        self.treeview.setHeaderHidden(True)
        self.treeview.setModel(self.model)
        self.treeview.setAlternatingRowColors(True)
        self.model.setHorizontalHeaderLabels(['Layers'])

        self.view = QtGui.QGraphicsView(self.scene)
        #self.view.setSceneRect(0,0,800,600)        

        splitter = QtGui.QSplitter(self)
        self.setCentralWidget(splitter)

        left_frame = QtGui.QFrame()
        left_frame.setMinimumWidth(200)
        left_vbox = QtGui.QVBoxLayout(left_frame)
        left_vbox.addWidget(self.treeview)

        splitter.addWidget(left_frame)
        
        right_frame = QtGui.QFrame()
        right_vbox = QtGui.QVBoxLayout(right_frame)
        right_vbox.addWidget(self.view)
        splitter.addWidget(right_frame)


        splitter.setSizes([100, 600])

        self.load_assets(self.resource_path('./assets'))

        self.treeview.installEventFilter(self)

    def rows_removed(self, parent, first, last):
        
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 0)

            for child_row in range(item.rowCount()):
                child_item = item.child(child_row)
                pixmap_item = self.layer_dict.get(child_item.data(BaseWin.DATA_PIXMAP_KEY))
                pixmap_item.setZValue(self.model.rowCount()-1-row)

    def eventFilter(self, widget, event):

        if event.type() == QtCore.QEvent.KeyPress:
            key = event.key()

            if key == QtCore.Qt.Key_Space:

                index = self.treeview.selectedIndexes()[0]
                item = index.model().itemFromIndex(index)

                if item.data(BaseWin.DATA_ITEM_TYPE) != BaseWin.PARENT_ITEM:
                    print 'Not a Parent item'
                    return True

                if not item.hasChildren():
                    print 'Has no children'
                    return True

                curr_sel = None
                num_rows = item.rowCount()

                if num_rows == 1:

                    child = item.child(0)

                    if child.checkState() == QtCore.Qt.CheckState.Checked:
                        child.setCheckState(QtCore.Qt.CheckState.Unchecked)
                    else:
                        child.setCheckState(QtCore.Qt.CheckState.Checked)

                elif num_rows > 1:

                    for row in range(num_rows):
                        if item.child(row).checkState() == QtCore.Qt.CheckState.Checked:
                            curr_sel = row
                            break

                    if curr_sel is None:
                        item.child(num_rows-1).setCheckState(QtCore.Qt.CheckState.Checked)
                        curr_sel = num_rows-1

                    new_sel = (curr_sel+1) % num_rows
                    
                    item.child(curr_sel).setCheckState(QtCore.Qt.CheckState.Unchecked)
                    item.child(new_sel).setCheckState(QtCore.Qt.CheckState.Checked)

                return True                

        return QtGui.QWidget.eventFilter(self, widget, event)

    def cleanModel(self, model):
        
        for item in self.scene.items():
            self.scene.removeItem(item)

        numRows = model.rowCount()
        for row in range(numRows):
            model.removeRow(0)

    def open_dir(self):
        
        selected_directory = QtGui.QFileDialog.getExistingDirectory()
        if selected_directory:
            self.load_assets(selected_directory)


    def load_assets(self, path):

        if not os.path.isdir(path):
            print('The directory dose not exist!')
            return

        self.cleanModel(self.model)

        dir_list = [p for p in os.listdir(path) if os.path.isdir(os.path.join(path, p))]

        for parent_index, dir_name in enumerate(sorted(dir_list)):

            dir_path = os.path.join(path, dir_name)            
            files_list = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and os.path.splitext(f)[-1] in self.valid_ext]

            parent_item = QtGui.QStandardItem(dir_name)
            parent_item.setData(BaseWin.PARENT_ITEM, BaseWin.DATA_ITEM_TYPE)
            parent_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
            #parent_item.setCheckable(True)

            self.model.insertRow(self.model.rowCount(), parent_item)

            for child_index, file in enumerate(files_list):

                if child_index == 0:
                    pixmap = QtGui.QPixmap(self.resource_path(file))
                    self.view.setSceneRect(QtCore.QRect(QtCore.QPoint(0,0), pixmap.size()))
                    pixmap_item = QtGui.QGraphicsPixmapItem(pixmap)

                file_name = os.path.basename(file)
                pixmap_item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(self.resource_path(file)))
                pixmap_item.setZValue(len(dir_list)-1-parent_index)
                self.layer_dict[file] = pixmap_item

                child_item = QtGui.QStandardItem(file_name)
                child_item.setData(BaseWin.CHILD_ITEM, BaseWin.DATA_ITEM_TYPE)

                
                child_item.setData(file, BaseWin.DATA_PIXMAP_KEY)

                
                child_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                child_item.setCheckable(True)

                if child_index == 0:

                    child_item.setCheckState(QtCore.Qt.CheckState.Checked)
                    self.scene.addItem(pixmap_item)

                parent_item.appendRow(child_item)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def item_changed(self, item):

        if item.data(BaseWin.DATA_ITEM_TYPE) == BaseWin.CHILD_ITEM:

            pixmap_item = self.layer_dict.get(item.data(BaseWin.DATA_PIXMAP_KEY))

            if item.checkState() == QtCore.Qt.CheckState.Checked:
                self.scene.addItem(pixmap_item)
                print 'Child item -> {} Checked'.format(item.text())

            else:
                self.scene.removeItem(pixmap_item)
                print 'Child item -> {} Uncecked'.format(item.text())

        elif item.data(BaseWin.DATA_ITEM_TYPE) == BaseWin.PARENT_ITEM:

            pass


def main():
    
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(petfactoryStyle.load_stylesheet())
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()