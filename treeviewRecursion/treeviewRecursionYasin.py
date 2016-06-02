import sys, os
from PySide import QtGui, QtCore
import xml.etree.ElementTree as ET
import style

class StandardItemModel(QtGui.QStandardItemModel):
    """docstring for Standard"""
    def __init__(self, *args, **kwargs):
        super(StandardItemModel, self).__init__(*args, **kwargs)


    def mimeTypes(self):
        return ['application/x-tech.artists.org']

    def mimeData(self, indices):

        mimeData = QtCore.QMimeData()
        encodedData = QtCore.QByteArray()
        stream = QtCore.QDataStream(encodedData, QtCore.QIODevice.WriteOnly)

        for index in indices:
            if not index.isValid():
                continue
            node = index.internalPointer()
                
            variant = QtCore.QVariant(node)
                
            # add all the items into the stream
            stream << variant
                
        print 'Encoding drag with: ", "application/x-tech.artists.org'
        mimeData.setData('application/x-tech.artists.org', encodedData)
        return mimeData

    def dropMimeData(self, data, action, row, column, parent):

        if action == QtCore.Qt.CopyAction:
            print "Copying"
        elif action == QtCore.Qt.MoveAction:
            print "Moving"
        print "Param data:", data
        print "Param row:",  row
        print "Param column:", column
        print "Param parent:", parent

        # Where are we inserting?
        beginRow = 0
        if row != -1:
            print "ROW IS NOT -1, meaning inserting inbetween, above or below an existing node"
            beginRow = row
        elif parent.isValid():
            print "PARENT IS VALID, inserting ONTO something since row was not -1, beginRow becomes 0 because we want to insert it at the begining of this parents children"
            beginRow = 0
        else:
            print "PARENT IS INVALID, inserting to root, can change to 0 if you want it to appear at the top"
            beginRow = self.rowCount(QtCore.QModelIndex())

        # create a read only stream to read back packed data from our QMimeData
        encodedData = data.data("application/x-tech.artists.org")

        stream = QtCore.QDataStream(encodedData, QtCore.QIODevice.ReadOnly)

        '''
        # decode all our data back into dropList
        dropList = []
        numDrop = 0

        while not stream.atEnd():
            variant = QtCore.QVariant()
            stream >> variant # extract
            node = variant.toPyObject()
            
            # add the python object that was wrapped up by a QVariant back in our mimeData method
            dropList.append( node ) 

            # number of items to insert later
            numDrop += 1

        '''
        print "INSERTING AT", beginRow, "WITH", numDrop, "AMOUNT OF ITEMS ON PARENT:", parent.internalPointer()
        
        # This will insert new items, so you have to either update the values after the insertion or write your own method to receive our decoded dropList objects.
        self.insertRows(beginRow, numDrop, parent) 
        
        for drop in dropList:
            # If you don't have your own insertion method and stick with the insertRows above, this is where you would update the values using our dropList.
            pass
        
class Outliner(QtGui.QWidget):

    def __init__(self):
        super(Outliner, self).__init__()
        
        self.setGeometry(30, 55, 350, 450)
        self.setWindowTitle('Outliner')
        self.xmlPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nodes.xml')
        vbox = QtGui.QVBoxLayout(self)

        self.meshItemList = []
        self.meshIconColor = (1, .8, 0, 1.0)
        self.transformIconColor = (.95, .95, .95, 1.0)
        self.shiftModifier = False

        #self.model = QtGui.QStandardItemModel()
        self.model = StandardItemModel()
                
        self.treeView = QtGui.QTreeView()
        
        vbox.addWidget(self.treeView)

        self.treeView.setModel(self.model)        
        self.treeView.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        #self.treeView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)


        self.populateModelFromXml(self.xmlPath)
        
        #rootIndex = self.model.indexFromItem(self.model.item(0,0))
        #self.treeView.selectionModel().select(rootIndex, QtGui.QItemSelectionModel.Select)

    def populateModelFromXml(self, filePath):

        tree = ET.parse(filePath)
        root = tree.getroot()
        self.recurseXmlNode(root, None, self.model.invisibleRootItem())

    def recurseXmlNode(self, xmlNode, xmlParent, qItemParent):

        qItem = QtGui.QStandardItem(xmlNode.get('name'))
        qItem.setCheckable(True)
        qItem.setCheckState(QtCore.Qt.CheckState.Checked)

        #if xmlNode.tag == 'node':
        #    qItem.setData(StandardItem.TRANSFORM_NODE, StandardItem.NODETYPE_ROLE)
        #    qItem.setIcon(QtGui.QIcon('transform.png'))

        #elif xmlNode.tag == 'mesh':
        #    qItem.setData(StandardItem.MESH_NODE, StandardItem.NODETYPE_ROLE)
        #    qItem.setIcon(QtGui.QIcon('mesh.png'))
            
        #else:
        #    qItem.setIcon(self.createColorIcon((0,0,0,1), 12, 12))

    
        qItemParent.appendRow(qItem)


        for child in list(xmlNode):
            self.recurseXmlNode(child, xmlParent, qItem)


       
def main():
    
    app = QtGui.QApplication(sys.argv)

    #style.compile_rc()
    app.setStyleSheet(style.loadStyleSheet())

    win = Outliner()
    win.show() 
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

