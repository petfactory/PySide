from PySide import QtGui, QtCore
import sys, os
import pprint
import importlib


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


class TestWin(QtGui.QMainWindow):
    
    def __init__(self):
        super(TestWin, self).__init__()
        
        self.setGeometry(10, 10, 400, 600)
        self.setWindowTitle('Test RCC Win')

        self.listViewList = []

        mainWidget = QtGui.QWidget()
        self.setCentralWidget(mainWidget)
        vbox = QtGui.QVBoxLayout(mainWidget)

        openResourceAction = QtGui.QAction('Open', self)
        openResourceAction.setShortcut('Ctrl+O')
        openResourceAction.triggered.connect(self.importResourceTriggered)

        saveIconAction = QtGui.QAction('Save', self)
        saveIconAction.setShortcut('Ctrl+S')
        saveIconAction.triggered.connect(self.saveIconTriggered)
        
        self.toolbar = self.addToolBar('fileToolbar')
        self.toolbar.addAction(openResourceAction)
        self.toolbar.addAction(saveIconAction)

        self.tabWidget = QtGui.QTabWidget()
        vbox.addWidget(self.tabWidget)


    def importResourceTriggered(self):
        fileName, selectedFilter = QtGui.QFileDialog.getOpenFileName(None, 'Import Resource', None, 'Python (*.py)')

        if fileName:

            baseName = os.path.basename(fileName)
            moduleName, ext = os.path.splitext(baseName)
            importlib.import_module(moduleName)

            self.resourceDict = self.getPathsFromResource()
            #pprint.pprint(self.resourceDict)

            self.addWidgetFromDict(self.resourceDict, self.tabWidget)

    def saveIconTriggered(self):

        index = self.tabWidget.currentIndex()
        if index == -1:
            print 'Please open a resource and select an icon to save'
            return

        listView = self.listViewList[index]
        selectionModel = listView.selectionModel()
        selectedQIndexes = selectionModel.selectedIndexes()

        if len(selectedQIndexes) == 0:
            print 'Please slect an icon'
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

    def getPathsFromResource(self):

        rc = QtCore.QResource()

        # children() -> Returns a list of all resources in this directory,
        # if the resource represents a file the list will be empty.
        rootResourceList = rc.children()

        #print rootResourceList

        retDict = {}
        for prefix in rootResourceList:

            #print prefix
            qDir = QtCore.QDir(':{}'.format(prefix))
            assetList = []
            retDict[prefix] = assetList
            recurseRcc(qDir, assetList)

        #pprint.pprint(retDict)
        return retDict


    def addWidgetFromDict(self, resourceDict, tabWidget):

        keyList = resourceDict.keys()

        currentTabNaneList = []
        for index in range(self.tabWidget.count()):
            currentTabNaneList.append(self.tabWidget.tabText(index))

        for key in keyList:

            if key in currentTabNaneList:
                print 'tab exists, skipping...'
                continue

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