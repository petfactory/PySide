from PySide import QtGui, QtCore
import mario
import icons
import sys
import pprint
reload(mario)

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
        
        self.setGeometry(10, 10, 20, 20)
        self.setWindowTitle('Test RCC Win')

        vbox = QtGui.QVBoxLayout(self)

        self.tabWidget = QtGui.QTabWidget()
        vbox.addWidget(self.tabWidget)

        self.resourceDict = getPathsFromResource()
        #pprint.pprint(self.resourceDict)

        self.addWidgetFromDict(self.resourceDict, self.tabWidget)

    def addWidgetFromDict(self, resourceDict, tabWidget):

        keyList = resourceDict.keys()

        for key in keyList:

            tab = QtGui.QWidget()
            tabWidget.addTab(tab, key)  
            tabVbox = QtGui.QVBoxLayout(tab)
            model = QtGui.QStandardItemModel()
            listView = QtGui.QListView()

            listView.setAlternatingRowColors(True)
            listView.setModel(model)
            tabVbox.addWidget(listView)
            assetPathList = resourceDict.get(key)

            for assetPath in assetPathList:
                self.populateListView(assetPath, model)

            sm = listView.selectionModel()
            sm.selectionChanged.connect(self.listViewSelectionChanged)

    def listViewSelectionChanged(self, a):
    	print a

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