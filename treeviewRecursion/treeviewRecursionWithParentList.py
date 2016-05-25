import sys, os
from PySide import QtGui, QtCore
import xml.etree.ElementTree as ET


class NodeType(object):

    TRANSFORM = 0
    MESH = 1

class StandardItemModel(QtGui.QStandardItemModel):

    #checkboxToggled = QtCore.Signal(QtCore.QModelIndex)

    def __init__(self):
        self.c = Communicate()
        super(StandardItemModel, self).__init__()

    
class Communicate(QtCore.QObject):
    checkBoxToggled = QtCore.Signal(QtGui.QStandardItem, QtCore.Qt.CheckState)

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
                self.model().c.checkBoxToggled.emit(self, state)

        super(StandardItem, self).setData(value, role)
        
class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 250, 350)
        self.setWindowTitle('Icon')
        self.xmlPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nodes.xml')
        vbox = QtGui.QVBoxLayout(self)
        self.treeView = QtGui.QTreeView()
        self.meshItemList = []
        self.meshIconColor = (1, .8, 0, 1.0)
        self.transformIconColor = (.95, .95, .95, 1.0)

        #self.model = QtGui.QStandardItemModel()
        self.model = StandardItemModel()
        self.model.c.checkBoxToggled.connect(self.itemCheckBoxToggled)
        self.model.dataChanged.connect(self.dataChanged)
        vbox.addWidget(self.treeView)
        self.treeView.setModel(self.model)


        cleanupDagButton = QtGui.QPushButton('DAG Cleanup')
        cleanupDagButton.clicked.connect(self.cleanupDagButtonClicked)
        vbox.addWidget(cleanupDagButton)
        self.populateModelFromXml(self.xmlPath)
        self.treeView.expandAll()

        self.selectMeshStartingFromRoot()
        
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
        diffSet = nodeSet.symmetric_difference(keepSet)
        #diffSet = keepSet.difference(nodeSet)

        #self.selectMeshItem()
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



    def recurseTreeView(self, node, nodeSet, keepSet, parentList=[]):

        nodeSet.add(node)

        # if not visible in Maya, early return
        if node.checkState() == QtCore.Qt.CheckState.Unchecked:
                #print 'UNCHECKED REMOVE: {}'.format('->'.join([n.text() for n in parentList]))
                return

        # leaf item
        if not node.hasChildren():

            if node.data() == NodeType.MESH:
                [keepSet.add(n) for n in parentList]
                keepSet.add(node)
                #print '   {}'.format('->'.join([n.text() for n in parentList]))
            #else:
            #    print 'REMOVE: {}'.format('->'.join([n.text() for n in parentList]))
            #    pass

        # loop through the children
        else:
            numRows = node.rowCount()
            if numRows > 0:
                for row in range(numRows):
                    parentList.append(node)
                    self.recurseTreeView(node.child(row), nodeSet, keepSet, parentList)

        if len(parentList) > 0:
            parentList.pop()


    def selectMeshItem(self):

        for meshItem in self.meshItemList:
            self.treeView.selectionModel().select(self.model.indexFromItem(meshItem), QtGui.QItemSelectionModel.Select)
            #print self.model.indexFromItem(meshItem)
            #print meshItem

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
            qItem.setData(NodeType.TRANSFORM, QtCore.Qt.UserRole + 1)
            qItem.setIcon(self.createColorIcon(self.transformIconColor, 12, 12))

        elif xmlNode.tag == 'mesh':
            qItem.setData(NodeType.MESH, QtCore.Qt.UserRole + 1)
            qItem.setIcon(self.createColorIcon(self.meshIconColor, 12, 12))
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