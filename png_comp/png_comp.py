#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys, os
from PySide import QtGui, QtCore
import petfactoryStyle

        
class ParentItem(QtGui.QStandardItem):
    pass

class ChildItem(QtGui.QStandardItem):
    pass


#class BaseWin(QtGui.QWidget):
class BaseWin(QtGui.QMainWindow):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(5, 50, 600, 500)
        self.setWindowTitle('Test')

        self.layer_dict = {}

        '''
        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        '''

        open_action = QtGui.QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open directory')
        open_action.triggered.connect(self.open_dir)

        self.toolbar = self.addToolBar('Open')
        self.toolbar.addAction(open_action)


        self.scene = QtGui.QGraphicsScene()
    
        self.model = QtGui.QStandardItemModel()
        self.model.itemChanged.connect(self.item_changed)

        self.treeview = QtGui.QTreeView()
        self.treeview.setModel(self.model)
        self.model.setHorizontalHeaderLabels(['Layers'])

        view = QtGui.QGraphicsView(self.scene)
        view.setSceneRect(0,0,800,600)        

        splitter = QtGui.QSplitter(self)
        self.setCentralWidget(splitter)

        splitter.addWidget(self.treeview)
        splitter.addWidget(view)

        self.load_assets(self.resource_path('./assets'))

        self.treeview.installEventFilter(self)


    def eventFilter(self, widget, event):

        if event.type() == QtCore.QEvent.KeyPress:
            key = event.key()

            if key == QtCore.Qt.Key_Space:
                print('space')
                index = self.treeview.selectedIndexes()[0]

                item = self.model.itemFromIndex(index)

                if not isinstance(item, ParentItem):
                    return True

                if not item.hasChildren():
                    return

                curr_sel = None
                num_rows = item.rowCount()

                if num_rows < 2:
                    return True

                for row in range(num_rows):
                    if item.child(row).checkState() == QtCore.Qt.CheckState.Checked:
                        curr_sel = row
                        break

                new_sel = (curr_sel+1) % num_rows
                
                item.child(curr_sel).setCheckState(QtCore.Qt.CheckState.Unchecked)
                item.child(new_sel).setCheckState(QtCore.Qt.CheckState.Checked)

                return True

            else:
                if key == QtCore.Qt.Key_Return:
                    self.edit.setText('return')
                elif key == QtCore.Qt.Key_Enter:
                    self.edit.setText('enter')
                return False
                

        return QtGui.QWidget.eventFilter(self, widget, event)


    def open_dir(self):
        selected_directory = QtGui.QFileDialog.getExistingDirectory()
        if selected_directory:
            self.load_assets(selected_directory)


    def load_assets(self, path):
        if not os.path.isdir(path):
            print('The directory dose not exist!')
            return

        dir_list = [p for p in os.listdir(path) if os.path.isdir(os.path.join(path, p))]
        z_value = 0
        #print dir_list

        for dir in dir_list:

            sub_layer_dict = {}
            self.layer_dict[dir] = sub_layer_dict

            dir_path = os.path.join(path, dir)
            #print dir_path
            files_list = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
            #print files_list

            for file in files_list:
                base = os.path.basename(file)
                z_value += 1
                sub_layer_dict[base] = {    'path':QtGui.QGraphicsPixmapItem(QtGui.QPixmap(self.resource_path(file))),
                                            'z_value': z_value
                                        }


        for layer_name, child_list in self.layer_dict.iteritems():
            
            parent_item = ParentItem(layer_name)
            parent_item.setCheckable(True)
            self.model.setItem(self.model.rowCount(), 0, parent_item)

            for index, child in enumerate(child_list):
                child_item = ChildItem(child)
                child_item.setCheckable(True)
                if index == 0:
                    child_item.setCheckState(QtCore.Qt.CheckState.Checked)

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

            #z_value = item.row()
            #print z_value

            if item.checkState() == QtCore.Qt.CheckState.Checked:
                pixmap_item.setZValue(z_value)
                self.scene.addItem(pixmap_item)
            else:
                self.scene.removeItem(pixmap_item)


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
    #app.setStyleSheet(petfactoryStyle.load_stylesheet())
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()