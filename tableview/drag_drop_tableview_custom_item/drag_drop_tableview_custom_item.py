import sys
from PySide import QtGui, QtCore

class MyItem(object):

    def __init__(self, camera, start_time, end_time, notes):

        self._camera = camera
        self._start_time = start_time
        self._end_time = end_time
        self._notes = notes

    # display_name
    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, value):
        self._camera = value
  
    # start_time
    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    # end_time
    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        self._end_time = value

    # notes
    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = value


class MyDelegate(QtGui.QItemDelegate):
    
    def __init__(self, parent=None):
        super(MyDelegate, self).__init__(parent)
        
    def createEditor(self, parent, option, index):
        
        column = index.column()
        
        if column == 1 or column == 2: 
            spinbox = QtGui.QSpinBox(parent)
            spinbox.setRange(-9999,9999)
            spinbox.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            return spinbox
        
        else:
            return QtGui.QLineEdit(parent)


class MyTableView(QtGui.QTableView):

    def __init__(self, parent=None):
        QtGui.QTableView.__init__(self, parent=None)

        self.setSelectionMode(self.ExtendedSelection)
        self.setDragEnabled(True)
        self.acceptDrops()
        self.setDragDropMode(self.InternalMove)
        self.setDropIndicatorShown(True)

        self.current_source = None

    def dragEnterEvent(self, event):
        event.accept()

    def startDrag(self, dropActions):
        index = self.currentIndex()
        self.current_source = index
        drag = QtGui.QDrag(self)
        mimedata = QtCore.QMimeData()
        mimedata.setData('application/x-pynode-item-instance', 'pet')
        drag.setMimeData(mimedata)

        if drag.start(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            pass

    def dragMoveEvent(self, event):

        if event.mimeData().hasFormat('application/x-pynode-item-instance'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

        else:
            event.ignore()

    def dropEvent(self, event):
        
        if event.mimeData().hasFormat('application/x-pynode-item-instance'):

            target_index = self.indexAt(event.pos())

            source_row = self.current_source.row()
            target_row = target_index.row()

            source_data = self.model()._items[source_row]
            target_data = self.model()._items[target_row]

            print('{0} was dropped on {1}'.format(source_data, target_data))

            self.model()._items[source_row] = target_data
            self.model()._items[target_row] = source_data
            self.update()
            
            event.accept()

        else:
            event.ignore()

class MyModel(QtCore.QAbstractTableModel):

    def __init__(self, items):
        '''Instantiates the model with a root item.'''
        super(MyModel, self).__init__()
        self._items = items

    # Mandatory method implementations ---------------------------

    # the following 3 methods (rowCount(...), columnCount(...), data(...)) must be implemented
    # default implementation of index(...), parent(...) are provided by the QAbstractTableModel class
    # Well behaved models will also implement headerData(...)
    def rowCount(self, index=QtCore.QModelIndex()):
        '''Returns the number of children for the given QModelIndex.'''
        return len(self._items)

    def columnCount( self, index=QtCore.QModelIndex()):
        '''This model will have only one column.'''
        return 4

    def data( self, index, role= QtCore.Qt.DisplayRole):
        '''Return the display name of the PyNode from the item at the given index.'''
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:

            row = index.row()
            col = index.column()

            if col == 0:
                return self._items[row].camera
            elif col == 1:
                return str(self._items[row].start_time)
            elif col == 2:
                return str(self._items[row].end_time)
            elif col == 3:
                return self._items[row].notes


    # optional method implementations ---------------------------

    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if role == QtCore.Qt.EditRole:
            
            row = index.row()
            col = index.column()

            if col == 0:
                self._items[row].camera = value
            elif col == 1:
                self._items[row].start_time = value
            elif col == 2:
                self._items[row].end_time = value
            elif col == 3:
                self._items[row].notes = value

            self.dataChanged.emit(index, index)
            return True

        return False

    def flags( self, index ):
        '''Valid items are selectable, editable, and drag and drop enabled. Invalid indices (open space in the view)
        are also drop enabled, so you can drop items onto the top level.
        '''
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled |  QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        ''' this will insert empty rows'''

        self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)

        for i in range(rows):
            self._items.insert(position, MyItem('', 0, 0, ''))

        self.endInsertRows()

        return True

    def append_item(self, item, parent=QtCore.QModelIndex()):
        ''' this will append an item'''

        position = self.rowCount()
        self.beginInsertRows(QtCore.QModelIndex(), position, position)
        self._items.insert(position, item)
        self.endInsertRows()
        return True


class MyTable(QtGui.QWidget):
    
    def __init__(self):
        super(MyTable, self).__init__()
                
        self.setGeometry(200, 200, 250, 350)
        self.setWindowTitle('Test')

        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)
        
        item1 = MyItem('camera1', 10, 20, 'notes 1')
        item2 = MyItem('camera2', 20, 50, 'notes 2')
        item3 = MyItem('camera3', 45, 110, 'notes 3')
        data = [item1, item2, item3]

        self.model = MyModel(data)

        tableview = MyTableView()
        tableview.setModel(self.model)
        tableview.setDragEnabled(True)
        tableview.setAcceptDrops(True)
        tableview.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        tableview.setAlternatingRowColors(True)
        tableview.setItemDelegate(MyDelegate(tableview))

        tableview.update()
        vbox.addWidget(tableview)

        btn = QtGui.QPushButton("OK")
        btn.clicked.connect(self.add_item)
        vbox.addWidget(btn)

        self.show()

    def add_item(self):
        item = MyItem('new camera', 45, 110, 'bal bala asa')
        self.model.append_item(item)


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = MyTable()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

