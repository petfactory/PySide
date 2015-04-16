import sys
from PySide import QtGui, QtCore

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

            source_data = self.model().items[source_row]
            target_data = self.model().items[target_row]

            print('{0} was dropped on {1}'.format(source_data, target_data))

            self.model().items[source_row] = target_data
            self.model().items[target_row] = source_data
            self.update()
            
            event.accept()

        else:
            event.ignore()

class MyModel(QtCore.QAbstractTableModel):

    def __init__(self, items):
        '''Instantiates the model with a root item.'''
        super(MyModel, self).__init__()
        self.items = items

    # Mandatory method implementations ---------------------------

    # the following 3 methods (rowCount(...), columnCount(...), data(...)) must be implemented
    # default implementation of index(...), parent(...) are provided by the QAbstractTableModel class
    # Well behaved models will also implement headerData(...)
    def rowCount(self, index):
        '''Returns the number of children for the given QModelIndex.'''
        return len(self.items)

    def columnCount( self, index ):
        '''This model will have only one column.'''
        return 2

    def data( self, index, role ):
        '''Return the display name of the PyNode from the item at the given index.'''
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:

            row = index.row()
            col = index.column()

            if col == 0:
                return self.items[row][col]

            elif col == 1:
                return self.items[row][col]

    # optional method implementations ---------------------------

    def flags( self, index ):
        '''Valid items are selectable, editable, and drag and drop enabled. Invalid indices (open space in the view)
        are also drop enabled, so you can drop items onto the top level.
        '''
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled |  QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable


class MyTable(QtGui.QWidget):
    
    def __init__(self):
        super(MyTable, self).__init__()
                
        self.setGeometry(200, 200, 250, 350)
        self.setWindowTitle('Test')

        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)
        
        chars = 'ABCDEFGHIJK'
        data = [ [chars[i], i] for i in range(len(chars))]
        self.model = MyModel(data)

        tableview = MyTableView()
        vbox.addWidget(tableview)
        tableview.setModel(self.model)

        tableview.setDragEnabled(True)
        tableview.setAcceptDrops(True)
        tableview.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        tableview.setAlternatingRowColors(True)

        tableview.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        tableview.update()

        btn = QtGui.QPushButton("OK")
        vbox.addWidget(btn)

        self.show()

        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = MyTable()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

