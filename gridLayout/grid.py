from PySide import QtGui, QtCore
import sys


class Win(QtGui.QWidget):
	def __init__(self, parent=None):
		super(Win, self).__init__(parent)

		self.gridlayout = QtGui.QGridLayout(self)

		self.btn1 = QtGui.QPushButton('One')
		self.btn1.clicked.connect(self.remove)
		self.gridlayout.addWidget(self.btn1, 0,0)

		self.btn2 = QtGui.QPushButton('Two')
		self.btn2.clicked.connect(self.test)
		self.gridlayout.addWidget(self.btn2, 1,0)

		

	def remove(self):
		print self.btn1
		self.gridlayout.removeWidget(self.btn1)
		self.btn1.deleteLater()
		self.btn1 = None
		print self.btn1

	def test(self):
		print self.btn1




def main():
    
    app = QtGui.QApplication(sys.argv)
    win = Win()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()