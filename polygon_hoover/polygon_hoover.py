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
            if modifiers == QtCore.Qt.ShiftModifier:
                print 'Shift modifier used' 

            else:
                print 'Some modifier used' 

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

        self.hit_dict = {}

        self.setGeometry(50, 100, 300, 300)
        self.setWindowTitle('Test')

        # layout
        vbox = QtGui.QVBoxLayout(self)

        self.scene = QtGui.QGraphicsScene()
    
        #self.scene.addPixmap(QtGui.QPixmap('mario.png'))


        self.add_hit_path(  outer_pos=[(10,10), (90,10), (40,50), (10,50)],
                            name='Mario',
                            color=(255, 0, 0),
                            scene=self.scene,
                            inner_pos=[[(20,20), (60,20), (30,40), (20,40)]])


        self.add_hit_path(  outer_pos=[(100,100), (200,100), (200,200), (100,200)],
                            name='Toad',
                            color=(0, 255, 135),
                            scene=self.scene,
                            inner_pos=[ [(110,110), (130,110), (130,130), (110,130)],
                                        [(170,170), (190,170), (190,190), (170,190)],
                                        [(150,110), (190,110), (190,130), (150,130)]])

        mario_item = self.hit_dict.get('Mario')
        if mario_item:
            mario_item.add_quick_groups(['One', 'Two'])

        toad_item = self.hit_dict.get('Toad')
        if toad_item:
            toad_item.add_quick_groups(['Three', 'Four', 'Five'])

        view = QtGui.QGraphicsView(self.scene)
        view.setSceneRect(0,0,300,300)
        
        vbox.addWidget(view)

    def add_hit_path(self, outer_pos, name, color, scene, quick_groups=None, inner_pos=None):

        path = QtGui.QPainterPath()
        color = QtGui.QColor(color[0], color[1], color[2], 255)
        polygon = [QtCore.QPoint(*p) for p in outer_pos]
        path.addPolygon(polygon)

        if inner_pos:
            for pos in inner_pos:
                polygon = [QtCore.QPoint(*p) for p in pos]
                path.addPolygon(polygon)
 
        item = MyPathItem(name=name, quick_groups=quick_groups)
        item.setPath(path)
        item.setBrush(QtGui.QBrush(color))
        item.setPen(QtGui.QPen(QtCore.Qt.NoPen))  
        scene.addItem(item)

        self.hit_dict[name] = item


def main():
    
    app = QtGui.QApplication(sys.argv)
    baseWin = BaseWin()
    baseWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()