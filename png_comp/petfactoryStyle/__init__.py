# -*- coding: utf-8 -*-

from PySide.QtCore import QFile, QTextStream
import platform
import pyside_style_rc


def load_stylesheet(pyside=True):


    f = QFile(":petfactoryStyle/style.qss")
    if not f.exists():
        pass

    else:
        f.open(QFile.ReadOnly | QFile.Text)
        ts = QTextStream(f)
        stylesheet = ts.readAll()
        if platform.system().lower() == 'darwin':  # see issue #12 on github
            mac_fix = '''
            QDockWidget::title
            {
                background-color: #353434;
                text-align: center;
                height: 12px;
            }
            '''
            stylesheet += mac_fix
        return stylesheet