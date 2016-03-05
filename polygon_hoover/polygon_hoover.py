#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from functools import partial
from PySide import QtGui, QtCore
import json, os

def apa(name):
    print name

class MyPathItem(QtGui.QGraphicsPathItem):

    def __init__(self, name):
        super(MyPathItem, self).__init__()
        self.setAcceptHoverEvents(True)
        self.setOpacity(.2)
        self.name = name
        self.quick_groups = None
        self.setToolTip(name)

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

        self.setGeometry(50, 100, 500, 500)
        self.setWindowTitle('Test')

        # layout
        vbox = QtGui.QVBoxLayout(self)

        self.scene = QtGui.QGraphicsScene()
    
        self.scene.addPixmap(QtGui.QPixmap('mario_bw.jpg'))

        view = QtGui.QGraphicsView(self.scene)
        view.setSceneRect(0,0,736,736)
        
        vbox.addWidget(view)

        self.load_paths()

        pants_item = self.hit_dict.get('Pants')
        if pants_item:
            pants_item.add_quick_groups(['One', 'Two'])

        hands_item = self.hit_dict.get('Hands')
        if hands_item:
            hands_item.add_quick_groups(['Three', 'Four', 'Five'])


    def load_paths(self):
        dirName = os.path.dirname(os.path.realpath(__file__))
        jsonPath = os.path.join(dirName, r'paths.json')

        with open(jsonPath, 'r') as f:
            data = f.read()
            jsonData = json.loads(data)
            #print jsonData

            for name, info_dict in jsonData.iteritems():

                path_outer = info_dict.get('path_outer')
                path_inner = info_dict.get('path_inner')
                color = info_dict.get('color')

                self.add_hit_path(  outer_pos=path_outer,
                                    name=name,
                                    color=color,
                                    scene=self.scene,
                                    inner_pos=path_inner)



    def add_hit_path(self, outer_pos, name, color, scene, inner_pos=None):

        path = QtGui.QPainterPath()
        color = QtGui.QColor(color[0], color[1], color[2], 255)

        for pos in outer_pos:
                polygon = [QtCore.QPoint(*p) for p in pos]
                path.addPolygon(polygon)

        #polygon = [QtCore.QPoint(*p) for p in outer_pos]
        #path.addPolygon(polygon)

        if inner_pos:
            for pos in inner_pos:
                polygon = [QtCore.QPoint(*p) for p in pos]
                path.addPolygon(polygon)
 
        item = MyPathItem(name=name)
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