#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
from PySide import QtGui

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.setGeometry(60, 100, 250, 150)
        self.setWindowTitle('Icon')
        
        vbox = QtGui.QVBoxLayout(self)

        combobox = QtGui.QComboBox()
        combobox.addItems(['Orange', 'Apple', 'Pear'])

        itemDelegate = QtGui.QStyledItemDelegate()
        combobox.setItemDelegate(itemDelegate); 

        combobox.setStyleSheet('''QComboBox QAbstractItemView::item {
                    min-height: 30px;}
                    ''')

        vbox.addWidget(combobox)    

        self.show()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()