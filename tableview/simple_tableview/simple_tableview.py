import sys
from PySide import QtGui

class MyTable(QtGui.QWidget):
    
    def __init__(self):
        super(MyTable, self).__init__()
                
        self.setGeometry(200, 200, 250, 350)
        self.setWindowTitle('Test')

        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)
        
        self.model = QtGui.QStandardItemModel()

        tableview = QtGui.QTableView()
        vbox.addWidget(tableview)
        tableview.setModel(self.model)

        btn = QtGui.QPushButton("OK")
        vbox.addWidget(btn)

        self.add_items('A B C D E'.split(' '))

        self.show()

    def add_items(self, item_list):

    	for row, item in enumerate(item_list):

    		q_item = QtGui.QStandardItem(item)
            
        	self.model.setItem(row, 0, q_item)
        
def main():
    
    app = QtGui.QApplication(sys.argv)

    ex = MyTable()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()