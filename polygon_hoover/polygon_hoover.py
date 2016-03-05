#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore

class MyPathItem(QtGui.QGraphicsPathItem):

    def __init__(self, name):
        super(MyPathItem, self).__init__()
        self.setAcceptHoverEvents(True)
        self.setOpacity(.2)
        self.name = name

    def hoverEnterEvent(self, event):
        print('Enter: {}').format(self.name)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setOpacity(.6)

    def hoverLeaveEvent(self, event):
        print('Leave: {}').format(self.name)
        self.setOpacity(.2)

    def mousePressEvent(self, event):
        print self.name

    def shape(self):
        return self.path()


class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(50, 100, 300, 300)
        self.setWindowTitle('Test')

        # layout
        vbox = QtGui.QVBoxLayout(self)

        self.scene = QtGui.QGraphicsScene()
    
        self.scene.addPixmap(QtGui.QPixmap('mario.png'))

        self.add_hit_path(  outer_pos_list=[(10,10), (90,10), (40,50), (10,50)],
                            name='Mario',
                            color=QtGui.QColor(255, 0, 0, 255),
                            scene=self.scene,
                            inner_pos_list=[(20,20), (60,20), (30,40), (20,40)])


        self.add_hit_path(  outer_pos_list=[(100,100), (200,100), (200,200), (100,200)],
                            name='Toad',
                            color=QtGui.QColor(0, 255, 135, 255),
                            scene=self.scene)



        view = QtGui.QGraphicsView(self.scene)
        view.setSceneRect(0,0,300,300)
        
        vbox.addWidget(view)

    def add_hit_path(self, outer_pos_list, name, color, scene, inner_pos_list=None):

        path = QtGui.QPainterPath()

        polygon = [QtCore.QPoint(*p) for p in outer_pos_list]
        path.addPolygon(polygon)

        if inner_pos_list:
            polygon = [QtCore.QPoint(*p) for p in inner_pos_list]
            path.addPolygon(polygon)
 
        item = MyPathItem(name)
        item.setPath(path)
        item.setBrush(QtGui.QBrush(color))
        item.setPen(QtGui.QPen(QtCore.Qt.NoPen))  

        scene.addItem(item)

def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()