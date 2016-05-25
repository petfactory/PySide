import sys, os
from PySide import QtGui, QtCore
import xml.etree.ElementTree as ET

class NodeType(object):

    TRANSFORM = 0
    MESH = 1


class UserRole(object):

    NODETYPE = QtCore.Qt.UserRole + 1


class StandardItemModel(QtGui.QStandardItemModel):

    checkBoxToggled = QtCore.Signal(QtGui.QStandardItem, QtCore.Qt.CheckState)

    def __init__(self):
        super(StandardItemModel, self).__init__()

    
class StandardItem(QtGui.QStandardItem):

    def __init__(self, text):
        super(StandardItem, self).__init__(text)

    def setData(self, value, role=QtCore.Qt.UserRole+1):

        #enum Qt::ItemDataRole
        if role == QtCore.Qt.EditRole:
            pass

        elif role == QtCore.Qt.CheckStateRole:
            if self.model() is not None:
                state = QtCore.Qt.CheckState.Unchecked if value is 0 else QtCore.Qt.CheckState.Checked
                self.model().checkBoxToggled.emit(self, state)

        super(StandardItem, self).setData(value, role)
        
class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(50, 50, 350, 450)
        #self.setWindowTitle('')
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


        cleanupDagButton = QtGui.QPushButton('DAG Cleanup')
        cleanupDagButton.clicked.connect(self.cleanupDagButtonClicked)
        vbox.addWidget(cleanupDagButton)
        self.populateModelFromXml(self.xmlPath)
        
        #self.treeView.expandAll()
        #self.treeView.setExpanded(self.model.indexFromItem(self.model.item(0,0)), True)
        #self.selectMeshStartingFromRoot()

        rootIndex = self.model.indexFromItem(self.model.item(0,0))
        self.treeView.selectionModel().select(rootIndex, QtGui.QItemSelectionModel.Select)

        self.setStyleSheet(
        '''QWidget {

            color: #e4e4e4;
            background-color: #282828;
            selection-background-color:#3d8ec9;
            selection-color: black;
            background-clip: border;
            border-image: none;
            outline: 0;
        }'''
        )

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


    def eventFilter(self, widget, event):

        if (event.type() == QtCore.QEvent.KeyPress and widget is self.treeView):
            key = event.key()
            if key == QtCore.Qt.Key_Shift:
                self.shiftModifier = True
            return False

        elif (event.type() == QtCore.QEvent.KeyRelease and widget is self.treeView):
            key = event.key()
            if key == QtCore.Qt.Key_Shift:
                self.shiftModifier = False
            return False


        return QtGui.QWidget.eventFilter(self, widget, event)


    def selectMeshStartingFromRoot(self):
        rootItem = self.model.item(0,0)
        nodeSet = set()
        keepSet = set()
        self.recurseTreeView(rootItem, nodeSet, keepSet)
        self.selectMeshItem()

    def cleanupDagButtonClicked(self):

        self.meshItemList = []
        self.treeView.selectionModel().clear()
        rootItem = self.model.item(0,0)
        nodeSet = set()
        keepSet = set()

        self.recurseTreeView(rootItem, nodeSet, keepSet)
        diffSet = nodeSet.difference(keepSet)

        for node in diffSet:
            self.treeView.selectionModel().select(self.model.indexFromItem(node), QtGui.QItemSelectionModel.Select)

    def itemCheckBoxToggled(self, item, state):

        if state == QtCore.Qt.CheckState.Unchecked:
            self.setNodeEnabledState(item, False)

        if state == QtCore.Qt.CheckState.Checked:
            self.setNodeEnabledState(item, True)

    def dataChanged(self, topLeft, bottomRigh):
        pass

    def setNodeEnabledState(self, node, state):

        numRows = node.rowCount()

        if numRows > 0:
            for row in range(numRows):
                child = node.child(row)
                child.setEnabled(state)
                if state:
                    child.setCheckState(QtCore.Qt.CheckState.Checked)
                else:
                    child.setCheckState(QtCore.Qt.CheckState.Unchecked)

                self.setNodeEnabledState(child, state)



    def recurseTreeView(self, node, nodeSet, keepSet):

        nodeSet.add(node)

        # if not visible in Maya, early return
        if node.checkState() == QtCore.Qt.CheckState.Unchecked:
                return

        # leaf item
        if not node.hasChildren():

            if node.data() == NodeType.MESH:

                while True:

                    if node in keepSet:
                        break

                    keepSet.add(node)
                    parent = node.parent()

                    if parent:
                        node = parent
                    else:
                        break

        # loop through the children
        else:
            numRows = node.rowCount()
            if numRows > 0:
                for row in range(numRows):
                    self.recurseTreeView(node.child(row), nodeSet, keepSet)

    def selectMeshItem(self):

        for meshItem in self.meshItemList:
            self.treeView.selectionModel().select(self.model.indexFromItem(meshItem), QtGui.QItemSelectionModel.Select)

    def populateModelFromXml(self, filePath):

        tree = ET.parse(filePath)
        root = tree.getroot()
        self.recurseXmlNode(root, None, self.model.invisibleRootItem())

    def createColorIcon(self, color, width, height):
        qColor = QtGui.QColor()
        qColor.setRgbF(*color)            
        pixmap = QtGui.QPixmap(width, height)
        pixmap.fill(QtGui.QColor(qColor))
        icon = QtGui.QIcon(pixmap)
        return icon

    def recurseXmlNode(self, xmlNode, xmlParent, qItemParent):

        qItem = StandardItem(xmlNode.get('name'))
        qItem.setCheckable(True)
        qItem.setCheckState(QtCore.Qt.CheckState.Checked)

        if xmlNode.tag == 'node':
            qItem.setData(NodeType.TRANSFORM, UserRole.NODETYPE)
            qItem.setIcon(QtGui.QIcon('transform.png'))
            #qItem.setIcon(self.createColorIcon(self.transformIconColor, 12, 12))

        elif xmlNode.tag == 'mesh':
            qItem.setData(NodeType.MESH, UserRole.NODETYPE)
            qItem.setIcon(QtGui.QIcon('mesh.png'))
            #qItem.setIcon(self.createColorIcon(self.meshIconColor, 12, 12))
        else:
            qItem.setIcon(self.createColorIcon((0,0,0,1), 12, 12))

    
        qItemParent.appendRow(qItem)


        for child in list(xmlNode):
            self.recurseXmlNode(child, xmlParent, qItem)


       
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show() 
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()