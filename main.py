#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = 1
from PyQt4.QtGui import QApplication
from MainWindow import MainWindow

__author__ = "uname"
__version__ = "0.1"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("cde")
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
