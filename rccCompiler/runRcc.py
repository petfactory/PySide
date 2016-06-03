import sys, os
import subprocess
from PySide import QtGui, QtCore
import xml.etree.ElementTree as ET
import xml.dom.minidom


'''
Paths in Qt resource files are artificial constructs, therefore you need to explicitly
define your path structure by hand (as opposed to xml structure):
They are "flat", they do not use the hierarchy of the xml like nodes.
'''

def recurseFlatDir(dir, xmlParent, parentList=None):

    if parentList is None:
        parentList = []
    
    contentList = os.listdir(dir)
    
    for content in contentList:

        contentPath = os.path.join(dir, content)

        if os.path.isdir(contentPath):
            parentList.append(content)
            recurseFlatDir(contentPath, xmlParent, parentList)

        else:
            _, ext = os.path.splitext(contentPath)
            if ext in ['.png', '.jpg', '.jpeg']:
                
                if len(parentList) > 0:
                    content = '{}/{}'.format('/'.join(parentList), content)
                
                xmlNode = ET.Element('file')
                xmlNode.text = content
                xmlParent.append(xmlNode)

    if len(parentList) > 0:
        parentList.pop()



def buildQrc(assetsDir, qrcFileName):

    if not os.path.isdir(assetsDir):
        print 'The assets directory is not valid'
        return

    qrcFilePath = os.path.join(assetsDir, '{}.qrc'.format(qrcFileName))

    if os.path.isfile(qrcFilePath):
        print 'The file; {} exists, overwrite...'

    rccElem = ET.Element('RCC')
    qresourceElem = ET.Element('qresource')
    rccElem.append(qresourceElem)

    recurseFlatDir(assetsDir, qresourceElem)
    
    # use ElementTree to build the xml like structure
    # use minidom to prettyfy it
    xmlString = ET.tostring(rccElem)
    miniDomXml = xml.dom.minidom.parseString(xmlString)
    prettyXML = miniDomXml.toprettyxml(indent='    ')

    # use ugly hack to remove the description
    skipfirstline = '\n'.join(prettyXML.split('\n')[1:]) 
    #print sansfirstline

    if qrcFilePath:
        f = open(qrcFilePath,'w')
        f.write(skipfirstline)
        f.close()
        

def compileResourceToPython(qrcFilePath, outFilePath):

    dirPath = os.path.dirname(__file__)
    rccPath = os.path.join(dirPath, 'pyside-rcc')

    subprocess.call([rccPath, qrcFilePath, '-o', outFilePath])


class TestWin(QtGui.QWidget):
    
    def __init__(self):
        super(TestWin, self).__init__()
        
        self.setGeometry(10, 50, 500, 400)
        self.setWindowTitle('Test RCC Win')

        self.qrcFileName = 'icons'
        self.qrcFilePath = '{}.qrc'.format(self.qrcFileName)

        self.compiledPythonFileName = 'icons'
        self.compiledPythonFilePath = '{}.py'.format(self.compiledPythonFileName)

        vbox = QtGui.QVBoxLayout(self)
        splitter = QtGui.QSplitter()
        vbox.addWidget(splitter)        

        self.model = QtGui.QStandardItemModel()
        self.listView = QtGui.QListView()
        self.listView.setAlternatingRowColors(True)
        self.listView.setModel(self.model)
        splitter.addWidget(self.listView)

        self.textEdit = QtGui.QTextEdit()
        splitter.addWidget(self.textEdit)

        openAssetButton = QtGui.QPushButton('Open Asset Dir')
        openAssetButton.clicked.connect(self.openAssetButtonClicked)
        vbox.addWidget(openAssetButton)

    def openAssetButtonClicked(self):

        assetDir = QtGui.QFileDialog.getExistingDirectory(None, 'Open Assets', None, QtGui.QFileDialog.ShowDirsOnly)

        if assetDir:
            
            buildQrc(assetDir, self.qrcFileName)

            qrcFilePath = os.path.join(assetDir, self.qrcFilePath)
            self.populateTextEditFromQrc(qrcFilePath, self.textEdit)

            fileName, selectedFilter = QtGui.QFileDialog.getSaveFileName(None, 'Save assets', None, 'Python (*.py)')
            
            if fileName:
                print os.path.join(os.path.dirname(__file__), self.qrcFilePath)

                compileResourceToPython(qrcFilePath, os.path.join(os.path.dirname(__file__),self.compiledPythonFilePath))
                compileResourceToPython(qrcFilePath, fileName)  

                importSuccess = False
                try:
                    import icons
                    importSuccess = True

                except ImportError:
                    print 'could not import icons.py'
                
                if importSuccess:
                    self.populateListViewFromQrc(qrcFilePath, self.model)



    def populateTextEditFromQrc(self, path, textEdit):
        
        data = None
        if(path):
            f = open(path,'r')
            data = f.read()
            f.close()
        if data:
            textEdit.setText(data)

    def createIconsFromQrc(self, xmlNode, model):

        if xmlNode.tag == 'file':
            
            item = QtGui.QStandardItem(xmlNode.text)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setIcon(QtGui.QIcon(QtGui.QPixmap(':/{}'.format(xmlNode.text))))
            model.appendRow(item)

        xmlChildren = xmlNode.getchildren()

        if xmlChildren:

            for xmlChild in xmlChildren:

                self.createIconsFromQrc(xmlChild, model)

    def populateListViewFromQrc(self, qrcPath, model):
        tree = ET.parse(qrcPath)
        root = tree.getroot()
        self.createIconsFromQrc(root, model)


def main():
     
    app = QtGui.QApplication(sys.argv)
    win = TestWin()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
        