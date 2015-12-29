#-*- coding: utf-8 -*-
import re
from PyQt4 import QtGui, QtCore
from Ui_Proxy import Ui_Proxy
from Serial import Serial
from TipWidget import TipWidget
from appicons import *
import DataManager
import util
import config

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        
        self.autoSend = False  # TODO: read config
        self.incPrefix = False # TODO: read config
        self.incStartVal = 0
        self.autoSendTimes = 0 
        
        self.ui = Ui_Proxy()
        self.flags = { "__isopen__": False, "__datatype__": config.ASCII_TYPE }
        
        self.ui.setupUi(self)
        self.ui.setupWidget(self)
        self.tipWidget = TipWidget(self)
        
        self.setupSignals()
        
        self.filterParent = re.compile("")
    
    def closeEvent(self, e):
        if self.flags["__isopen__"]:
            self.serial.terminate()
            
        e.accept()
        config.saveSettings(self.ui.getCurrentConfigDict())
        
    def setupSignals(self):
        self.ui.open_pushButton.clicked.connect(self.onOpenPort)
        self.ui.updatePort_pushButton.clicked.connect(self.onUpdatePort)
        self.ui.send_pushButton.clicked.connect(self.onSendData)
        self.ui.clear_pushButton.clicked.connect(self.ui.recv_TextBrowser.clear)
        self.ui.autoSend_checkBox.stateChanged.connect(self.onAutoSend)
        self.ui.sendType_comboBox.currentIndexChanged.connect(self.ui.onSendTypeChanged)
        self.ui.inc_checkBox.stateChanged.connect(self.onIncCheckBoxStateChanged)
        self.ui.resetStartVal_pushButton.clicked.connect(self.resetIncStartVal)
        
        self.ui.clearLcdNumber_pushButton.clicked.connect(self.ui.clearLcdNumber)
        
        self.ui.about_action.triggered.connect(self.onAbout)
        self.ui.settings_action.triggered.connect(self.onSettings)
        self.ui.saveData_action.triggered.connect(self.onSaveData)

    def openPort(self, settings=None):
        if not settings:
            settings = self.ui.getPortSettings()
                
        if not settings["port"]:
            return False, u"错误的串口号"
            
        self.serial = Serial()
        self.connect(self.serial.qtobj, QtCore.SIGNAL(Serial.SIG_NEWDATA), self.onRecvData)
        self.connect(self.serial.qtobj, QtCore.SIGNAL(Serial.SIG_RECVEXCEPTION), self.onRecvException)
        ret, msg = self.serial.open(settings)
        
        return ret, msg
        
    def closePort(self):
        self.serial.terminate()
        self.ui.onPortClosed()
        self.flags["__isopen__"] = False
        
    def onOpenPort(self):
        if self.flags["__isopen__"]:
            return self.closePort()
            
        self.ui.onPortOpening()
        
        ret, msg = self.openPort()
        if not ret:
            QtGui.QMessageBox.critical(self, u"打开串口失败", u"设备正忙或已移除, 请重新尝试打开")
        else:
            self.flags["__isopen__"] = True
            self.serial.start()
            self.ui.onPortOpened()
    
    def onUpdatePort(self):
        newCount = self.ui.updatePortComBox(self.flags["__isopen__"])
        self.tipWidget.makeInfoText(u"更新了 " + `newCount` + u" 个串口")
    
    def onSendData(self):
        if not self.flags["__isopen__"]:
            return
            
        data, _type = self.ui.getDataAndType()
        ret, msg = util.checkData(data, _type)
        if not ret:
            QtGui.QMessageBox.critical(self, "Error", u"%s" % msg)
            return
            
        if self.autoSend:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.onTimeout)
            self.timer.start(self.ui.getAutoSendInterval())
            self.ui.onAutoSendStarted()
        else:
            self.sendData()
        
    def sendData(self):
        data, _type = self.ui.getDataAndType()
        ret, buff = DataManager.getDataToSend(data, _type, self.ui.getAsciiTail())
        if not ret:
            QtGui.QMessageBox.critical(self, u"发送数据错误", buff)
            return
        
        # 以PB协议模式发送时, 在收发区显示协议编码后的HEX
        if _type == config.PROTO_TYPE:
            data += "\n" + util.toVisualHex(buff)
        elif _type == config.ASCII_TYPE:
            if self.incPrefix:
                buff = `self.incStartVal` + buff
                data = `self.incStartVal` + data
                self.incStartVal += 1
                
        self.ui.onSendData(unicode(data, "utf-8"), _type)
        try:
            self.serial.send(buff, _type)
            self.ui.addTXBytesNumber(len(buff))
        except Exception as e:
            if self.autoSend:
                self.ui.autoSend_checkBox.setChecked(False)
                QtGui.QMessageBox.critical(self, "", u"发送失败, 可能串口已关闭")
            
    def onRecvData(self, nData):
        self.ui.addRXBytesNumber(len(nData))
        text = DataManager.getVisualizedData(nData, self.ui.getRecvType())
        if self.filterParent.match(text):
            self.ui.onRecvData(text)
    
    def onRecvException(self):
        QtGui.QMessageBox.critical(self, u"接收异常", u"串口设备故障或已移除\n请先排查问题，再尝试请新打开串口")
        self.onOpenPort()
        # TODO: 更新串口列表
        
    def onAutoSend(self, status):
        self.autoSend = status == 2
        self.ui.onAutoSend(status)
        self.autoSendTimes = 0
    
    def onIncCheckBoxStateChanged(self, status):
        self.incPrefix = status == 2
    
    def resetIncStartVal(self):
        self.incStartVal = 0
        
    def onTimeout(self):
        if not self.autoSend:
            self.timer.stop()
            del self.timer
            return
        
        self.sendData()
        self.autoSendTimes += 1
        self.ui.updateAutoSendTimes(self.autoSendTimes)
        
        
    def onSettings(self):
        value, ret = QtGui.QInputDialog.getInt(self, u"数据合并", u"合并指定时间(毫秒)内收到的数据      ", config.mergeInterval)
        if not ret:
            return
        
        if value > 20:
            ret = QtGui.QMessageBox.question(self, u"提醒", u"过长的时间可能会造成数据丢失", u"仍要设置", u"放弃设置")
            if ret != 0:
                return
        
        if value >= 0:
            config.mergeInterval = value
    
    def onSaveData(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, u"保存数据", "", "Data File(*.txt)")
        if fileName == "":
            return
        
        if not util.writeToFile(fileName, self.ui.getRecvWidgetContent()):
            QtGui.QMessageBox.critical(self, u"错误", u"保存文件失败")
        
    def onAbout(self):
        QtGui.QMessageBox.information(self, u"关于", config.ABOUT_MESSAGE)
