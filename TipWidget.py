#-*- coding: utf-8 -*-
# This is a tip widget like Toast.makeText in Android
# Version 1.0Beta
# Code by HeQingwei

from Ui_TipWidget import Ui_TipWidget
from tipicons import *

from Queue import Queue
from PyQt4.QtGui import QApplication, QWidget, QPixmap
from PyQt4.QtCore import QTimer, Qt

class TipWidget(QWidget):
    
    TIMER_INTERVAL     = 10
    TIMER_COUNTER_STEP = 30
    MAX_OPACITY_TIME   = 100
    
    TEXT_TYPE_INFO     = 1
    TEXT_TYPE_WARNING  = 2
    TEXT_TYPE_ERROR    = 3
    INFO_ICON_PATH     = ":/tip/icons/tip/info.png"
    WARNING_ICON_PATH  = ":/tip/icons/tip/warning.png"
    ERROR_ICON_PATH    = ":/tip/icons/tip/error.png"

    SHORT_TIME         = 2000
    LONG_TIME          = 4000
    
    MAX_QUEUE_SIZE = 20
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.ui = Ui_TipWidget()
        self.ui.setupUi(self)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.__onTimeout)
        self.queue = Queue(self.MAX_QUEUE_SIZE)
        
        self.timerCounter = 0
        self.maxOpacityCounter = 0
        
        self.setWindowOpacity(0)
    
    def __makeText(self, text, type=TEXT_TYPE_INFO, t=SHORT_TIME):
        if self.timer.isActive():
            if not self.queue.full():
                self.queue.put_nowait((text, type, t))
            return
            
        iconPath = self.INFO_ICON_PATH
        if type == self.TEXT_TYPE_WARNING:
            iconPath = self.WARNING_ICON_PATH
        elif type == self.TEXT_TYPE_ERROR:
            iconPath = self.ERROR_ICON_PATH
        
        self.ui.image_label.setPixmap(QPixmap(iconPath))
        self.ui.text_label.setText(text)
        self.timer.start(self.TIMER_INTERVAL)
        
        self.show()
    
    def makeInfoText(self, text="", t=SHORT_TIME):
        self.__makeText(text, self.TEXT_TYPE_INFO, t)
    
    def makeWarningText(self, text="", t=SHORT_TIME):
        self.__makeText(text, self.TEXT_TYPE_WARNING, t)
    
    def makeErrorText(self, text="", t=LONG_TIME):
        self.__makeText(text, self.TEXT_TYPE_ERROR, t)
        
    def __onTimeout(self):
        self.timerCounter += self.TIMER_COUNTER_STEP
        if self.timerCounter >= self.SHORT_TIME:
            self.__onFinished()
            return
            
        if self.timerCounter < self.SHORT_TIME / 2:
            self.setWindowOpacity(1.0 / (self.SHORT_TIME / 2) * self.timerCounter)
        else:
            self.maxOpacityCounter += 1
            if self.maxOpacityCounter < self.MAX_OPACITY_TIME:
                self.timerCounter -= self.TIMER_COUNTER_STEP
                return
                
            self.setWindowOpacity(1.0 / (self.SHORT_TIME / 2) * (self.SHORT_TIME - self.timerCounter))
            
    def __onFinished(self):
        self.close()
        self.timer.stop()
        self.maxOpacityCounter = 0
        self.timerCounter = 0
        if not self.queue.empty():
            args = self.queue.get()
            self.__makeText(args[0], args[1], args[2])
            
if __name__ == "__main__":
    import sys
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv)
    w = SC_TipWidget()
    w.makeInfoText("information test message")
    w.makeWarningText("warning test message")
    w.makeErrorText("error test message")
    sys.exit(app.exec_())