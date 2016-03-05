#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from functools import partial
from PySide import QtGui, QtCore

def apa(name):
    print name

class MyPathItem(QtGui.QGraphicsPathItem):

    def __init__(self, name, quick_groups=None):
        super(MyPathItem, self).__init__()
        self.setAcceptHoverEvents(True)
        self.setOpacity(.2)
        self.name = name
        self.quick_groups = quick_groups

    def hoverEnterEvent(self, event):
        #print('Enter: {}').format(self.name)

        if self.quick_groups:
            self.setCursor(QtCore.Qt.CrossCursor)
        else:
            self.setCursor(QtCore.Qt.PointingHandCursor)

        self.setOpacity(.6)

    def hoverLeaveEvent(self, event):
        #print('Leave: {}').format(self.name)
        self.setOpacity(.2)

    def mousePressEvent(self, event):

        modifiers = QtGui.QApplication.keyboardModifiers()

        if modifiers == QtCore.Qt.NoModifier:
            print self.name

        else:
            print 'Modifier press' 
            

    def shape(self):
        return self.path()

    def contextMenuEvent(self, event):

        if self.quick_groups:

            menu = QtGui.QMenu()

            for name in self.quick_groups:
                action = menu.addAction(name)
                action.triggered.connect(partial(apa, name))

            selectedAction = menu.exec_(event.screenPos())
        else:
            print('"{}" has no quick groups').format(self.name)


    def add_quick_groups(self, quick_groups=None):
        self.quick_groups = quick_groups

class BaseWin(QtGui.QWidget):
    
    def __init__(self):
        super(BaseWin, self).__init__() 

        self.setGeometry(50, 100, 300, 300)
        self.setWindowTitle('Test')

        # layout
        vbox = QtGui.QVBoxLayout(self)

        self.scene = QtGui.QGraphicsScene()
    
        self.scene.addPixmap(QtGui.QPixmap('mario.png'))

        mario_item = self.add_hit_path( outer_pos_list=[(10,10), (90,10), (40,50), (10,50)],
                                        name='Mario',
                                        color=QtGui.QColor(255, 0, 0, 255),
                                        scene=self.scene,
                                        quick_groups=['Three', 'Four', 'Five'],
                                        inner_pos_list=[(20,20), (60,20), (30,40), (20,40)])


        toad_item = self.add_hit_path(  outer_pos_list=[(100,100), (200,100), (200,200), (100,200)],
                                        name='Toad',
                                        color=QtGui.QColor(0, 255, 135, 255),
                                        scene=self.scene,
                                        quick_groups=['One', 'Two'])

        toad_item.add_quick_groups()


        view = QtGui.QGraphicsView(self.scene)
        view.setSceneRect(0,0,300,300)
        
        vbox.addWidget(view)

    def add_hit_path(self, outer_pos_list, name, color, scene, quick_groups=None, inner_pos_list=None):

        path = QtGui.QPainterPath()

        polygon = [QtCore.QPoint(*p) for p in outer_pos_list]
        path.addPolygon(polygon)

        if inner_pos_list:
            polygon = [QtCore.QPoint(*p) for p in inner_pos_list]
            path.addPolygon(polygon)
 
        item = MyPathItem(name, quick_groups)
        item.setPath(path)
        item.setBrush(QtGui.QBrush(color))
        item.setPen(QtGui.QPen(QtCore.Qt.NoPen))  

        scene.addItem(item)

        return item

def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()