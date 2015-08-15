from PySide import QtGui, QtCore
import sys, random, math

def lerp(x0, y0, x1, y1, x):

    return y0+(y1-y0)*(float(x)-x0)/(x1-x0)

#t: current time, b: begInnIng value, c: change In value, d: duration

def linear(t, b, c, d):
    return c*t+b

def easeInCubic(t, b, c, d):
    t /= d
    return c*t*t*t+b

def easeOutCubic(t, b, c, d):
    t=t/d-1
    return c*(t*t*t + 1) + b

def easeInOutCubic(t, b, c, d):
    t /= d/2
    if t < 1:
        return c/2*t*t*t + b
    t -= 2
    return c/2*(t*t*t + 2) + b

class Widget(QtGui.QWidget):
    
    def __init__(self):
        super(Widget, self).__init__()
        
        self.setGeometry(50, 50, 200, 200)
        self.setWindowTitle('Widget')
        self.show()

        self.equations = {}
        self.equations['linear'] = linear
        self.equations['easeInOutCubic'] = easeInOutCubic
        self.equations['easeOutCubic'] = easeOutCubic
        self.equations['easeInCubic'] = easeInCubic

        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(5,5,5,5)
        self.setLayout(vbox)

        self.combo = QtGui.QComboBox()
        self.curve_canvas = CurveCanvas(self.equations.get(self.combo.currentText()))

        
        self.combo.addItems(self.equations.keys())
        self.combo.currentIndexChanged.connect(self.index_changed)
        self.combo.setCurrentIndex(3)

        vbox.addWidget(self.curve_canvas)
        vbox.addWidget(self.combo)

        self.min_spinbox = QtGui.QDoubleSpinBox()
        self.min_spinbox.setSingleStep(.05)
        self.min_spinbox.setRange(0, 0.95)
        vbox.addWidget(self.min_spinbox)

        self.min_spinbox.valueChanged.connect(self.min_spinbox_change)


        self.max_spinbox = QtGui.QDoubleSpinBox()
        self.max_spinbox.setSingleStep(.05)
        self.max_spinbox.setRange(0.05, 1.0)
        self.max_spinbox.setValue(1.0)

        vbox.addWidget(self.max_spinbox)

        self.max_spinbox.valueChanged.connect(self.max_spinbox_change)


        self.process_data_btn = QtGui.QPushButton('Process')
        vbox.addWidget(self.process_data_btn)
        self.process_data_btn.clicked.connect(self.process_data)

    def process_data(self):

        #print(self.combo.currentText())
        equation = self.equations.get(self.combo.currentText())
        num = 30
        mult = 100
        p_list = [i*(1.0/(num-1)) for i in range(num)]
        #print(p_list)

        for p in p_list:
            u = min(1.0,max(0, lerp(self.min_spinbox.value(),0,self.max_spinbox.value(),1,p)))
            y = equation(u, 0, 1.0, 1.0)
            print(y*mult)


    def index_changed(self, index):
        self.curve_canvas.change_equation(self.equations.get(self.combo.currentText()))
        self.curve_canvas.repaint()

    def min_spinbox_change(self, val):

        limit = self.max_spinbox.value()-.05
        if val > limit:
            self.min_spinbox.blockSignals(True)
            self.min_spinbox.setValue(limit)
            self.min_spinbox.blockSignals(False)
            val = limit

        self.curve_canvas.change_min(val)
        self.curve_canvas.repaint()



    def max_spinbox_change(self, val):

        limit = self.min_spinbox.value()+.05
        if val < limit:
            self.max_spinbox.blockSignals(True)
            self.max_spinbox.setValue(limit)
            self.max_spinbox.blockSignals(False)
            val = limit

        self.curve_canvas.change_max(val)
        self.curve_canvas.repaint()



class CurveCanvas(QtGui.QWidget):
    
    def __init__(self, equation):
        super(CurveCanvas, self).__init__()
        
        self.equation = equation
        self.min = 0.0
        self.max = 1.0

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
        
    def drawPoints(self, qp):
      
        #qp.setPen(QtCore.Qt.red)
        width, height = self.size().toTuple()
        offset = 6

        pen = QtGui.QPen()  # creates a default pen
        pen.setColor(QtGui.QColor(210,210,210))
        pen.setWidth(1)
        qp.setPen(pen)

        num = 11
        inc = 1.0/(num-1)
        for i in range(num):
            x = i*inc*(width-offset*2)+offset
            y = i*inc*(height-offset*2)+offset
            qp.drawLine(x,offset, x, height-offset)
            qp.drawLine(offset, y, width-offset, y)
        
        
        if self.equation is None:
            return

        old_min = self.min
        old_max = self.max

        pen.setColor(QtGui.QColor(150,150,150))
        qp.setPen(pen)

        for i in range(num-1):

            u1 = i * inc
            u2 = (i+1) * inc
            x1 = u1 * (width-offset*2) + offset
            x2 = u2 * (width-offset*2) + offset

            uy1 = min(1.0, max(0, lerp(old_min,0,old_max,1,u1)))
            uy2 = min(1.0, max(0, lerp(old_min,0,old_max,1,u2)))
            y1 = self.equation(uy1, 0, 1.0, 1.0) * (height-offset*2) + offset
            y2 = self.equation(uy2, 0, 1.0, 1.0) * (height-offset*2) + offset
            qp.drawLine(x1, -y1+height, x2, -y2+height)


        pen.setWidth(4)
        pen.setColor(QtCore.Qt.black)
        qp.setPen(pen)

        for i in range(num):
            u = i * inc
            uy = min(1.0,max(0, lerp(old_min,0,old_max,1,u)))
            x = u * (width-offset*2) + offset
            y = self.equation(uy, 0, 1.0, 1.0) * (height-offset*2) + offset
            qp.drawPoint(x, -y+height)

    def change_equation(self, equation):
        self.equation = equation

    def change_min(self, val):
        self.min = val

    def change_max(self, val):
        self.max = val

def main():

    app = QtGui.QApplication(sys.argv)
    #ex = CurveDraw()
    ex = Widget()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()