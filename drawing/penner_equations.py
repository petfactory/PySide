from PySide import QtGui, QtCore
import sys, random, math

def lerp(x0, y0, x1, y1, x):

    return y0+(y1-y0)*(float(x)-x0)/(x1-x0)

#t: current time, b: begInnIng value, c: change In value, d: duration

def linear(t, b, c, d):
    return (c-b)*(t/d)

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
        self.equations['easeInCubic'] = easeInCubic
        self.equations['easeOutCubic'] = easeOutCubic
        

        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(5,5,5,5)
        self.setLayout(vbox)
        self.curve_canvas = CurveCanvas(self.equations['linear'])
        vbox.addWidget(self.curve_canvas)

        self.combo = QtGui.QComboBox()
        self.combo.addItems(self.equations.keys())
        vbox.addWidget(self.combo)
        self.combo.currentIndexChanged.connect(self.index_changed)

    def index_changed(self, index):
        self.curve_canvas.change_equation(self.equations.get(self.combo.currentText()))
        self.curve_canvas.repaint()

        



class CurveCanvas(QtGui.QWidget):
    
    def __init__(self, equation):
        super(CurveCanvas, self).__init__()
        
        self.equation = equation
        #self.setGeometry(50, 50, 100, 100)
        self.setWindowTitle('Points')
        self.show()
        

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
        
    def drawPoints(self, qp):
      
        #qp.setPen(QtCore.Qt.red)

        pen = QtGui.QPen()  # creates a default pen
        pen.setWidth(2)
        qp.setPen(pen)
        
        
        if self.equation is None:
            return

        width, height = self.size().toTuple()
        num_p = 20;
        inc = 1.0/(num_p-1)

        '''
        for i in range(num_p-1):

            u1 = i * inc
            u2 = (i+1) * inc
            x1 = u1 * width
            x2 = u2 * width
            y1 = self.equation(u1, 0, height, 1.0)
            y2 = self.equation(u2, 0, height, 1.0)
            qp.drawLine(x1, -y1+height, x2, -y2+height)
        '''
        offset = 6
        pen.setWidth(5)
        qp.setPen(pen)

        for i in range(num_p):
            u = i * inc
            x = u * (width-offset*2) + offset
            y = self.equation(u, 0, (height-offset*2), 1.0)
            qp.drawPoint(x, -(y+offset)+height)
            print(x, y+ offset)

    def change_equation(self, equation):
        self.equation = equation

def main():

    app = QtGui.QApplication(sys.argv)
    #ex = CurveDraw()
    ex = Widget()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()