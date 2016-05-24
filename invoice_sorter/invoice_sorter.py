import sys, os
from PySide import QtGui, QtCore
import petfactoryStyle

class Button(QtGui.QPushButton):
  
    def __init__(self, title, parent):
        super(Button, self).__init__(title, parent)
        
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
      
        #if e.mimeData().hasFormat('text/plain'):
        #    e.accept()
        #else:
        #    e.ignore() 
        e.accept()


    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            print dir(event.mimeData())
            print event.mimeData().html()
            links = []
            for url in event.mimeData().urls():
                
                links.append(str(url.toLocalFile()))
                print links[0]

        else:
            event.ignore()

class InvoiceSorterWindow(QtGui.QMainWindow):
    

    def __init__(self):
        super(InvoiceSorterWindow, self).__init__() 

        self.setGeometry(5, 50, 400, 600)
        self.setAcceptDrops(True)

        #menubar = self.menuBar()
        #menubar.setNativeMenuBar(False)
        #file_menu = menubar.addMenu('&File')

        main_frame = QtGui.QFrame()
        vbox = QtGui.QVBoxLayout(main_frame)

        self.model = QtGui.QStandardItemModel()
        self.model.appendRow(QtGui.QStandardItem('apa'))
        
        self.tableview = QtGui.QTableView()
        self.tableview.setModel(self.model)

        self.tableview.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        vbox.addWidget(self.tableview)

        self.setCentralWidget(main_frame)

        edit = QtGui.QLineEdit('', self)
        edit.setDragEnabled(True)
        vbox.addWidget(edit)

        button = Button("Button", self)
        vbox.addWidget(button)

    def dropEvent(self, e):
        print e.mimeData().text()





def main():
    
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(petfactoryStyle.load_stylesheet())
    win = InvoiceSorterWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()