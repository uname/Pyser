#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = 1
from PyQt4.QtGui import QApplication
from MainWindow import MainWindow

__author__ = "Apache"
__version__ = "0.1"
__email__ = "apache@tencent.com"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("plastique")
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
