# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TipWidget.ui'
#
# Created: Tue Jun 23 19:13:29 2015
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TipWidget(object):
    def setupUi(self, TipWidget):
        TipWidget.setObjectName(_fromUtf8("TipWidget"))
        TipWidget.resize(375, 82)
        TipWidget.setStyleSheet(_fromUtf8("background-color: rgb(89, 89, 89);"))
        self.image_label = QtGui.QLabel(TipWidget)
        self.image_label.setGeometry(QtCore.QRect(10, 10, 64, 64))
        self.image_label.setFrameShape(QtGui.QFrame.NoFrame)
        self.image_label.setText(_fromUtf8(""))
        self.image_label.setObjectName(_fromUtf8("image_label"))
        self.text_label = QtGui.QLabel(TipWidget)
        self.text_label.setGeometry(QtCore.QRect(80, 20, 281, 41))
        self.text_label.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"font: 11pt \"新宋体\";"))
        self.text_label.setObjectName(_fromUtf8("text_label"))

        self.retranslateUi(TipWidget)
        QtCore.QMetaObject.connectSlotsByName(TipWidget)

    def retranslateUi(self, TipWidget):
        TipWidget.setWindowTitle(QtGui.QApplication.translate("TipWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.text_label.setText(QtGui.QApplication.translate("TipWidget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

