import sys, os
from PySide import QtGui, QtCore
import xml.etree.ElementTree as ET
import style
import treeviewWithEditor

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setGeometry(20, 60, 350, 450)
        self.setWindowTitle('Outliner')  

        splitter = QtGui.QSplitter()
        self.setCentralWidget(splitter)

        outliner = treeviewWithEditor.Outliner()
        splitter.addWidget(outliner)

        outliner2 = treeviewWithEditor.Outliner()
        splitter.addWidget(outliner2)
        



def main():
    
    app = QtGui.QApplication(sys.argv)

    style.compile_rc()
    app.setStyleSheet(style.loadStyleSheet())

    mainWin = MainWindow()
    mainWin.show() 
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()