from PySide import QtGui, QtCore
import mario
import sys

class TestWin(QtGui.QWidget):
    
    def __init__(self):
        super(TestWin, self).__init__()
        
        self.setGeometry(10, 10, 20, 20)
        self.setWindowTitle('Test RCC Win')

        vbox = QtGui.QVBoxLayout(self)

        self.addLabels([':fish.png', ':question.png', ':toad.png', ':brick/subBrick/brick.png'], vbox)
        

    def addLabels(self, nameList, layout):

        for name in nameList:
            label = QtGui.QLabel()
            label.setPixmap(name)
            layout.addWidget(label)


def main():
     
    app = QtGui.QApplication(sys.argv)
    win = TestWin()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()