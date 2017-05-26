#-*- coding: utf-8 -*-
from PyQt4 import QtGui

class Ui_TextView(QtGui.QTextBrowser):
    
    def __init__(self, parent):
        QtGui.QTextBrowser.__init__(self, parent)
        self.vbar = self.verticalScrollBar()
        
    def setPlainTextWithNoNL(self, text=""):
        textCursor = self.textCursor ()
        textCursor.movePosition(QtGui.QTextCursor.End)
        textCursor.insertText(text)
        self.vbar.setValue(self.vbar.maximum())
        