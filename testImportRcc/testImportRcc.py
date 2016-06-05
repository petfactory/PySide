from PySide import QtGui, QtCore
import mario
import icons
import sys, os
import pprint
reload(mario)

'''
>>> moduleNames = ['sys', 'os', 're', 'unittest'] 
>>> moduleNames
['sys', 'os', 're', 'unittest']
>>> modules = map(__import__, moduleNames)
'''


def recurseRcc(qDir, assetList):

    dirList = qDir.entryList(QtCore.QDir.Dirs)
    fileList = qDir.entryList(QtCore.QDir.Files)

    for file in fileList:
        #print fName
        fName =  '{}/{}'.format(qDir.path(), file)
        assetList.append(fName)
        
    for _dir in dirList:
        dName =  '{}/{}'.format(qDir.path(), _dir)
        #print dName
        d = QtCore.QDir(dName)
        recurseRcc(d, assetList)

def getPathsFromResource():

    rc = QtCore.QResource()

    # children() -> Returns a list of all resources in this directory,
    # if the resource represents a file the list will be empty.
    rootResourceList = rc.children()

    print rootResourceList

    retDict = {}
    for prefix in rootResourceList:
        #print prefix
        qDir = QtCore.QDir(':{}'.format(prefix))
        assetList = []
        retDict[prefix] = assetList
        recurseRcc(qDir, assetList)

    #pprint.pprint(retDict)
    return retDict



class TestWin(QtGui.QWidget):
    
    def __init__(self):
        super(TestWin, self).__init__()
        
        self.setGeometry(10, 10, 400, 600)
        self.setWindowTitle('Test RCC Win')

        self.listViewList = []


        vbox = QtGui.QVBoxLayout(self)

        self.tabWidget = QtGui.QTabWidget()
        vbox.addWidget(self.tabWidget)

        self.resourceDict = getPathsFromResource()
        #pprint.pprint(self.resourceDict)

        self.addWidgetFromDict(self.resourceDict, self.tabWidget)

        saveIconButton = QtGui.QPushButton('Save Icon')
        saveIconButton.clicked.connect(self.saveIconButtonClicked)
        vbox.addWidget(saveIconButton)


    def saveIconButtonClicked(self):
        index = self.tabWidget.currentIndex()
        listView = self.listViewList[index]
        selectionModel = listView.selectionModel()
        selectedQIndexes = selectionModel.selectedIndexes()

        if len(selectedQIndexes) < 0:
            return

        saveDir = QtGui.QFileDialog.getExistingDirectory(None, 'Select Directory to save icons')
        
        if saveDir:

            for qIndex in selectedQIndexes:

                baseName = os.path.basename(qIndex.data())
                savePath = os.path.join(saveDir, baseName)

                #print savePath
                if os.path.isfile(savePath):
                    print 'file exists'
                    return

                qIcon = qIndex.data(QtCore.Qt.DecorationRole)
                availSizeList =  qIcon.availableSizes()
                pixmap = qIcon.pixmap(availSizeList[0])
                pixmap.save(savePath)

        #return
        #fileName, selectedFilter = QtGui.QFileDialog.getSaveFileName(None, 'Save pixmap', baseName, 'PNG (*.png)')
        #if fileName:
        #    pass


    def addWidgetFromDict(self, resourceDict, tabWidget):

        keyList = resourceDict.keys()

        for key in keyList:

            tab = QtGui.QWidget()
            tabWidget.addTab(tab, key)  
            tabVbox = QtGui.QVBoxLayout(tab)
            model = QtGui.QStandardItemModel()
            listView = QtGui.QListView()
            listView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            self.listViewList.append(listView)
            listView.setAlternatingRowColors(True)
            listView.setModel(model)
            tabVbox.addWidget(listView)
            assetPathList = resourceDict.get(key)

            for assetPath in assetPathList:
                self.populateListView(assetPath, model)

            #sm = listView.selectionModel()
            #sm.selectionChanged.connect(self.listViewSelectionChanged)

    def listViewSelectionChanged(self, newSelection, oldSelection):
    	print newSelection.indexes()

    def populateListView(self, assetPath, model):

        item = QtGui.QStandardItem(assetPath)
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        item.setIcon(QtGui.QIcon(QtGui.QPixmap(assetPath)))
        model.appendRow(item)

def main():
     
    app = QtGui.QApplication(sys.argv)
    win = TestWin()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()