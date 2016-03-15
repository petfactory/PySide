#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
TODO:
reorder parent layers, adjust z_index
skip the layer dict and add directly to the layer userData
'''
import sys, os
from PySide import QtGui, QtCore
import petfactoryStyle

        
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


    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(5, 50, 600, 500)
        self.setWindowTitle('Test')

        self.layer_dict = {}
        self.valid_ext = ['.png', '.jpg', '.jpeg']

        open_action = QtGui.QAction(QtGui.QIcon(self.resource_path('open_dir.png')), '&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open directory')
        open_action.triggered.connect(self.open_dir)

        self.toolbar = self.addToolBar('Open')
        self.toolbar.addAction(open_action)


        self.scene = QtGui.QGraphicsScene()
    
        self.model = QtGui.QStandardItemModel()

        ''' Set the item prototype
        self.model.setItemPrototype(ParentItem()) '''

        self.model.itemChanged.connect(self.item_changed)

        #self.treeview = QtGui.QTreeView()
        self.treeview = MyTreeView()
        
        self.treeview.setDragEnabled(True)
        self.treeview.setDragDropMode(QtGui.QAbstractItemView.InternalMove)

        self.treeview.setHeaderHidden(True)
        self.treeview.setModel(self.model)
        self.treeview.setAlternatingRowColors(True)
        self.model.setHorizontalHeaderLabels(['Layers'])

        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setSceneRect(0,0,800,600)        

        splitter = QtGui.QSplitter(self)
        self.setCentralWidget(splitter)

        left_frame = QtGui.QFrame()
        left_frame.setMinimumWidth(200)
        left_vbox = QtGui.QVBoxLayout(left_frame)
        left_vbox.addWidget(self.treeview)

        #layer_order_hbox = QtGui.QHBoxLayout()
        #move_layer_up_button = QtGui.QPushButton()
        #move_layer_down_button = QtGui.QPushButton()

        #layer_order_hbox.addWidget(move_layer_up_button)
        #move_layer_up_button.setIcon(QtGui.QIcon(self.resource_path('up_arrow.png')))
        #move_layer_up_button.setFixedHeight(26)

        #layer_order_hbox.addWidget(move_layer_down_button)
        #move_layer_down_button.setIcon(QtGui.QIcon(self.resource_path('down_arrow.png')))
        #move_layer_down_button.setFixedHeight(26)

        #left_vbox.addLayout(layer_order_hbox)

        splitter.addWidget(left_frame)
        
        right_frame = QtGui.QFrame()
        right_vbox = QtGui.QVBoxLayout(right_frame)
        right_vbox.addWidget(self.view)
        splitter.addWidget(right_frame)


        splitter.setSizes([100, 600])

        self.load_assets(self.resource_path('./assets'))

        self.treeview.installEventFilter(self)

        self.model.rowsInserted.connect(self.rows_inserted)

    def rows_inserted(self, *args):
        print 'Rows inserted'

        num_rows = self.model.invisibleRootItem().rowCount()

        for row in range(num_rows):
            print self.model.item(row)

    def eventFilter(self, widget, event):

        if event.type() == QtCore.QEvent.KeyPress:
            key = event.key()

            if key == QtCore.Qt.Key_Space:

                index = self.treeview.selectedIndexes()[0]
                item = index.model().itemFromIndex(index)

                #if not isinstance(item, ParentItem):
                #if not item.type() == QtGui.QStandardItem.UserType+1:
                if item.data(QtCore.Qt.UserRole) != BaseWin.PARENT_ITEM:
                    print 'Not a Parent item!'
                    return True

                if not item.hasChildren():
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
        self.layer_dict = {}

        dir_list = [p for p in os.listdir(path) if os.path.isdir(os.path.join(path, p))]

        for index, dir in enumerate(sorted(dir_list)):

            sub_layer_dict = {}
            self.layer_dict[dir] = sub_layer_dict

            dir_path = os.path.join(path, dir)
            
            files_list = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and os.path.splitext(f)[-1] in self.valid_ext]

            for file in files_list:
                base = os.path.basename(file)
                sub_layer_dict[base] = {    'path':QtGui.QGraphicsPixmapItem(QtGui.QPixmap(self.resource_path(file))),
                                            'z_value': index
                                        }

        key_list = self.layer_dict.keys()

        #for layer_name, child_list in self.layer_dict.iteritems():
        for key in sorted(key_list):
            
            parent_item = ParentItem(key)
            parent_item.setData(BaseWin.PARENT_ITEM, QtCore.Qt.UserRole)
            parent_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
            parent_item.setCheckable(True)

            self.model.setItem(self.model.rowCount(), 0, parent_item)

            child_list = self.layer_dict.get(key)

            for index, child in enumerate(child_list):

                child_item = ChildItem(child)
                child_item.setData( BaseWin.CHILD_ITEM, QtCore.Qt.UserRole)
                child_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                child_item.setCheckable(True)

                if index == 0:

                    child_item.setCheckState(QtCore.Qt.CheckState.Checked)
                    pixmap_item =  child_list[child].get('path')
                    z_value = child_list[child].get('z_value')
                    pixmap_item.setZValue(z_value)
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

        contents = self.layer_dict.get(item.text())

        if contents is None:
            
            sub_layer_dict = self.layer_dict.get(item.parent().text())

            if sub_layer_dict is None:
                return

            info_dict = sub_layer_dict.get(item.text())

            pixmap_item = info_dict.get('path')
            z_value = info_dict.get('z_value')

            if pixmap_item is None:
                return

            if item.checkState() == QtCore.Qt.CheckState.Checked:
                pixmap_item.setZValue(z_value)
                self.scene.addItem(pixmap_item)
            else:
                self.scene.removeItem(pixmap_item)

def main():
    
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(petfactoryStyle.load_stylesheet())
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()