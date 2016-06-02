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



def buildQrc(sourceDir, destFileName):

    if not os.path.isdir(sourceDir):
        print 'The source directory is not valid'
        return

    destFilePath = os.path.join(sourceDir, '{}.qrc'.format(destFileName))

    if os.path.isfile(destFilePath):
        print 'The file; {} exists, overwrite...'

    rccElem = ET.Element('RCC')
    qresourceElem = ET.Element('qresource')
    rccElem.append(qresourceElem)

    recurseFlatDir(sourceDir, qresourceElem)
    

    xmlString = ET.tostring(rccElem)
    miniDomXml = xml.dom.minidom.parseString(xmlString)
    prettyXML = miniDomXml.toprettyxml(indent='    ')

    sansfirstline = '\n'.join(prettyXML.split('\n')[1:]) 
    print sansfirstline

    if(destFilePath):
        f = open(destFilePath,'w')
        f.write(sansfirstline)
        f.close()
    

def compileResource(inputQrc, outFile):

    dirPath = os.path.dirname(__file__)
    rccPath = os.path.join(dirPath, 'pyside-rcc')
    outFile = os.path.join(dirPath, outFile)
    inputQrc = os.path.join(dirPath, inputQrc)

    subprocess.call([rccPath, inputQrc, '-o', outFile])


class TestWin(QtGui.QWidget):
    
    def __init__(self):
        super(TestWin, self).__init__()
        
        self.setGeometry(10, 50, 500, 400)
        self.setWindowTitle('Test RCC Win')

        vbox = QtGui.QVBoxLayout(self)
        splitter = QtGui.QSplitter()
        vbox.addWidget(splitter)        

        self.model = QtGui.QStandardItemModel()
        self.listView = QtGui.QListView()
        self.listView.setAlternatingRowColors(True)
        self.listView.setModel(self.model)
        splitter.addWidget(self.listView)
        #self.populateListView(self.model, [':/apa', ':/write', ':/sub1/switch.png', ':/sub1/sub2/read.png'])

        self.textEdit = QtGui.QTextEdit()
        splitter.addWidget(self.textEdit)

        self.populateListViewFromQrc('/Users/johan/Desktop/pysideRcc/icons/icons.qrc', self.model)

        self.populateTextEditFromQrc('/Users/johan/Desktop/pysideRcc/icons/icons.qrc', self.textEdit)

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
            
    def populateListView(self, model, imageNameList):
        #print imageNameList

        for imageName in imageNameList:
            item = QtGui.QStandardItem(imageName)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setIcon(QtGui.QIcon(QtGui.QPixmap(imageName)))
            model.appendRow(item)
         
def main():
     
    buildQrc('/Users/johan/Desktop/pysideRcc/icons', 'icons')
    compileResource('/Users/johan/Desktop/pysideRcc/icons/icons.qrc', 'icons.py')

    importSuccess = False
    try:
        import icons
        importSuccess = True
    except ImportError:
        print 'could not import icons.py'
    
    if importSuccess:
    
        app = QtGui.QApplication(sys.argv)
        win = TestWin()
        win.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
        