#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore
import os

def loadStyleSheet():

    import style.style_rc

    f = QtCore.QFile(":petfactoryStyle/style.qss")

    if not f.exists():
        print "Unable to load stylesheet, file not found in resources"
        return

    else:
        f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        ts = QtCore.QTextStream(f)
        stylesheet = ts.readAll()
        return stylesheet


def compile_rc():
    """Compile using pyside-rcc """
    
    print("Compiling for PySide: style.qrc -> style_rc.py")
    abspath = os.path.dirname(os.path.abspath(__file__))
    os.system("pyside-rcc -py3 {} -o {}".format(os.path.join(abspath, 'style.qrc'), os.path.join(abspath, 'style_rc.py')))