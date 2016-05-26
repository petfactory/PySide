import sys, os
from PySide import QtGui, QtCore
import xml.etree.ElementTree as ET
import style

class StandardItemModel(QtGui.QStandardItemModel):

    checkBoxToggled = QtCore.Signal(QtGui.QStandardItem, QtCore.Qt.CheckState)

    def __init__(self, *args, **kwargs):
        super(StandardItemModel, self).__init__(*args, **kwargs)

    
class StandardItem(QtGui.QStandardItem):

    TRANSFORM_NODE = 0
    MESH_NODE = 1

    NODETYPE_ROLE = QtCore.Qt.UserRole + 1

    def __init__(self, *args, **kwargs):
        super(StandardItem, self).__init__(*args, **kwargs)

    def setData(self, value, role=QtCore.Qt.UserRole+1):

        #enum QtCore.Qt.ItemDataRole
        if role == QtCore.Qt.EditRole:
            pass

        elif role == QtCore.Qt.CheckStateRole:
            if self.model() is not None:
                state = QtCore.Qt.CheckState.Unchecked if value is 0 else QtCore.Qt.CheckState.Checked
                self.model().checkBoxToggled.emit(self, state)

        super(StandardItem, self).setData(value, role)
        
class Outliner(QtGui.QWidget):

    def __init__(self):
        super(Outliner, self).__init__()
        
        self.setGeometry(30, 55, 350, 450)
        self.setWindowTitle('Outliner')
        self.xmlPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nodes.xml')
        vbox = QtGui.QVBoxLayout(self)
        self.treeView = QtGui.QTreeView()
        self.meshItemList = []
        self.meshIconColor = (1, .8, 0, 1.0)
        self.transformIconColor = (.95, .95, .95, 1.0)
        self.shiftModifier = False

        self.model = StandardItemModel()
        self.model.checkBoxToggled.connect(self.itemCheckBoxToggled)
        
        self.model.dataChanged.connect(self.dataChanged)
        vbox.addWidget(self.treeView)
        self.treeView.setModel(self.model)
        self.treeView.installEventFilter(self)
        self.treeView.expanded.connect(self.treeViewExpanded)
        self.treeView.collapsed.connect(self.treeViewCollapsed)

        self.populateModelFromXml(self.xmlPath)
        
        #self.treeView.expandAll()
        #self.treeView.setExpanded(self.model.indexFromItem(self.model.item(0,0)), True)
        #self.selectMeshStartingFromRoot()

        rootIndex = self.model.indexFromItem(self.model.item(0,0))
        self.treeView.selectionModel().select(rootIndex, QtGui.QItemSelectionModel.Select)


    def recursiveExpand(self, view, index, expand):
        
        view.setExpanded(index, expand)
        model = view.model()
        numRows = model.rowCount(index)
        for row in range(numRows):
            child = model.index(row, 0, index)
            self.recursiveExpand(view, child, expand)


    def treeViewCollapsed(self, index):
        if self.shiftModifier:
            self.recursiveExpand(self.treeView, index, False)

    def treeViewExpanded(self, index):
        if self.shiftModifier:
            self.recursiveExpand(self.treeView, index, True)


    def eventFilter(self, obj, event):

        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Shift:
                self.shiftModifier = True

        elif event.type() == QtCore.QEvent.KeyRelease:
            if event.key() == QtCore.Qt.Key_Shift:
                self.shiftModifier = False

        # standard event processing
        return QtCore.QObject.eventFilter(self, obj, event)


    def selectMeshStartingFromRoot(self):
        rootItem = self.model.item(0,0)
        nodeSet = set()
        keepSet = set()
        self.recurseTreeView(rootItem, nodeSet, keepSet)
        self.selectMeshItem()


    def itemCheckBoxToggled(self, item, checkState):
        model = item.model()
        model.blockSignals(True)
        self.recursiveCheckState(item, checkState)
        model.blockSignals(False)
        model.layoutChanged.emit()


    def dataChanged(self, topLeft, bottomRigh):
        print topLeft

    def recursiveCheckState(self, item, checkState):

        numRows = item.rowCount()
        if numRows > 0:
            for row in range(numRows):
                child = item.child(row)
                child.setEnabled(checkState == QtCore.Qt.CheckState.Checked)
                child.setCheckState(checkState)
                self.recursiveCheckState(child, checkState)


    def selectMeshItem(self):

        for meshItem in self.meshItemList:
            self.treeView.selectionModel().select(self.model.indexFromItem(meshItem), QtGui.QItemSelectionModel.Select)

    def populateModelFromXml(self, filePath):

        tree = ET.parse(filePath)
        root = tree.getroot()
        self.recurseXmlNode(root, None, self.model.invisibleRootItem())


    def recurseXmlNode(self, xmlNode, xmlParent, qItemParent):

        qItem = StandardItem(xmlNode.get('name'))
        qItem.setCheckable(True)
        qItem.setCheckState(QtCore.Qt.CheckState.Checked)

        if xmlNode.tag == 'node':
            qItem.setData(StandardItem.TRANSFORM_NODE, StandardItem.NODETYPE_ROLE)
            qItem.setIcon(QtGui.QIcon('transform.png'))

        elif xmlNode.tag == 'mesh':
            qItem.setData(StandardItem.MESH_NODE, StandardItem.NODETYPE_ROLE)
            qItem.setIcon(QtGui.QIcon('mesh.png'))
            
    
        qItemParent.appendRow(qItem)

        for child in list(xmlNode):
            self.recurseXmlNode(child, xmlParent, qItem)


'''    
def main():
    
    app = QtGui.QApplication(sys.argv)

    style.compile_rc()
    app.setStyleSheet(style.loadStyleSheet())

    win = Outliner()
    win.show() 
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
'''