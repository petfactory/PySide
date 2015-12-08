
import sys, re, os
from PySide import QtGui

sys.path.append('/Users/johan/Dev/maya/petfactory_maya_scripts/petfactory')
#print(sys.path)
import gui.persistence


def get_files(dirPath, pattern):

    retStr = 'no match found'

    dirCont = os.listdir(dirPath)
    min = max = inc = 0
    frameNumList = []
    matchList = []
    for index, cont in enumerate(dirCont):
        
        if os.path.isfile(os.path.join(dirPath, cont)):

            match = pattern.match(cont)

            if match:
                fullMatch = match.group()
                mGroups = match.groups()
                matchList.append(fullMatch)

                try:
                    num = int(mGroups[0])
                except ValueError as e:
                    print('The capturing group is not a number!\n{}'.format(e))
                    return
                if inc == 0:
                    min = num
                    max = min
                    inc += 1

                if num < min:
                    min = num

                elif num > max:
                    max = num

                if num not in frameNumList:
                    frameNumList.append(num)

                fullSet = set(xrange(min, max + 1))
                diffSet = fullSet.difference(set(frameNumList))


                retStr = '{} Total number of frames\n'.format((max+1)- min)
                retStr += '{} Missing frames\n'.format(len(diffSet))
                retStr += 'missing values are :{0}\n'.format(sorted(diffSet))

                print(retStr)

                print('-----------')

                for i in range(min, max+1):
                    name = ''
                    if i in diffSet:
                        name = '-> missing'
                    print('{} {}'.format(i, name))

                print('-----------')

    return retStr


class SeqFinder(QtGui.QWidget):
    
    def __init__(self):
        super(SeqFinder, self).__init__()
                
        self.setGeometry(200, 200, 250, 350)
        self.setWindowTitle('Sequence finder')

        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)
        
        self.setDirBtn = QtGui.QPushButton('Set source dir')
        vbox.addWidget(self.setDirBtn)
        self.setDirBtn.clicked.connect(self.selectDirBtn)

        self.dirPathLineEdit = QtGui.QLineEdit()
        vbox.addWidget(self.dirPathLineEdit)

        self.regexTextEdit = QtGui.QLineEdit()
        self.regexTextEdit.setText('^robot_lighting.([\d]*).png$')
        vbox.addWidget(self.regexTextEdit)
        

        searchBtn = QtGui.QPushButton('Search')
        vbox.addWidget(searchBtn)
        searchBtn.clicked.connect(self.searchSeq)

        self.resultTextEdit = QtGui.QTextEdit()
        vbox.addWidget(self.resultTextEdit)

        vbox.addStretch()
        self.show()

    def selectDirBtn(self):
        dir = gui.persistence.select_dir('Select source dir')
        if dir:
            print(dir)
            self.dirPathLineEdit.setText(dir)

    def searchSeq(self):

        dirPath = self.dirPathLineEdit.text()
        if not os.path.isdir(dirPath):
            res = '"{}" is not a valid directory'.format(dirPath)
            print(res)
            self.resultTextEdit.setText(res)
            return

        pattern = re.compile(self.regexTextEdit.text())

        res = get_files(dirPath, pattern)
        self.resultTextEdit.setText(res)

        
def main():
    
    app = QtGui.QApplication(sys.argv)
    sf = SeqFinder()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()